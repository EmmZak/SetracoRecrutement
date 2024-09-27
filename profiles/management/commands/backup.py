from django.core.management import BaseCommand
from ...services import backup


class Command(BaseCommand):
    help = "Backup db and files"

    def handle(self, *args, **options):
        backup()
