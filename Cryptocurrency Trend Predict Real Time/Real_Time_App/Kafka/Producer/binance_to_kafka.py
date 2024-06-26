import json
import websocket
from kafka import KafkaProducer
from binance.client import Client
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("../.env", override=True)
bootstrap_servers_ = os.getenv('BOOSTRAP_SERVERS')
socket_url = os.getenv('SOCKET_URL')

# Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers_,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Initialize Binance client
client = Client()

# Get exchange information and filter for symbols ending with 'USDT'
exchange_info = client.get_exchange_info()
symbols = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['symbol'].endswith('USDT')]

# Prepare WebSocket stream assets
assets = [symbol.lower() + '@kline_1m' for symbol in symbols]
relevant_assets = '/'.join(assets)


def manipulate(data):
    value_data = data['k']
    price, sym = value_data['c'], value_data['s']
    event_time = pd.to_datetime(data['E'], unit='ms').isoformat()
    return {'price': price, 'symbol': sym, 'event_time': event_time}


def on_message(ws, message):
    json_message = json.loads(message)
    if 'data' in json_message:
        data = json_message['data']
        if 'k' in data:
            manipulated_data = manipulate(data)
            producer.send('crypto-prices', value=manipulated_data)


def on_error(ws_, error):
    print(f"Error: {error}")
    ws_.close()


def on_open(_):
    print("### WebSocket opened ###")


# WebSocket URL
socket = f"{socket_url}{relevant_assets}"

# Start WebSocket connection
ws = websocket.WebSocketApp(
    socket,
    on_message=on_message,
    on_error=on_error,
    on_open=on_open
)
ws.run_forever()
