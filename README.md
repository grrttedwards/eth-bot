gdax_agent 
---------- 
 
### What is this? 
I'm learning about the world of crypto, and figured why not start watching some prices? This runs on my otherwise idle [raspberry pi that hosts my WeatherClock](https://github.com/grrttedwards/raspberry-pi-matrix/). The script pushes a report to me via Pushbullet once every [insert frequency I've yet to determine here] that says the most recent trade, the best bid/ask price, and the value of the trade from the last [update frequency].  
 
### Why not just use [some app you know about]? 
Because I didn't want to, this is much simpler for me, and this gets pushed to all my devices. 
 
### How use this 
Edit `settings.ini` with your Pushbullet API token. You can monitor any currency on GDAX with it, just go set the agent product to the product string e.g. `'BTC-USD'`.

If you want to get a few different currencies, just comma separate them when creating a GDAX_Agent e.g. `'ETH-USD', 'BTC-USD'`

Running
```
python gdax-agent.py
```

### Requirements
- Python 3.6 for the sweet string literal interpolation
- `pip install -r requirements.txt` or `pip install requests gdax`


### Todo:
- ~~I want to get more than one currency: cool yeah I'll do that~~ done!
- I want an alert when it changes more than [x]%: hmm maybe
- todo
