import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

load_dotenv()
User = get_user_model()


class Command(BaseCommand):
    '''Создаёт админа по данным из .env файла.'''

    def handle(self, *args, **options):

        username = os.getenv('USERNAME_ADMIN')
        email = os.getenv('EMAIL_ADMIN')
        password = os.getenv('PASSWORD_ADMIN')

        if not User.objects.filter(username=username).exists():
            try:
                User.objects.create_superuser(
                    email=email, username=username,
                    password=password
                )
            except Exception:
                raise
        else:
            pass
