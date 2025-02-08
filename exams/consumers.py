import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MinimalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("MinimalChatConsumer: Connection attempt", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"message": "WebSocket Connected"}))
    
    async def disconnect(self, close_code):
        print("MinimalChatConsumer: Disconnected with code", close_code)
    
    async def receive(self, text_data):
        # Echo received data for now.
        await self.send(text_data=text_data)
