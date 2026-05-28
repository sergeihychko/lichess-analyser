import logging
import os
import requests
import pprint
from configparser import ConfigParser

import berserk

# Json printer setup
printer = pprint.PrettyPrinter(indent=4)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("lichess_wrapper")

# Config
config = ConfigParser()
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(script_dir, "..", "settings.ini")
config.read(config_file_path)

token = config.get('main-section', 'lichess_token', fallback=None)