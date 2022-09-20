import configparser
import os
from os import environ, path
from dotenv import load_dotenv
CONFIG_PATH = 'app/config/config.ini'
BOT_SECTION = 'bot_envs'
config = configparser.ConfigParser()

CONFIG_KEYS = ['username', 'password', 'discord_bot_token', 'plex_token', 'plex_url',
                'roles', 'plex_libs', 'owner_id', 'channel_id', 'identifier',
                'auto_remove_user']

# settings
Discord_bot_token = ""
roles = None
PLEX_TOKEN = ""
PLEX_URL = ""
Plex_LIBS = None
switch = 0 


if(path.exists('bot.env')):
    try:
        load_dotenv(dotenv_path='bot.env')
        # settings
        Discord_bot_token = environ.get('discord_bot_token')            
        switch = 1
    
    except Exception as e:
        pass
        
try:
    Discord_bot_token = str(os.environ['token'])
    switch = 1
except Exception as e:
    pass

if(path.exists('app/config/config.ini')):
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        PLEX_TOKEN = config.get(BOT_SECTION, 'plex_token')
        PLEX_URL = config.get(BOT_SECTION, 'plex_url')
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