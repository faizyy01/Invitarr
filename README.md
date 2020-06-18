[![Discord](https://img.shields.io/discord/708829995744755822?color=7289DA&label=Discord&style=for-the-badge&logo=discord)](https://discord.gg/vcxCytN) 
[![DockerHub](https://img.shields.io/badge/Docker-Hub-%23099cec?style=for-the-badge&logo=docker)](https://hub.docker.com/r/piratify/invitarr)
![Docker Pulls](https://img.shields.io/docker/pulls/piratify/invitarr?color=099cec&style=for-the-badge)
# Invitarr
Plex Discord Bot to invite a user to a plex server once a user gets a certain role in discord. 

Once a role is given to the discord user, they get a direct message asking for their email and their email gets added to plex. 

If the discord user loses their role their email is also removed from plex. (You can disable this and the database if you want.)

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

```
docker pull piratify/invitarr:latest
docker run -d --restart unless-stopped --name invitarr -v /path to config:/app/app/config -p 5001:5001 piratify/invitarr:latest
```

Refer to the [Wiki](https://github.com/Sleepingpirates/Invitarr/wiki) for detailed steps.

# Screenshots
![bot](https://github.com/Sleepingpirates/Invitarr/blob/master/Screenshots/June_06.10.2020_07.08.21_PM.png)
