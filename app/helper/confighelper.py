import configparser
from os import environ, path
from dotenv import load_dotenv
config = configparser.ConfigParser()

CONFIG_PATH = 'app/config/config.ini'
BOT_SECTION = 'bot_envs'
CONFIG_KEYS = ['username', 'password', 'discord_bot_token', 'plex_user', 'plex_pass',
                'role_id', 'plex_server_name', 'plex_libs', 'owner_id', 'channel_id',
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
roleid = 0
PLEXUSER = ""
PLEXPASS = ""
PLEX_SERVER_NAME = ""
Plex_LIBS = ""
chan = 0
ownerid = 0
auto_remove_user = ""

switch = 0 

try:
    if(path.exists(CONFIG_PATH)):
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        Discord_bot_token = config.get(BOT_SECTION, 'discord_bot_token')
        roleid = config.get(BOT_SECTION, 'role_id')
        PLEXUSER = config.get(BOT_SECTION, 'plex_user')
        PLEXPASS = config.get(BOT_SECTION, 'plex_pass')
        PLEX_SERVER_NAME = config.get(BOT_SECTION, 'plex_server_name')
        Plex_LIBS = config.get(BOT_SECTION, 'plex_libs')
        chan = int(config.get(BOT_SECTION, 'channel_id'))
        ownerid = int(config.get(BOT_SECTION, 'owner_id'))
        auto_remove_user = config.get(BOT_SECTION, 'auto_remove_user') if config.get(BOT_SECTION, 'auto_remove_user') else False
        switch = 1
    else:
        load_dotenv(dotenv_path='bot.env')
        Discord_bot_token = environ.get('discord_bot_token')
        roleid = int(environ.get('role_id'))
        PLEXUSER = environ.get('PLEXUSER')
        PLEXPASS = config.get(BOT_SECTION, 'plex_pass')
        PLEX_SERVER_NAME = config.get(BOT_SECTION, 'plex_server_name')
        Plex_LIBS = config.get(BOT_SECTION, 'plex_libs')
        chan = int(config.get(BOT_SECTION, 'channel_id'))
        ownerid = int(config.get(BOT_SECTION, 'owner_id'))
        auto_remove_user = config.get(BOT_SECTION, 'auto_remove_user') if config.get(BOT_SECTION, 'auto_remove_user') else False
        switch = 1
except:
    print("Cannot find config/Incomplete config")

