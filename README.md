[![Discord](https://img.shields.io/discord/733333568092373035?color=7289DA&label=Discord&style=for-the-badge&logo=discord)](https://discord.gg/EnUBXmF) 
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
-plexadd <email>
This command is used to add an email to plex
-plexrm <email>
This command is used to remove an email from plex
-db ls
This command is used to list Invitarrs database
-db add <email> <@user>
This command is used to add exsisting users email and discord id to the DB.
-db rm <position>
This command is used to remove a record from the Db. Use -db ls to determine record position. ex: -db rm 1
```

# Docker Setup & Start

1. First pull the image 
```
docker pull piratify/invitarr:latest
```
2. Make the container 
```
docker run -d --restart unless-stopped --name invitarr -v /path to config:/app/app/config -p 5001:5001 piratify/invitarr:latest
```

Refer to the [Wiki](https://github.com/Sleepingpirates/Invitarr/wiki) for detailed steps.

# Screenshot
![bot](https://github.com/Sleepingpirates/Invitarr/blob/master/Screenshots/June_06.10.2020_07.08.21_PM.png)
