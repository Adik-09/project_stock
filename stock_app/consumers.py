import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "stock_data_updates"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    print(" WebSocket Connected")  # Debugging line


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print("WebSocket Disconnected")

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({"response": "Data received"}))

    async def stock_update(self, event):
        stock_data = event["stock_data"]  # Get the stock data JSON
        top_loser = event["top_loser"]
        top_gainer = event["top_gainer"]
        await self.send(text_data=json.dumps({"update": json.loads(stock_data),
                                              "top_loser":json.loads(top_loser),
                                              "top_gainer":json.loads(top_gainer),
                                              }))  # Send the real data

