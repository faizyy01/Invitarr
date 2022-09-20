import discord
import os
from os import path
from discord.ext import commands, tasks
from discord.utils import get
from plexapi.myplex import MyPlexPinLogin
import asyncio
import sys
import secrets
from app.bot.helper.confighelper import switch, Discord_bot_token, roles, CONFIG_PATH, BOT_SECTION
import app.bot.helper.confighelper as confighelper
import configparser
maxroles = 10



if roles is None:
    roles = []
else:
    roles = list(roles.split(','))

if switch == 0:
    print("Missing Config.")
    sys.exit()

print("V 1.0")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=".", intents = intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print("bot is online.")


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    if not message.guild:
        return
    await bot.process_commands(message)

def reload():
    bot.reload_extension(f'app.bot.cogs.app')

async def getplex(ctx, message):
    username = None
    await ctx.author.send(message)
    while(username == None):
        def check(m):
            return m.author == ctx.author and not m.guild
        try:
            username = await bot.wait_for('message', timeout=200, check=check)
            return username.content
        except asyncio.TimeoutError:
            message = "Timed Out. Try again."
            return None

async def gettoken(ctx, identifier):
    try:
        headers = {
            'X-Plex-Product': 'Invitarr',
            'X-Plex-Client-Identifier': str(identifier)
        }
        pinlogin = MyPlexPinLogin(headers=headers, requestTimeout=300, oauth=True)
        await ctx.author.send("Please follow this link within five minutes to authenticate Invitarr:\n{}".format(pinlogin.oauthUrl()))
        pinlogin.run()
        pinlogin.waitForLogin()
        return pinlogin.token
    except asyncio.TimeoutError:
        await ctx.author.send("Timed Out. Try again.")
        return None

@bot.command()           
@commands.has_permissions(administrator=True)
async def roleadd(ctx, role: discord.Role):
    if len(roles) <= maxroles:
        roles.append(role.name)
        saveroles = ",".join(roles)
        confighelper.change_config("roles", saveroles)
        await ctx.author.send("Updated roles. Bot is restarting. Please wait.")
        print("Roles updated. Restarting bot.")
        reload()
        await ctx.author.send("Bot has been restarted. Give it a few seconds.")
        print("Bot has been restarted. Give it a few seconds.")

@bot.command()
@commands.has_permissions(administrator=True)
async def setupplex(ctx):
    token = ""
    plexurl = ""
    identifier = None
    if(path.exists('app/config/config.ini')):
        try:
            config = configparser.ConfigParser()
            config.read(CONFIG_PATH)
            identifier = config.get(BOT_SECTION, 'identifier')
        except:
            pass
    if identifier is None:
        identifier = "{} (Invitarr)".format(secrets.token_urlsafe(16))
        print(identifier)
        confighelper.change_config("identifier", identifier)
    token = await gettoken(ctx, identifier)
    if token is None:
        return
    plexurl = await getplex(ctx, "Please reply with the url to your plex server:")
    if plexurl is None:
        return
    confighelper.change_config("plex_token", str(token))
    confighelper.change_config("plex_url", str(plexurl))
    print("Plex token and plex url updated. Restarting bot.")
    await ctx.author.send("Plex token and plex url updated. Restarting bot. Please wait.")
    reload()
    await ctx.author.send("Bot has been restarted. Give it a few seconds. Please check logs and make sure you see the line: `Logged into plex`. If not run this command again and make sure you enter the right values. ")
    print("Bot has been restarted. Give it a few seconds.")

@bot.command()
@commands.has_permissions(administrator=True)
async def setuplibs(ctx):
    libs = ""
    libs = await getplex(ctx, "libs")
    if libs is None:
        return
    else:
        confighelper.change_config("plex_libs", str(libs))
        print("Plex libraries updated. Restarting bot. Please wait.")
        reload()
        await ctx.author.send("Bot has been restarted. Give it a few seconds. Please check logs and make sure you see the line: `Logged into plex`. If not run this command again and make sure you enter the right values. ")
        print("Bot has been restarted. Give it a few seconds.")

bot.load_extension(f'app.bot.cogs.app')
bot.run(Discord_bot_token)