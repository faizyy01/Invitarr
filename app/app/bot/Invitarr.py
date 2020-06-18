#Copyright 2020 Sleepingpirate.
import os
from os import environ
import discord
from discord.ext import commands
import asyncio
from plexapi.myplex import MyPlexAccount
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from dotenv import load_dotenv
import configparser
CONFIG_PATH = 'app/config/config.ini'
BOT_SECTION = 'bot_envs'

try:
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
except:
    print("Cannot find config")

# settings
Discord_bot_token = config.get(BOT_SECTION, 'discord_bot_token')
roleid = int(config.get(BOT_SECTION, 'role_id'))
PLEXUSER = config.get(BOT_SECTION, 'plex_user')
PLEXPASS = config.get(BOT_SECTION, 'plex_pass')
PLEX_SERVER_NAME = config.get(BOT_SECTION, 'plex_server_name')
Plex_LIBS = config.get(BOT_SECTION, 'plex_libs')
chan = int(config.get(BOT_SECTION, 'channel_id'))
ownerid = int(config.get(BOT_SECTION, 'owner_id'))
auto_remove_user = config.get(BOT_SECTION, 'auto_remove_user') if config.get(BOT_SECTION, 'auto_remove_user') else False

li = list(Plex_LIBS.split(','))
Plex_LIBS = li

#rolenames = list(roleid.split(','))

if auto_remove_user:
    print("auto remove user = True")
    import db as db

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
        plex.myPlexAccount().removeFriend(user=plexname)
    except Exception as e:
        print(e)
        return False
    else:
        print(plexname +' has been removed from plex (☞ຈل͜ຈ)☞')
        return True

class MyClient(discord.Client):
    async def on_ready(self):
        print('Made by Sleepingpirate https://github.com/Sleepingpirates/')
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await client.change_presence(activity=discord.Game(name="Do -help in {}".format(client.get_channel(chan))))

    async def on_member_update(self, before, after):
        role = after.guild.get_role(roleid)
        secure = client.get_channel(chan)
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
                if auto_remove_user:
                    db.save_user(str(after.id), email.content)
                await asyncio.sleep(20)
                await after.send('You have Been Added To Plex!')
                await secure.send(plexname + ' ' + after.mention + ' was added to plex')
            else:
                await after.send('There was an error adding this email address. Message Server Admin.')
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


    async def on_message(self, message):
        secure = client.get_channel(chan)
        if message.author.id == self.user.id:
            return

        if message.author.id == ownerid:
           if message.content.startswith('-db add'):
               mgs = message.content.replace('-db add ','')
               try:
                   mgs = mgs.split(' ')
                   email = mgs[0]
                   bad_chars = ['<','>','@','!']
                   user_id = mgs[1]
                   for i in bad_chars:
                       user_id = user_id.replace(i, '')
                   db.save_user(user_id, email)
                   await secure.send(email + ' ' + mgs[1] + ' was added to plex')
               except:
                   await message.channel.send('Cannot add this user to db.')
                   print("Cannot add this user to db.")
               await message.delete()

        if str(message.channel) == str(secure):
            if message.content.startswith('-db ls') or message.content.startswith('-db rm'):
                embed = discord.Embed(title='Invitarr Database.')
                all = db.read_useremail()
                for index, peoples in enumerate(all):
                    index = index + 1
                    id = int(peoples[1])
                    dbuser = client.get_user(id)
                    dbemail = peoples[2]
                    embed.add_field(name=f"**{index}. {dbuser.name}**", value=dbemail+'\n', inline=False)
                if message.content.startswith('-db ls'):
                    await secure.send(embed = embed)
                else:
                    try:
                        position = message.content.replace("-db rm", "")
                        position = int(position) - 1
                        id = all[position][1]
                        email = db.get_useremail(id)
                        deleted = db.delete_user(id)
                        if deleted:
                            print("Removed {} from db".format(email))
                            await secure.send("Removed {} from db".format(email))
                        else:
                            print("Cannot remove this user from db.")
                    except Exception as e:
                        print(e)

            if message.content.startswith('-help'):
                embed = discord.Embed(title='Invitarr Bot Commands', description='Made by [Sleepingpirates](https://github.com/Sleepingpirates/Invitarr), [Join Discord Server](https://discord.gg/vcxCytN)')
                embed.add_field(name='-plexadd <email>', value='This command is used to add an email to plex', inline=False)
                embed.add_field(name='-plexrm <email>', value='This command is used to remove an email from plex', inline=False)
                embed.add_field(name='-db ls', value='This command is used list Invitarrs database', inline=False)
                embed.add_field(name='-db add <email> <@user>', value='This command is used add exsisting users email and discord id to the DB.', inline=False)
                embed.add_field(name='-db rm <position>', value='This command is used remove a record from the Db. Use -db ls to determine record position. ex: -db rm 1', inline=False)
                await secure.send(embed = embed)


    async def on_member_remove(self, member):
        if auto_remove_user:
            try:
                user_id = member.id ## not there
                email = db.get_useremail(user_id)
                plexremove(email)
                deleted = db.delete_user(user_id)
                if deleted:
                    print("Removed {} from db".format(email))
                    secure = client.get_channel(chan)
                    await secure.send(email + ' ' + member.mention + 'was removed from plex because they left the server')
                else:
                    print("Cannot remove this user from db.")
            except:
                print("Cannot remove this user from plex.")

client = MyClient()
client.run(Discord_bot_token)
