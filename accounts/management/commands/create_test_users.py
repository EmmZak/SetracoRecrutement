from django.core.management import BaseCommand
from ...services import create_test_users


class Command(BaseCommand):
    help = "Creates read only default permission groups for users"

    def handle(self, *args, **options):
        print("handle createion")
        create_test_users()
