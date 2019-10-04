import os
import json
from os import environ

ENV = environ.get('env', 'development')
CONFIG_FILE_PATH = os.path.join(os.path.curdir, 'config', 'config.json')

def get_config(env):
    if env in ['development', 'production']:
        if os.path.isfile(CONFIG_FILE_PATH):
            config = json.load(open(CONFIG_FILE_PATH,'r'))
            return config.get(env,None)
    return None


global_config = get_config(ENV)
    
