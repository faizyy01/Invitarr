[![Discord](https://img.shields.io/discord/869287648487936040?color=7289DA&label=Discord&style=for-the-badge&logo=discord)](https://discord.gg/9M2NPtmmrV)
[![DockerHub](https://img.shields.io/badge/Docker-Hub-%23099cec?style=for-the-badge&logo=docker)](https://hub.docker.com/r/piratify/invitarr)
![Docker Pulls](https://img.shields.io/docker/pulls/piratify/invitarr?color=099cec&style=for-the-badge)

Invitarr 
=================

Invitarr is a chatbot that invites discord users to plex. You can also automate this bot to invite discord users to plex once a certain role is given to a user or the user can also be added manually.  

### Features

- Ability to invite users to plex from discord 
- Fully automatic invites using roles 
- Ability to kick users from plex if they leave the discord server or if their role is taken away.
- Ability to view the database in discord and to edit it.
- Fully configurable via a web portal

Commands: 

```
.plexinvite <email>
This command is used to add an email to plex
.plexremove <email>
This command is used to remove an email from plex
.dbls
This command is used to list Invitarrs database
.dbadd <email> <@user>
This command is used to add exsisting users email and discord id to the DB.
.dbrm <position>
This command is used to remove a record from the Db. Use -db ls to determine record position. ex: -db rm 1
```

# Setup 

**1. Enter discord bot token in bot.env**

**2. Install requirements**

```
pip3 install -r requirements.txt 
```
**3. Start the bot**
```
python3 Run.py
```

# Docker Setup & Start

1. First pull the image 
```
docker pull piratify/invitarr:latest
```
2. Make the container 
```
docker run -d --restart unless-stopped --name invitarr -v /path to config:/app/app/config -e "token=YOUR_DISCORD_TOKEN_HERE" piratify/invitarr:latest
```

# After bot has started 

Setup Commands: 

```
.setupplex
This command is used to setup plex login. 
.roleadd <@role>
These role(s) will be used as the role(s) to automatically invite user to plex
.setuplibs
This command is used to setup plex libraries. Default is set to all. 
```

Refer to the [Wiki](https://github.com/Sleepingpirates/Invitarr/wiki) for detailed steps.

**Enable Intents else bot will not Dm users after they get the role.**
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents

