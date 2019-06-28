#!/usr/bin/env python
"""
This script allows for a Botkit to be automatically reloaded with a new refreshed ngrok tunnel session.

It overcomes the limitation of the ngrok free account limitation of tunnel expiration every 8 hours,
by automatically stopping the current ngrok and botkit every 7.5 hours and then recreating a new ngrok
session, getting the new session's URL, and restarting botkit using the new URL.

The logic is scheduled to run every 7.5 hours natively within the script. No need for external cron scheduler.

"""

import subprocess
import requests
import json
import time
import schedule

__author__ = "Charles Youssef"
__copyright__ = "Copyright 2019 Cisco and/or its affiliates"
__license__ = "CISCO SAMPLE CODE LICENSE"
__version__ = "1.0"
__email__ = "cyoussef@cisco.com"


def main():
    # stop the currently running botkit node:
    print("Stopping the current bot...")
    stop_botkit = subprocess.run("pkill -9 node".split(), stdout = subprocess.PIPE)
    time.sleep(1)

    # stop the currently running ngrok session:
    print("Stopping the current ngrok session...")
    stop_ngrok = subprocess.run("pkill -9 ngrok".split(), stdout = subprocess.PIPE)
    time.sleep(1)

    # start a new ngrok session on http port 3000 (used by botkit):
    print("Starting a new ngrok session...")
    start_ngrok = subprocess.Popen(['ngrok','http', '3000'], stdout = subprocess.PIPE)
    time.sleep(1)

    # get the new ngrok session URL for the HTTPS session:
    ngrok_api_url = "http://localhost:4040/api/tunnels"
    ngrok_new_session_response = requests.get(ngrok_api_url).text
    ngrok_new_tunnel_url = json.loads(ngrok_new_session_response)['tunnels'][1]['public_url']
    time.sleep(1)

    # start a new botkit node:
    print("Starting a new bot...")
    start_botkit = "PUBLIC_URL=%s node bot.js" % ngrok_new_tunnel_url
    subprocess.run(start_botkit, shell=True)


if __name__ == "__main__":
    # Run the program now then repeatedly every 7hours 30 minutes = 450 minutes
    main()
    schedule.every(450).minutes.do(main)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except (KeyboardInterrupt, EOFError):
            sys.exit(1)
