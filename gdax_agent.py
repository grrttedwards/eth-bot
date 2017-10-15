import configparser
import time
import gdax
from pushbullet import Pushbullet


class GDAX_Agent:
    """Interact and read trade information from GDAX"""
    def __init__(self, product):
        config = configparser.ConfigParser()
        config.read('./settings.ini')

        pushbullet_token = config['pushbullet']['api_key']
        self.pushbullet = Pushbullet(pushbullet_token)
        self.product = product
        self.pub_client = gdax.PublicClient()
        self.last_price = 0

    def __percent_change(self, price):
        if self.last_price:
            return round((price - self.last_price) / self.last_price * 100, 2)
        return 0

    def __get_trade_info(self):
        response = self.pub_client.get_product_ticker(self.product)
        price = float(response['price'])
        bid = float(response['bid'])
        ask = float(response['ask'])
        return {'price': price, 'bid': bid, 'ask': ask}

    def update_and_push(self):
        info = self.__get_trade_info()
        price = info['price']
        bid = info['bid']
        ask = info['ask']
        delta_price = price - self.last_price
        delta_percent = self.__percent_change(price)

        title = f'{self.product}: ${price:.2f}'
        body = f"Bid: {bid:.2f}, Ask: {ask:.2f}, $Δ: {delta_price:.2f}, %Δ: {delta_percent:.2f}"
        self.pushbullet.push_note(title, body)
        self.last_price = price

    def poll(self, interval):
        while True:
            self.update_and_push()
            time.sleep(5)


if __name__ == "__main__":
    MINUTES = 60
    interval = 60 * MINUTES  # once an hour
    agent = GDAX_Agent('ETH-USD')  # other options BTC-USD/anything on GDAX
    agent.poll(interval)
