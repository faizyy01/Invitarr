import os
from os import environ, path
import logging
import discord
from discord.ext import commands
import asyncio
from plexapi.myplex import MyPlexAccount
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import texttable
import sys
from app.header.configparser import roleid, PLEXUSER, PLEXPASS, PLEX_SERVER_NAME, Plex_LIBS, chan, ownerid

sys.stdout = sys.stderr
Plex_LIBS = list(Plex_LIBS.split(','))
roleid = list(roleid.split(','))

account = MyPlexAccount(PLEXUSER, PLEXPASS)
plex = account.resource(PLEX_SERVER_NAME).connect()  # returns a PlexServer instance

class app(commands.Cog):

    @commands.Cog.listener()
    async def on_ready(self):
        print('Made by Sleepingpirate https://github.com/Sleepingpirates/')
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


def setup(bot):
    bot.add_cog(app(bot))