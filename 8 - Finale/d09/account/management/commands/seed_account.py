from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings




USERS = [
    {"username": "jguaglio", "password": 'password'},
    {"username": "testeur", "password": 'password'},
    {"username": "john", "password": 'password'},
]

USERS_ADMIN = [
    {"username": settings.DATA_ENV["SYSTEM_USERNAME"], "password": settings.DATA_ENV["SYSTEM_PASSWORD"]},
]

class Command(BaseCommand):
    help = "Creates 3 users."

    @transaction.atomic
    def handle(self, *args, **options):
        for data in USERS:
            user, created = User.objects.get_or_create(username=data["username"])
            if created:
                user.set_password(data["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User created: {user.username}"))
            else:
                self.stdout.write(f"User already exists: {user.username}")
        for data in USERS_ADMIN:
            if not User.objects.filter(username=data["username"]).exists():
                user = User.objects.create_superuser(username=data["username"], password=data["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User created: {user.username}"))
        self.stdout.write(self.style.SUCCESS(
            f"Done. User password: password"
        ))
