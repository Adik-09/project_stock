from django.urls import re_path
from stock_app.consumers import StockConsumer  # Import your consumer

websocket_urlpatterns = [
    re_path(r'ws/stocks/$', StockConsumer.as_asgi()),  # Ensure this matches frontend
]