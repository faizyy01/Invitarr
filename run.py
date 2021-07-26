import discord
import os
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import sys
from app.bot.helper.confighelper import switch, Discord_bot_token, roles
import app.bot.helper.confighelper as confighelper
maxroles = 10

if roles is None:
    roles = []
else:
    roles = list(roles.split(','))

if switch == 0:
    print("Missing Config.")
    sys.exit()

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

async def getplex(ctx, type):
    username = None
    await ctx.author.send("Please reply with your Plex {}:".format(type))
    while(username == None):
        def check(m):
            return m.author == ctx.author and not m.guild
        try:
            username = await bot.wait_for('message', timeout=200, check=check)
            return username.content
        except asyncio.TimeoutError:
            message = "Timed Out. Try again."
            return None

@bot.command()           
@commands.has_permissions(administrator=True)
async def roleadd(ctx, role: discord.Role):
    if len(roles) <= maxroles:
        roles.append(role.name)
        saveroles = ",".join(roles)
        confighelper.change_config("roles", saveroles)
        await ctx.author.send("Updated roles. Bot is restarting.")
        print("Roles updated. Restarting bot.")
        reload()
        await ctx.author.send("Bot has been restarted. Give it a few seconds.")
        print("Bot has been restarted. Give it a few seconds.")

@bot.command()
@commands.has_permissions(administrator=True)
async def setupplex(ctx):
    username = ""
    pasword = ""
    servername = ""
    username = await getplex(ctx, "username")
    if username is None:
        return
    else:
        password = await getplex(ctx, "password")
        if password is None:
            return
        else:
            servername = await getplex(ctx, "servername")
            if servername is None:
                return
            else:
                confighelper.change_config("plex_user", str(username))
                confighelper.change_config("plex_pass", str(password))
                confighelper.change_config("plex_server_name", str(servername))
                print("Plex username, password, and plex server name updated. Restarting bot.")
                await ctx.author.send("Plex username, password, and plex server name updated. Restarting bot.")
                reload()
                await ctx.author.send("Bot has been restarted. Give it a few seconds. Please check logs and make sure you see the line: `Logged into plex`. If not run this command again and make sure you enter the right values. ")
                print("Bot has been restarted. Give it a few seconds.")
                
bot.load_extension(f'app.bot.cogs.app')
bot.run(Discord_bot_token)