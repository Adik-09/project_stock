import yfinance as yf
from django.shortcuts import render
from django.core.cache import cache
import random

def stock_list(request):
    tickers = [
        "AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "NVDA", "META", 
        "JPM", "NFLX", "V", "WMT", "KO", "PEP", "INTC", "PYPL"
    ]

    return render(request, 'show_stock.html', {
        "tickers": random.sample(tickers, 5),
    })

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io,base64
import seaborn as sns
import pandas as pd

def stock_chart(request, stock_name):
    stock_obj = yf.Ticker(stock_name)

    cache_key = f"stock_data_{stock_name}" 
    data = cache.get(cache_key)  
    
    if data is None or not isinstance(data, pd.DataFrame) or data.empty:
        data = stock_obj.history(period="7d")
        if not data.empty:  
            cache.set(cache_key, data, timeout=30)

    if data.empty:
        return render(request, 'show_chart.html', {'error': 'No data available for this stock.'})

    sns.set_style("darkgrid")  
    plt.figure(figsize=(12, 6))


    plt.plot(data.index, data['Close'], marker='o', linestyle='-', color='#ff5733', markersize=6, markerfacecolor='yellow', linewidth=2.5, alpha=0.85, label=f'{stock_name} Price')
    plt.xlabel('Date', fontsize=12, fontweight='bold', color='white')
    plt.ylabel('Stock Price (₹)', fontsize=12, fontweight='bold', color='white')
    plt.xticks(rotation=45, color='white')
    plt.yticks(color='white')
    plt.legend(fontsize=10, loc='upper left', facecolor='black', edgecolor='white', labelcolor='white')
    plt.gca().set_facecolor('#1c1c1c')  
    plt.gcf().set_facecolor('#1c1c1c')  

    buf = io.BytesIO()
    plt.savefig(buf, format='jpg', bbox_inches='tight', facecolor='#1c1c1c')  
    plt.close()

    graph_image = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render(request, 'show_chart.html', {'graph_image': graph_image})
