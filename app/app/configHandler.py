import configparser

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

def change_config_form(form_output):
    """
    Function to change config on the basis of form_output from web
    """
    for key in CONFIG_KEYS:
        try:
            change_config(key, form_output[key].data)
        except:
            pass
