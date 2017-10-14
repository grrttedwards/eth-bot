gdax_agent 
---------- 
 
#### What is this? 
I'm learning about the world of crypto, and figured why not start watching some prices? This runs on my otherwise idle [raspberry pi that hosts my WeatherClock](https://github.com/grrttedwards/raspberry-pi-matrix/). The script pushes a report to me via Pushbullet once every [insert frequency I've yet to determine here] that says the most recent trade, the best bid/ask price, and the value of the trade from the last [update frequency].  
 
#### Why not just use [some app you know about]? 
Because I didn't want to, this is much simpler for me, and this gets pushed to all my devices. 
 
#### How use this 
Edit the settings file with your Pushbullet API token. You could even monitor BTC on GDAX with it, just go set the agent product to 'BTC-USD'. 