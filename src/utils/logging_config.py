import logging
import sys
from pathlib import Path

from utils.config import PROJECT_ROOT

def setup_logging():
    LOG_FILE = PROJECT_ROOT / 'bot.log'
    DEBUG_FILE = PROJECT_ROOT / 'debug.log'

    LOG_FILE.touch()
    DEBUG_FILE.touch()



    

    info_file_handler = logging.FileHandler(
        LOG_FILE,
        mode ='a',
        encoding ='utf-8')
    info_file_handler.setLevel(logging.INFO)
    
    debug_file_handler = logging.FileHandler(
        DEBUG_FILE,
        mode='a',
        encoding='utf-8')
    debug_file_handler.setLevel(logging.DEBUG)

    # console_handler = logging.StreamHandler(sys.stdout)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[info_file_handler, debug_file_handler],
        force=True 
    )

    logging.info("Logging initialised; file at %s", LOG_FILE)


