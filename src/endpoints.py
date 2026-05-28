from flask import Flask, jsonify, request
from flask_cors import CORS
import os
# from chessdotcom_wrapper import ClientWrapper
# from lichess_wrapper import Driver
from configparser import ConfigParser
import requests
import logging
import functools
from typing import Callable, Any

app = Flask(__name__)
CORS(app)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("main")

# Config
config = ConfigParser()
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(script_dir, "..", "settings.ini")
config.read(config_file_path)


# Common error handling decorator for view functions
def safe_api_call(fn: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            logger.debug("Calling endpoint: %s", fn.__name__)
            return fn(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            logger.exception("HTTP request error in %s", fn.__name__)
            return jsonify({'error': str(e)}), 502
        except ValueError as e:
            logger.exception("Invalid input in %s", fn.__name__)
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.exception("Unexpected error in %s", fn.__name__)
            return jsonify({'error': 'internal server error'}), 500
    return wrapper


# Request logging (optional)
@app.before_request
def log_request_info():
    logger.info("Incoming request: %s %s from %s", request.method, request.path, request.remote_addr)




if __name__ == '__main__':
    app.run(debug=True)