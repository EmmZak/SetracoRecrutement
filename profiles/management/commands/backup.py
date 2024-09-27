from SetracoRecrutement.logger import Logger
from django.core.management import call_command
from datetime import datetime
from django.conf import settings  # Import settings
import shutil
import os
import zipfile
from tempfile import TemporaryDirectory
import logging
from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger('backup')

class Command(BaseCommand):
    help = "Backup db and files"

    def handle(self, *args, **options):
        try:
            # Get the backup directory from settings
            backup_dir = settings.BACKUP_DIR
            os.makedirs(backup_dir, exist_ok=True)

            # Dynamic filename for the zip
            zip_filename = f'backup_{datetime.now().strftime("%d_%m_%Y")}.zip'
            zip_filepath = os.path.join(backup_dir, zip_filename)

            # Create a temporary directory to hold dump and media files
            with TemporaryDirectory() as temp_dir:
                # 1. Backup the database
                dump_file = os.path.join(temp_dir, 'dump.json')
                with open(dump_file, 'w') as f:
                    call_command('dumpdata', stdout=f)
                logger.info(f'Database dumped to {dump_file}')

                # 2. Backup the media files
                media_root = settings.MEDIA_ROOT  # Get MEDIA_ROOT from settings
                backup_media_dir = os.path.join(temp_dir, 'profile_files')

                if os.path.exists(media_root):
                    shutil.copytree(media_root, backup_media_dir)
                    logger.info(f'Media files copied to {backup_media_dir}')
                else:
                    logger.warning(
                        f'Media root directory "{media_root}" does not exist.')

                # 3. Create a zip file containing dump.json and profile_files
                with zipfile.ZipFile(zip_filepath, 'w') as backup_zip:
                    # Add the dump.json file
                    backup_zip.write(dump_file, arcname='dump.json')

                    # Add all media files (recursively)
                    for root, dirs, files in os.walk(backup_media_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            backup_zip.write(file_path, arcname=arcname)

                logger.info(f'Backup successfully zipped to {zip_filepath}')

        except Exception as e:
            logger.error(f'Error during backup process: {e}')
