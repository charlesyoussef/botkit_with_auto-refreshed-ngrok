# botkit_with_auto-refreshed-ngrok

This script allows for a Botkit to be automatically reloaded with a new refreshed ngrok tunnel session.

It overcomes the limitation of the ngrok free account limitation of tunnel expiration every 8 hours,
by automatically stopping the current ngrok and botkit every 7.5 hours and then recreating a new ngrok
session, getting the new session's URL, and restarting botkit using the new URL.


## Usage
$ python botkit_with_auto-refreshed-ngrok.py


## Installation & prerequisites

1. ngrok (https://ngrok.com) already installed
2. Botkit bot already present. This script will be copied to the working directory of the Botkit (where bot.js resides)
3. Python packages mentioned in requirements.txt installed. To install them:
$ pip install -r requirements.txt

It is recommended to install the Python dependencies in a new virtual environment based on Python 3.6 or above. For information on setting up a virtual environment please check:
http://docs.python-guide.org/en/latest/dev/virtualenvs/


## Authors & Maintainers

Charles Youssef <cyoussef@cisco.com>

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](./LICENSE).
