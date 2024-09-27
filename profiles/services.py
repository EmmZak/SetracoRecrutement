from SetracoRecrutement.logger import Logger

logger = Logger('backup')


def backup():
    logger.info("Backup start")
    try:
        logger.info("DB backup")

        logger.info("Files backup")
    except Exception as e:
        logger.error(f"Error while backing up {e}")
    logger.info("Backup done")



