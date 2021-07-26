import configparser
import os
from os import environ, path
from dotenv import load_dotenv
CONFIG_PATH = 'app/config/config.ini'
BOT_SECTION = 'bot_envs'
config = configparser.ConfigParser()

CONFIG_KEYS = ['username', 'password', 'discord_bot_token', 'plex_user', 'plex_pass',
                'roles', 'plex_server_name', 'plex_libs', 'owner_id', 'channel_id',
                'auto_remove_user']

# settings
Discord_bot_token = ""
roles = None
PLEXUSER = ""
PLEXPASS = ""
PLEX_SERVER_NAME = ""
Plex_LIBS = ["all"]
switch = 0 


if(path.exists('bot.env')):
    try:
        load_dotenv(dotenv_path='bot.env')
        # settings
        Discord_bot_token = environ.get('discord_bot_token')            
        switch = 1
    
    except Exception as e:
        pass

elif(path.exists('app/config/config.ini')):
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        Discord_bot_token = config.get(BOT_SECTION, 'discord_bot_token')
    except:
        pass
else:
    try:
        Discord_bot_token = str(os.environ['token'])
        switch = 1
    except Exception as e:
        print("ERROR. No config found.")

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


def change_config(key, value):
    """
    Function to change the key, value pair in config
    """
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
    except Exception as e:
        print(e)
        print("Cannot Read config.")

    try:
        config.set(BOT_SECTION, key, str(value))
    except Exception as e:
        config.add_section(BOT_SECTION)
        config.set(BOT_SECTION, key, str(value))

    try:
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        print(e)
        print("Cannot write to config.")
