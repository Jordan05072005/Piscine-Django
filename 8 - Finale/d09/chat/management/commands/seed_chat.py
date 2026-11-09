from django.core.management.base import BaseCommand
from django.db import transaction
from chat.models import ChatRoom

CHATROOMS = ["general", "random", "help"]



class Command(BaseCommand):
    help = "Creates 3 users."

    @transaction.atomic
    def handle(self, *args, **options):
        for name in CHATROOMS:
            room, created = ChatRoom.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Chatroom created: {room.name}"))
            else:
                self.stdout.write(f"Chatroom already exists: {room.name}")
