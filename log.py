import sys
import logging

formatter = logging.Formatter('====> %(asctime)s | %(name)s | %(levelname)s | %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler('roll.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

logging.basicConfig(
        handlers = [stream_handler,file_handler],
        level=logging.DEBUG,
    )
logging.getLogger("httpx").setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

