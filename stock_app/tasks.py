from celery import shared_task
import yfinance as yf
from django.core.cache import cache
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@shared_task
def update_stock_data():
    tickers = [
        "AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "NVDA", "META", 
        "JPM", "NFLX", "V", "WMT", "KO", "PEP", "INTC", "PYPL"
    ]

    stock_data = []

    data = yf.download(tickers, period="3d")

    if not data.empty:
        for tic in tickers:
            try:
                prev_close = data["Close"][tic].iloc[-2]  
                current_price = data["Close"][tic].iloc[-1]  
                change = current_price - prev_close
                percent_change = (change / prev_close) * 100

                stock_data.append({
                    "ticker": tic,
                    "Oprice": round(data["Open"][tic].iloc[-1], 2),
                    "Cprice": round(current_price, 2),
                    "change": round(change, 2),
                    "percent_change": round(percent_change, 2),
                    "volume": int(data["Volume"][tic].iloc[-1])
                })
            except KeyError:
                print(f"Skipping {tic}: Data not available")

    sorted_data = sorted(stock_data, key=lambda x: x['change'])
    top_loser = sorted_data[:3]
    top_gainer = sorted_data[-3:]

    # Send data via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
    "stock_data_updates",
    {   
        "type": "stock_update",  # Match consumers.py function name
        "stock_data": json.dumps(stock_data),
        "top_loser":json.dumps(top_loser),
        "top_gainer":json.dumps(top_gainer),
    }
    )

    print("Message Sent to WebSocket!")  # Debugging

    return "Stock data updated successfully!"
