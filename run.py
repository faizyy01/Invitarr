import discord
import os
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import sys
from app.header.configparser import switch, Discord_bot_token

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


@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, name):
    bot.load_extension(f'Cogs.{name}')
    print(f"The {name} cog has been loaded successfully.")


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, name):
    bot.unload_extension(f'Cogs.{name}')
    print(f"The {name} cog has been unloaded successfully.")


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, name):
    bot.unload_extension(f'Cogs.{name}')
    bot.load_extension(f'Cogs.{name}')
    print(f"The {name} cog has been reloaded successfully.")


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    if not message.guild:
        return
    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def all(ctx):
    for filename in os.listdir("Cogs"):
        if filename.endswith('.py'):
            bot.unload_extension(f'Cogs.{filename[:-3]}')
    for filename in os.listdir("Cogs"):
        if filename.endswith('.py'):
            bot.load_extension(f'Cogs.{filename[:-3]}')
    print("All cogs has been reloaded.")


for filename in os.listdir("Cogs"):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')

bot.run(Discord_bot_token)