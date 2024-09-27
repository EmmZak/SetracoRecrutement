import os
import shutil
import zipfile
import logging
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from tempfile import TemporaryDirectory

logger = logging.getLogger('backup')

class Command(BaseCommand):
    help = 'Restores the database and media files from a backup.'

    def add_arguments(self, parser):
        parser.add_argument('backup_zip', type=str,
                            help="Path to the backup zip file.")

    def handle(self, *args, **kwargs):
        backup_zip = kwargs['backup_zip']

        if not os.path.exists(backup_zip):
            raise CommandError(f'The file {backup_zip} does not exist.')

        logger.info(f'Starting restore process from {backup_zip}...')
        self.restore_from_zip(backup_zip)
        logger.info('Restore process completed.')

    def restore_from_zip(self, backup_zip):
        try:
            # Create a temporary directory to extract the zip contents
            with TemporaryDirectory() as temp_dir:
                # Extract the zip file to the temporary directory
                with zipfile.ZipFile(backup_zip, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                logger.info(f'Extracted backup to {temp_dir}')

                # 1. Restore the database from dump.json
                dump_file = os.path.join(temp_dir, 'dump.json')
                if os.path.exists(dump_file):
                    call_command('loaddata', dump_file)
                    logger.info(
                        f'Database restored successfully from {dump_file}')
                else:
                    raise CommandError(
                        f'dump.json not found in the backup zip.')

                # 2. Restore media files to MEDIA_ROOT
                media_backup_dir = os.path.join(temp_dir, 'profile_files')
                media_root = settings.MEDIA_ROOT

                if os.path.exists(media_backup_dir):
                    # Copy media files back to MEDIA_ROOT
                    shutil.copytree(media_backup_dir,
                                    media_root, dirs_exist_ok=True)
                    logger.info(
                        f'Media files restored successfully to {media_root}')
                else:
                    logger.warning(f'No media files found in the backup zip.')

        except Exception as e:
            logger.error(f'Error during restore process: {e}')
            raise CommandError(f'Error during restore: {e}')
