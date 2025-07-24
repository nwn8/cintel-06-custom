import requests
import json
from datetime import datetime


U_value="&apikey=6bf3bdff97a14db19bdea24ba1900629"




def get_price(ticker):

    ticker_symbol=ticker

    url=f"https://api.twelvedata.com/price?symbol={ticker_symbol}{U_value}"
    response = requests.get(url)

    #print(f"Status Code: {response.status_code}")
    #print(f"Response Body: {response.json()}")

    price=response.json()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    price_dict = {'price' : float(price['price']), 'timestamp':timestamp}

    #print(appl_dict)
    return price_dict