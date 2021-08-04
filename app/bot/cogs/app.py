import discord
from discord.ext import commands
import asyncio
from plexapi.myplex import MyPlexAccount
from discord import Webhook, AsyncWebhookAdapter
import app.bot.helper.db as db
import app.bot.helper.plexhelper as plexhelper
import texttable
import os 
from os import path
import configparser
CONFIG_PATH = 'app/config/config.ini'
BOT_SECTION = 'bot_envs'

# settings
roles = None
PLEXUSER = ""
PLEXPASS = ""
PLEX_SERVER_NAME = ""
Plex_LIBS = None

if(path.exists('app/config/config.ini')):
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        PLEXUSER = config.get(BOT_SECTION, 'plex_user')
        PLEXPASS = config.get(BOT_SECTION, 'plex_pass')
        PLEX_SERVER_NAME = config.get(BOT_SECTION, 'plex_server_name')
    except:
        pass
if(path.exists('app/config/config.ini')):
    try:
        roles = config.get(BOT_SECTION, 'roles')
    except:
        pass
if(path.exists('app/config/config.ini')):
    try:
        Plex_LIBS = config.get(BOT_SECTION, 'plex_libs')
    except:
        pass

try:
    account = MyPlexAccount(PLEXUSER, PLEXPASS)
    plex = account.resource(PLEX_SERVER_NAME).connect()  # returns a PlexServer instance
    print('Logged into plex!')
except:
    print('Error with plex login. Please check username and password and Plex server name or setup plex in the bot.')

if roles is not None:
    roles = list(roles.split(','))

if Plex_LIBS is None:
    Plex_LIBS = ["all"]
else:
    Plex_LIBS = list(Plex_LIBS.split(','))

class app(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Made by Sleepingpirate https://github.com/Sleepingpirates/')
        print(f'Logged in as {self.bot.user} (ID: {self.bot.user.id})')
        print('------')
        if roles is None:
            print('Configure roles to enable auto invite after a role is assigned.')
    
    async def embederror(self, author, message):
        embed1 = discord.Embed(title="ERROR",description=message, color=0xf50000)
        await author.send(embed=embed1)

    async def embedinfo(self, author, message):
        embed1 = discord.Embed(title=message, color=0x00F500)
        await author.send(embed=embed1)

    async def getemail(self, after):
        email = None
        await self.embedinfo(after,'Welcome To '+ PLEX_SERVER_NAME +'. Just reply with your email so we can add you to Plex!')
        await self.embedinfo(after,'I will wait 24 hours for your message, if you do not send it by then I will cancel the command.')
        while(email == None):
            def check(m):
                return m.author == after and not m.guild
            try:
                email = await self.bot.wait_for('message', timeout=86400, check=check)
                if(plexhelper.verifyemail(str(email.content))):
                    return str(email.content)
                else:
                    email = None
                    message = "Invalid email. Please just type in your email and nothing else."
                    await self.embederror(after, message)
                    continue
            except asyncio.TimeoutError:
                message = "Timed Out. Message Server Admin with your email so They Can Add You Manually."
                await self.embederror(after, message)
                return None


    async def addtoplex(self, email, channel):
        if(plexhelper.verifyemail(email)):
            if plexhelper.plexadd(plex,email,Plex_LIBS):
                await self.embedinfo(channel, 'This email address has been added to plex')
                return True
            else:
                await self.embederror(channel, 'There was an error adding this email address. Check logs.')
                return False
        else:
            await self.embederror(channel, 'Invalid email.')
            return False

    async def addtoplexhome(self, email, channel):
        if(plexhelper.verifyemail(email)):
            if plexhelper.plexhomeadd(plex,email,Plex_LIBS):
                await self.embedinfo(channel, 'This email address has been added to plex home')
                return True
            else:
                await self.embederror(channel, 'There was an error adding this email address. Check logs.')
                return False
        else:
            await self.embederror(channel, 'Invalid email.')
            return False

    async def removefromplex(self, email, channel):
        if(plexhelper.verifyemail(email)):
            if plexhelper.plexremove(plex,email):
                await self.embedinfo(channel, 'This email address has been removed from plex.')
                return True
            else:
                await self.embederror(channel, 'There was an error removing this email address. Check logs.')
                return False
        else:
            await self.embederror(channel, 'Invalid email.')
            return False
    
    async def removefromplexhome(self, email, channel):
        if(plexhelper.verifyemail(email)):
            if plexhelper.plexremovehome(plex,email):
                await self.embedinfo(channel, 'This email address has been removed from plex home.')
                return True
            else:
                await self.embederror(channel, 'There was an error removing this email address. Check logs.')
                return False
        else:
            await self.embederror(channel, 'Invalid email.')
            return False

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if roles is None:
            return
        roles_in_guild = after.guild.roles
        role = None
        for role_for_app in roles:
            for role_in_guild in roles_in_guild:
                if role_in_guild.name == role_for_app:
                    role = role_in_guild

                if role is not None and (role in after.roles and role not in before.roles):
                    email = await self.getemail(after)
                    if email is not None:
                        await self.embedinfo(after, "Got it we will be adding your email to plex shortly!")
                        if plexhelper.plexadd(plex,email,Plex_LIBS):
                            db.save_user(str(after.id), email)
                            await asyncio.sleep(5)
                            await self.embedinfo(after, 'You have Been Added To Plex! Login to plex and accept the invite!')
                        else:
                            await self.embedinfo(after, 'There was an error adding this email address. Message Server Admin.')
                    return

                elif role is not None and (role not in after.roles and role in before.roles):
                    try:
                        user_id = after.id
                        email = db.get_useremail(user_id)
                        plexhelper.plexremove(plex,email)
                        deleted = db.delete_user(user_id)
                        if deleted:
                            print("Removed {} from db".format(email))
                            #await secure.send(plexname + ' ' + after.mention + ' was removed from plex')
                        else:
                            print("Cannot remove this user from db.")
                    except Exception as e:
                        print(e)
                        print("{} Cannot remove this user from plex.".format(email))
                    return

    @commands.cog.listener()
    async def on_member_remove(self, member):
        email = db.get_useremail(member.id)
        plexhelper.plexremove(plex,email)
        deleted = db.delete_user(member.id)
        if deleted:
            print("Removed {} from db because user left discord server.".format(email))

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['plexadd'])
    async def plexinvite(self, ctx, email):
        await self.addtoplex(email, ctx.channel)
    
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['plexrm'])
    async def plexremove(self, ctx, email):
        await self.removefromplex(email, ctx.channel)
    
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['plexaddhome'])
    async def plexinvitehome(self, ctx, email):
        await self.addtoplexhome(email, ctx.channel)
    
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['plexrmhome'])
    async def plexremovehome(self, ctx, email):
        await self.removefromplexhome(email, ctx.channel)
        
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def dbadd(self, ctx, email, member: discord.Member):
        #await self.addtoplex(email, ctx.channel)
        if plexhelper.verifyemail(email):
            try:
                db.save_user(str(member.id), email)
                await self.embedinfo(ctx.channel,'email and user were added to the database.')
            except Exception as e:
                await self.embedinfo(ctx.channel, 'There was an error adding this email address to database.')
                print(e)
        else:
            await self.embederror(ctx.channel, 'Invalid email.')

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def dbls(self, ctx):

        embed = discord.Embed(title='Invitarr Database.')
        all = db.read_useremail()
        table = texttable.Texttable()
        table.set_cols_dtype(["t", "t", "t"])
        table.set_cols_align(["c", "c", "c"])
        header = ("#", "Name", "Email")
        table.add_row(header)
        for index, peoples in enumerate(all):
            index = index + 1
            id = int(peoples[1])
            dbuser = self.bot.get_user(id)
            dbemail = peoples[2]
            try:
                username = dbuser.name
            except:
                username = "User Not Found."
            embed.add_field(name=f"**{index}. {username}**", value=dbemail+'\n', inline=False)
            table.add_row((index, username, dbemail))
        
        total = str(len(all))
        if(len(all)>25):
            f = open("db.txt", "w")
            f.write(table.draw())
            f.close()
            await ctx.channel.send("Database too large! Total: {total}".format(total = total),file=discord.File('db.txt'))
        else:
            await ctx.channel.send(embed = embed)
        
            

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def dbrm(self, ctx, position):
        embed = discord.Embed(title='Invitarr Database.')
        all = db.read_useremail()
        table = texttable.Texttable()
        table.set_cols_dtype(["t", "t", "t"])
        table.set_cols_align(["c", "c", "c"])
        header = ("#", "Name", "Email")
        table.add_row(header)
        for index, peoples in enumerate(all):
            index = index + 1
            id = int(peoples[1])
            dbuser = self.bot.get_user(id)
            dbemail = peoples[2]
            try:
                username = dbuser.name
            except:
                username = "User Not Found."
            embed.add_field(name=f"**{index}. {username}**", value=dbemail+'\n', inline=False)
            table.add_row((index, username, dbemail))

        try:
            position = int(position) - 1
            id = all[position][1]
            email = db.get_useremail(id)
            deleted = db.delete_user(id)
            if deleted:
                print("Removed {} from db".format(email))
                await self.embedinfo(ctx.channel,"Removed {} from db".format(email))
            else:
                await self.embederror(ctx.channel,"Cannot remove this user from db.")
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(app(bot))