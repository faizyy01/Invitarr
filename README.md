[![Discord](https://img.shields.io/discord/708829995744755822?color=7289DA&label=Discord&style=for-the-badge&logo=discord)](https://discord.gg/vcxCytN) 
[![DockerHub](https://img.shields.io/badge/Docker-Hub-%23099cec?style=for-the-badge&logo=docker)](https://hub.docker.com/r/piratify/invitarr)
![Docker Pulls](https://img.shields.io/docker/pulls/piratify/invitarr?color=099cec&style=for-the-badge)
[![Deploy](http://img.shields.io/badge/%E2%86%91_Deploy_to-Heroku-7056bf.svg?style=for-the-badge)](https://dashboard.heroku.com/new?template=https://github.com/Sleepingpirates/Invitarr-Heroku)
# Invitarr
Plex Discord Bot to invite a user to a plex server once a user gets a certain role in discord. 

Once a role is given to the discord user, they get a direct message asking for their email and their email gets added to plex. 

If the discord user loses their role their email is also removed from plex. (You can disable this and the database if you want.)

Commands: 
```
-plexadd "email" #To add an email to plex. 
-plexrm "email" #To remove an email that is in plex. 
-dbadd "email" @user #To link an exsisting user's plex email and discord account.
```

# Installation & Configuration

Envs:

```
PLEXUSER=
PLEXPASS=
PLEX_SERVER_NAME=
Plex_LIBS=
ownerid=
discord_bot_token=
roleid=
channelid=
autoremoveuser=True #Default is set to False. This enables database and auto-remove. 
```

Refer to the [Wiki](https://github.com/Sleepingpirates/Invitarr/wiki) for detailed steps.

Quick Link to docker -> https://hub.docker.com/r/piratify/invitarr

# Screenshots
![bot](https://github.com/Sleepingpirates/Invitarr/blob/master/Screenshots/June_06.10.2020_07.08.21_PM.png)
