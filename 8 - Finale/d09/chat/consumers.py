import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage, ChatRoom
from django.contrib.auth.models import User
from django.conf import settings

class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room_name = None
        self.group_name = None
        self.room = None


    async def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'chat_{self.room_name}'
        self.room = await self.get_room()
        if self.room is None: await self.close(); return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await database_sync_to_async(self.room.users.add)(self.user)

        messages = await self.getFirstMessages()

        await self.chat_message({
            'usernames': [message.author.username for message in messages],
            'messages': [message.content for message in messages],
        })

        usernames = await self.get_usernames()
        await self.channel_layer.group_send(self.group_name, {
            'type': 'user.update',
            'users': usernames,
        })

        # Message systeme (admin)
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat.message',
            'usernames': [settings.DATA_ENV["SYSTEM_USERNAME"]],
            'messages': [f'{self.user.username} has joined the chat'],
        })


    async def disconnect(self, code):
        if self.room is None: return
        await database_sync_to_async(self.room.users.remove)(self.user)

        usernames = await self.get_usernames()
        await self.channel_layer.group_send(self.group_name, {
            'type': 'user.update',
            'users': usernames,
        })

        # Message systeme (admin)
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat.message',
            'usernames': [settings.DATA_ENV["SYSTEM_USERNAME"]],
            'messages': [f'{self.user.username} has left the chat'],
        })
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


    async def receive(self, text_data):
        data = json.loads(text_data)

        # Envoye aux instances de ChatConsumer sur chat_message pour partager les message reçu
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat.message',
            'usernames': [self.user.username],
            'messages': [data['message']],
        })
        # Envoye sur save_message
        await self.save_message({
            'type': 'save.message',
            'username': self.user.username,
            'message': data['message'],
        })


    async def chat_message(self, event):
        # Envoye sur le socket (chat.js) de celui qui a init la connection pour afficher le messages
        await self.send(text_data=json.dumps({
            'username': event['usernames'],
            'messages': event['messages'],
            'system': [username == settings.DATA_ENV["SYSTEM_USERNAME"] for username in event['usernames']],
            'type': 'chat_message',
        }))


    async def user_update(self, event):
        await self.send(text_data=json.dumps({
            'users': event['users'],
            'type': 'connection',
        }))


    @database_sync_to_async
    def save_message(self, content):
        message = ChatMessage.objects.create(
            content=content['message'],
            author=User.objects.get(username=content['username']),
            room=ChatRoom.objects.get(name=self.room_name)
        )
        message.save()

    @database_sync_to_async
    def get_room(self):
        return ChatRoom.objects.filter(name=self.room_name).first()

    @database_sync_to_async
    def get_usernames(self):
        return list(self.room.users.values_list('username', flat=True))

    @database_sync_to_async
    def getFirstMessages(self):
        return list(reversed(
            ChatMessage.objects
            .filter(room=self.room)
            .select_related('author')
            .order_by('-date')[:3]
        ))



