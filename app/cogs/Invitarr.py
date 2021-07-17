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
from app.header.configparser import roleid, PLEXUSER, PLEXPASS, PLEX_SERVER_NAME, Plex_LIBS, chan, ownerid, auto_remove_user

sys.stdout = sys.stderr
Plex_LIBS = list(Plex_LIBS.split(','))
roleid = list(roleid.split(','))

if auto_remove_user:
    print("auto remove user = True")
    import db as db

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
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        secure = client.get_channel(chan)
        for role_for_plex in roleid:
            role = after.guild.get_role(int(role_for_plex))
            if (role in after.roles and role not in before.roles):
                await after.send('Welcome To '+ PLEX_SERVER_NAME +'. Just reply with your email so we can add you to Plex!')
                await after.send('I will wait 10 minutes for your message, if you do not send it by then I will cancel the command.')
                def check(m):
                    return m.author == after and not m.guild
                try:
                    email = await client.wait_for('message', timeout=600, check=check)
                except asyncio.TimeoutError:
                    await after.send('Timed Out. Message Server Admin So They Can Add You Manually.')
                    return
                else:
                    await asyncio.sleep(5)
                    await after.send('Got it we will be processing your email shortly')
                    print(email.content) #make it go to a log channel
                    plexname = str(email.content)
                    if plexadd(plexname):
                        if auto_remove_user:
                            db.save_user(str(after.id), email.content)
                        await asyncio.sleep(20)
                        await after.send('You have Been Added To Plex!')
                        await secure.send(plexname + ' ' + after.mention + ' was added to plex')
                    else:
                        await after.send('There was an error adding this email address. Message Server Admin.')
                    return
            
            elif(role not in after.roles and role in before.roles):
                if auto_remove_user:
                    try:
                        user_id = after.id
                        email = db.get_useremail(user_id)
                        plexremove(email)
                        deleted = db.delete_user(user_id)
                        if deleted:
                            print("Removed {} from db".format(email))
                            await secure.send(plexname + ' ' + after.mention + ' was removed from plex')
                        else:
                            print("Cannot remove this user from db.")
                    except:
                        print("Cannot remove this user from plex.")
                return
            

def setup(bot):
    bot.add_cog(app(bot))