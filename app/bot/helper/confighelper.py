import configparser
from os import environ, path
from dotenv import load_dotenv
config = configparser.ConfigParser()

CONFIG_PATH = 'app/config/config.ini'
BOT_SECTION = 'bot_envs'
CONFIG_KEYS = ['username', 'password', 'discord_bot_token', 'plex_user', 'plex_pass',
                'roles', 'plex_server_name', 'plex_libs', 'owner_id', 'channel_id',
                'auto_remove_user']

def get_config():
    """
    Function to return current config
    """
    try:
        config.read(CONFIG_PATH)
        return config
    except Exception as e:
        print(e)
        print('error in reading config')
        return None


CONFIG_PATH = 'app/config/config.ini'
BOT_SECTION = 'bot_envs'

# settings
Discord_bot_token = ""
roles = ""
PLEXUSER = ""
PLEXPASS = ""
PLEX_SERVER_NAME = ""
Plex_LIBS = ""
chan = 0
ownerid = 0
auto_remove_user = ""

switch = 0 

try:
   load_dotenv(dotenv_path='bot.env')
   
   # settings
   Discord_bot_token = environ.get('discord_bot_token')
   roles = (environ.get('roles'))             # Role Id, right click the role and copy id.
   PLEXUSER = environ.get('plex_user')          # Plex Username
   PLEXPASS = environ.get('plex_pass')          # plex password
   PLEX_SERVER_NAME = environ.get('plex_server_name')    # Name of plex server
   Plex_LIBS = environ.get('plex_libs')  #name of the libraries you want the user to have access to.
   chan = int(environ.get('channel_id'))
   ownerid = int(environ.get('owner_id'))
   auto_remove_user = environ.get('auto_remove_user') if environ.get('auto_remove_user') else False # auto remove user from plex and db if removed from the role
   switch = 1
   if switch == 1:
       Plex_LIBS = list(Plex_LIBS.split(','))
       roles = list(roles.split(','))
        
except Exception as e:
    print(e)

