#Copyright 2020 Sleepingpirate. 

import discord
from discord.ext import commands
import asyncio
from plexapi.myplex import MyPlexAccount
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import db as db


# settings
Discord_bot_token = 'NzE5OTIyMjE0NzQ4Njg0NDQ4.Xt-eCA.3AfI93j0it3dHKI5BaMb8o0tzAk' 
roleid = 719937272480530432             # Role Id, right click the role and copy id.  
PLEXUSER = 'sahil.sharma071997@gmail.com'           # Plex Username
PLEXPASS = 'DUbBaNenQ!8SdQG'           # plex password
PLEX_SERVER_NAME = 'Sahil-Y50'   # Name of plex server 
Plex_LIBS = ["Films"] #name of the libraries you want the user to have access to.
chan = 719924353789329420 #Channel id of the channel you want to log emails and use -plexadd in. 

account = MyPlexAccount(PLEXUSER, PLEXPASS)
plex = account.resource(PLEX_SERVER_NAME).connect()  # returns a PlexServer instance

def plexadd(plexname):
    try:
        plex.myPlexAccount().inviteFriend(user=plexname, server=plex, sections=Plex_LIBS, allowSync=False,
                                              allowCameraUpload=False, allowChannels=False, filterMovies=None,
                                              filterTelevision=None, filterMusic=None)

    except Exception as e:
        print(e)
        return False
    else:
        print(plexname +' has been added to plex (☞ຈل͜ຈ)☞')
        return True


def plexremove(plexname):
    try:
        plex.myPlexAccount().removeFriend(user=plexname, server=plex)

    except Exception as e:
        print(e)
        return False
    else:
        print(plexname +' has been added to plex (☞ຈل͜ຈ)☞')
        return True

class MyClient(discord.Client):
    async def on_ready(self):
        print('Made by Sleepingpirate https://github.com/Sleepingpirates/')
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_member_update(self, before, after):
        role = after.guild.get_role(roleid)
        if (role in after.roles and role not in before.roles):
            await after.send('Welcome To '+ PLEX_SERVER_NAME +'. Just reply with your email so we can add you to Plex!')
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
            if plexadd(plexname):
                db.save_user(after.display_name, email.content)
                await asyncio.sleep(20)
                await after.send('You have Been Added To Plex!')
                secure = client.get_channel(chan)
                await secure.send(plexname + ' ' + after.mention + ' was added to plex')
            else:
                await after.send('There was an error adding this email address. Message Server Admin.')
        if(role not in after.roles and role in before.roles):
            print('condt2')
            # plexremove(after.)
            
            




    async def on_message(self, message):
        secure = client.get_channel(chan)
        if message.author.id == self.user.id:
            return

        if str(message.channel) == str(secure):
            if message.content.startswith('-plexadd'):
                mgs = message.content.replace('-plexadd ','')
                if plexadd(mgs):
                    await message.channel.send('The email has been added! {0.author.mention}'.format(message))
                else:
                    message.channel.send('Error Check Logs! {0.author.mention}'.format(message))
            if message.content.startswith('-plexrm'):
                mgs = message.content.replace('-plexrm ','')
                if plexremove(mgs):
                    await message.channel.send('The email has been removed! {0.author.mention}'.format(message))
                else:
                    message.channel.send('Error Check Logs! {0.author.mention}'.format(message))

client = MyClient()
client.run(Discord_bot_token)
