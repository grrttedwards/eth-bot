import configparser
import time
import gdax
from pushbullet import Pushbullet


class GDAX_Agent:
    """Interact and read trade information from GDAX"""
    def __init__(self, *products):
        config = configparser.ConfigParser()
        config.read('./settings.ini')

        pushbullet_token = config['pushbullet']['api_key']
        self.pushbullets = {product: Pushbullet(pushbullet_token) for product in products}
        self.products = products
        self.pub_client = gdax.PublicClient()
        self.last_prices = {product: 0.0 for product in products}

    def __percent_change(self, price, last_price):
        if last_price:
            return round((price - last_price) / last_price * 100, 2)
        return 0

    def __get_deltas(self, price, product):
        last_price = self.last_prices[product]
        delta_price = price - last_price
        delta_percent = self.__percent_change(price, last_price)
        return delta_price, delta_percent

    def __get_trade_info(self, product):
        response = self.pub_client.get_product_ticker(product)
        price = float(response['price'])
        bid = float(response['bid'])
        ask = float(response['ask'])
        return price, bid, ask

    def update_and_push(self, product):
        price, bid, ask = self.__get_trade_info(product)
        delta_price, delta_percent = self.__get_deltas(price, product)

        title = f'{product}: ${price:.2f}'
        body = f"Bid: {bid:.2f}, Ask: {ask:.2f}, $Δ: {delta_price:.2f}, %Δ: {delta_percent:.2f}"
        self.pushbullets[product].push_note(title, body)
        self.last_prices[product] = price

    def poll(self, interval):
        while True:
            for product in self.products:
                self.update_and_push(product)
            time.sleep(interval)


if __name__ == '__main__':
    MINUTES = 60
    interval = 60 * MINUTES  # once an hour
    agent = GDAX_Agent('ETH-USD', 'BTC-USD')  # other options BTC-USD/anything on GDAX
    agent.poll(interval)
