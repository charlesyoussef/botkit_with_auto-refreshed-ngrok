# botkit_with_auto-refreshed-ngrok
Botkit automatically reloaded with a refreshed ngrok tunnel session

It overcomes the limitation of the ngrok free account limitation of tunnel expiration every 8 hours,
by automatically stopping the current ngrok and botkit every 7.5 hours and then recreating a new ngrok
session, getting the new session's URL, and restarting botkit using the new URL.
