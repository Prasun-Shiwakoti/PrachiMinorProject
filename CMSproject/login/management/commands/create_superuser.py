# create_superuser.py

from django.core.management import BaseCommand
from core.models import CustomUser

class Command(BaseCommand):
    help = 'Create a superuser manually'

    def handle(self, *args, **options):
        # Replace these values with the desired information
        email = 'superuser@example.com'
        password = 'admin/'
        usertype = 'admin'

        # Create a superuser instance
        superuser = CustomUser.objects.create(email=email, password=password, usertype=usertype)

        # Set superuser attributes
        superuser.is_staff = True
        superuser.is_superuser = True

        # Save the superuser to the database
        superuser.save()

        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
