import discord
from discord.ext import commands
import asyncio
from plexapi.myplex import MyPlexAccount
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

account = MyPlexAccount('user', 'pass')
plex = account.resource('plex server name here').connect()  # returns a PlexServer instance

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_member_update(self, before, after):
        role1 = after.guild.get_role(roleid) #I had two roles... you are welcome to use just one or many...
        role2 = after.guild.get_role(roleid)
        if (role1 in after.roles and role1 not in before.roles) or (role2 in after.roles and role2 not in before.roles):
            await after.send('Welcome To Sleepingpirates Plex Server. Just reply with your email so we can add you to Plex!')
            await after.send('I will wait 10 minutes for your message, if you do not send it by then I will cancel the command.')
            def check(m):
                return m.author == after and not m.guild
            try:
                email = await client.wait_for('message', timeout=600, check=check)
            except asyncio.TimeoutError:
                await after.send('error... message pirate... so he can add you manually.')
            else:
                await asyncio.sleep(5)
                await after.send('Got it we will be processing your email shortly')
            print(email.content) #for logging... 
            plexname = str(email.content)
            try:
                plex.myPlexAccount().inviteFriend(user=plexname, server=plex, sections=["Movies","TV Shows","Movies - Trending","Anime"], allowSync=False, #your libs here
                                                      allowCameraUpload=False, allowChannels=False, filterMovies=None,
                                                      filterTelevision=None, filterMusic=None)
                await asyncio.sleep(20)

            except Exception as e:
                print(e)
            else:
                await after.send('You have Been Added To Plex!')
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url('webhook url here', adapter=AsyncWebhookAdapter(session)) #webhook to a discord channel to log emails
                await webhook.send(plexname + ' was added to plex', username='Logger')

client = MyClient()
client.run('token-here')
