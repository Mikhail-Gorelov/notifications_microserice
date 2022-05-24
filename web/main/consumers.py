from asgiref.sync import async_to_sync
from django.conf import settings
from channels.generic.websocket import WebsocketConsumer


class NotificationsConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "notifications",
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "notifications",
            self.channel_name
        )

    def email_notification(self, event: dict):
        print(event)
        data = event.get('data')
        print('hello', data)
        self.send_json(content=data)
