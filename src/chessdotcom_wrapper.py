import logging
import os
import requests
import pprint
from configparser import ConfigParser

import chessdotcom
from chessdotcom import ChessDotComClient

# Json printer setup
printer = pprint.PrettyPrinter(indent=4)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("chessdotcom_wrapper")

# Config
config = ConfigParser()
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(script_dir, "..", "settings.ini")
config.read(config_file_path)

account = config.get('main-section', 'account', fallback=None)



def get_last_ten_games(account):
    # Mandatory: Configure User-Agent for Chess.com API
    chessdotcom.Client.request_config["headers"]["User-Agent"] = "sergehychko: shychko@gmail.com"

    archives_response = chessdotcom.get_player_game_archives(account)
    archives = archives_response.json['archives']

    if not archives:
        print(f"No archives found for {account}")
        return []

    last_archive_url = archives[-1]

    headers = {
        "User-Agent": "sergehychko: shychko@gmail.com"
    }

    # 3. Fetch the games from that archive
    archive_response = requests.get(last_archive_url, headers=headers, timeout=10)
    archive_response.raise_for_status()
    games = archive_response.json()['games']
    return games[:10]


# Initialize client with a required User-Agent header
client = ChessDotComClient(user_agent="My Python Application")

# Retrieve profile for a specific user
response = client.get_player_profile(account)

# Access data via attributes
print(response.player.name)
print(response.player.title)
print(response.player.joined_datetime)



last_games = get_last_ten_games(account)
if last_games:
    #printer.pprint(last_games)
    for i, game in enumerate(last_games, 1):
        print(f"--- Game {i} ---")
        print(f"White: {game['white']['username']} : {game['white']['result']}")
        print(f"Black: {game['black']['username']} : {game['black']['result']}")
        print(f"PGN Preview: {game['pgn'][:100]}...")
else:
    print("No games found.")