import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "group_chat_gfg"  # Use snake_case for variable names
        await self.channel_layer.group_add(
            self.room_group_name,  # Use snake_case for variable names
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,  # Use snake_case for variable names
            self.channel_name  # Use channel_name instead of channel_layer
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        await self.channel_layer.group_send(
            self.room_group_name,  # Use snake_case for variable names
            {
                "type": "send_message",  # Use snake_case for method names
                "message": message,
                "username": username,
            }
        )

    async def send_message(self, event):  # Use snake_case for method names
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))
