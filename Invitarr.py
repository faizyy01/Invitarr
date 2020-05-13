#Copyright 2020 Sleepingpirate. 

import discord
from discord.ext import commands
import asyncio
from plexapi.myplex import MyPlexAccount
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

# settings
Discord_bot_token = '' 
roleid =                # Role Id, right click the role and copy id.  
PLEXUSER = ''           # Plex Username
PLEXPASS = ''           # plex password
PLEX_SERVER_NAME = ''   # Name of plex server 
Plex_LIBS = ["Movies","TV Shows"] #name of the libraries you want the user to have access to.
Webhookurl = '' # For logging the user repiles, create a webhook to the discord channel you want to log this in.



account = MyPlexAccount(PLEXUSER, PLEXPASS)
plex = account.resource(PLEX_SERVER_NAME).connect()  # returns a PlexServer instance

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_member_update(self, before, after):
        role = after.guild.get_role(roleid) 
        if (role in after.roles and role not in before.roles):
            await after.send('Welcome To The Plex. Just reply with your email so we can add you to Plex!')
            await after.send('I will wait 10 minutes for your message, if you do not send it by then I will cancel the command.')
            def check(m):
                return m.author == after and not m.guild
            try:
                email = await client.wait_for('message', timeout=600, check=check)
            except asyncio.TimeoutError:
                await after.send('Timed Out. Message Server Admin So They Can Add You Manually.')
            else:
                await asyncio.sleep(5)
                await after.send('Got it we will be processing your email shortly')
            print(email.content) #make it go to a log channel
            plexname = str(email.content)
            try:
                plex.myPlexAccount().inviteFriend(user=plexname, server=plex, sections=Plex_LIBS, allowSync=False, 
                                                      allowCameraUpload=False, allowChannels=False, filterMovies=None,
                                                      filterTelevision=None, filterMusic=None)
                await asyncio.sleep(20)

            except Exception as e:
                print(e)
            else:
                await after.send('You have Been Added To Plex!')
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(Webhookurl, adapter=AsyncWebhookAdapter(session)) 
                await webhook.send(plexname + ' was added to plex', username='Logger')

client = MyClient()
client.run(Discord_bot_token)
