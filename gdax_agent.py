import configparser
import time
import decimal

import gdax

from pushbullet import Pushbullet


class GDAX_Agent:
    def __init__(self, product):
        config = configparser.ConfigParser()
        config.read('./settings.ini')

        pushbullet_token = config['pushbullet']['api_key']
        self.pushbullet = Pushbullet(pushbullet_token)

        self.product = product
        self.pub_client = gdax.PublicClient()

        self.last_price = 0

    def __get_trade_info(self):
        response = self.pub_client.get_product_ticker(self.product)
        price = float(response['price'])
        bid = float(response['bid'])
        ask = float(response['ask'])
        return {'price': price, 'bid': bid, 'ask': ask}

    def update_and_push(self):
        info = self.__get_trade_info()
        title = '{0}: {1:.2f}'.format(self.product, info['price'])
        body = "Bid: {0:.2f}, Ask: {1:.2f}, Δ: {2:.2f}" \
                .format(info['bid'], info['ask'], self.last_price)
        self.pushbullet.push_note(title, body)
        self.last_price = info['price']

    def poll(self, interval):
        while True:
            self.update_and_push()
            time.sleep(interval)


if __name__ == "__main__":
    MINUTES = 60
    interval = 60 * MINUTES  # once an hour
    agent = GDAX_Agent('ETH-USD')  # other options BTC-USD/anything on GDAX
    agent.poll(interval)
