#['LINKUSDT', 'LINKETH', 'ETHUSDT'] 

import time, requests, math, threading, pyautogui, datetime, csv
import hashlib, base64, hmac, json
from urllib.parse import urljoin, urlencode
from pyautogui import Point
from pairs import TRIANGLES
from decimal import Decimal as D

#Zero fees
#Different pairs

SECRET_KEY = ''
KEY = ''
BASE_URL = 'https://api.binance.com'
headers = {
    'X-MBX-APIKEY': KEY
}

FEE = 0.001
input = 50
currencies = ['LINKUSDT', 'LINKETH', 'ETHUSDT']

def price(pair):
    r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={pair}")
    return r.json()['price']

def order(pair, side, quantity):
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': pair,
        'side': side,
        'type': 'MARKET',
        'quantity': quantity,
        'recvWindow': 60000,
        'timestamp': timestamp
    }
    query_string = urlencode(params)
    params['signature'] = hmac.new(SECRET_KEY.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BASE_URL, PATH)
    r = requests.post(url, headers=headers, params=params)
    print(r.json())
    return r.json()['fills'][0]['qty']

#Custom triangle for ['LINKUSDT', 'LINKETH', 'ETHUSDT']
class triangular():
    def __init__(self, pair1, pair2, pair3):
        self.pair1 = pair1
        self.pair2 = pair2
        self.pair3 = pair3
    
    def is_triangle(self):
        pair1 = float(price(self.pair1))
        pair2 = float(price(self.pair2))
        pair3 = float(price(self.pair3))
        print(50/pair1 * pair2 * pair3)
        if (50/pair1 * pair2 * pair3* 0.997) > 50:
            print("start")
            un = order('LINKUSDT', 'buy', round(50/pair1, 3))
            deux = order('LINKETH', 'sell', round(float(un)-0.04, 2))
            order('ETHUSDT', 'sell', round(float(deux)*pair2-0.00004, 5))


first = triangular('LINKUSDT', 'LINKETH', 'ETHUSDT')
while True:
    first.is_triangle()
    time.sleep(3)