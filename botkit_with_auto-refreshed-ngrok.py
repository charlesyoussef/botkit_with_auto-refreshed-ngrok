#!/usr/bin/env python
"""This is part of the MEA-Calendar Webex-Teams bot functionality.
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
import threading
import sys


__author__ = "Charles Youssef"
__copyright__ = "Copyright 2019 Cisco and/or its affiliates"
__license__ = "CISCO SAMPLE CODE LICENSE"
__version__ = "1.1"
__email__ = "cyoussef@cisco.com"


def bot_run():
    # get the new ngrok session URL for the HTTPS session:
    ngrok_api_url = "http://localhost:4040/api/tunnels"
    ngrok_new_session_response = requests.get(ngrok_api_url).text
    #print(ngrok_new_session_response)
    ngrok_new_tunnel_url = json.loads(ngrok_new_session_response)['tunnels'][1]['public_url']
    time.sleep(10)
    print("%s: %s" % (time.asctime(time.localtime(time.time())), "Starting a new bot..."))
    command = "PUBLIC_URL=%s node bot.js" % ngrok_new_tunnel_url
    subprocess.run(command, shell=True)


def main():
    # stop the currently running botkit node:
    print("%s: %s" % (time.asctime(time.localtime(time.time())), "Stopping the current bot..."))
    stop_ngrok = subprocess.run("pkill -9 node", shell=True)
    time.sleep(10)

    # stop the currently running ngrok session:
    print("%s: %s" % (time.asctime(time.localtime(time.time())), "Stopping the current ngrok session..."))
    stop_ngrok = subprocess.run("pkill -9 ngrok".split(), stdout = subprocess.PIPE)
    time.sleep(10)

    # start a new ngrok session on http port 3000 (used by botkit):
    print("%s: %s" % (time.asctime(time.localtime(time.time())), "Starting a new ngrok session..."))
    ngrok = subprocess.Popen(['ngrok','http', '3000'], stdout = subprocess.PIPE)
    time.sleep(10)

    # start a new botkit node as a separate thread, as otherwise the command
    # has to be ran with Shell=True and otherwise the program execution is stopped
    threading1 = threading.Thread(target=bot_run)
    threading1.daemon = True
    threading1.start()


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
