from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Replace 'admin' with your username
user = User.objects.get(username='admin')  # or another username
token, created = Token.objects.get_or_create(user=user)

print(token.key)  # This will print the token


class Command(BaseCommand):
    help = 'Generate token for a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
            token, created = Token.objects.get_or_create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Token for {username}: {token.key}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))
