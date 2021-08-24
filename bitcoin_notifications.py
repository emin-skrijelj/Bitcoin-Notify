import requests
import time
from datetime import datetime

bitcoin_api_url = 'https://blockchain.info/ticker'
webhooks_url = 'https://maker.ifttt.com/trigger/bitcoin_price_update/with/key/dtdm3uKejIiP9db6Jsd9ei'

def get_latest_bitcoin_price():
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    return float(response_json['USD']['buy'])

def post_ifttt_webhook(event, value):
    data = {'value1': value}
    ifttt_event_url = webhooks_url.format(event)
    requests.post(ifttt_event_url, json=data)


def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    return '<br>'.join(rows)

bitcoin_emergency_price = 45000

def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date':date, 'price':price})

        if price < bitcoin_emergency_price:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            bitcoin_history = []
        
        time.sleep(45)



time.sleep(5*60)


if __name__ == '__main__':
    main()