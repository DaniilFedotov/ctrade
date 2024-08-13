import sys
import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"backend.log", mode="a"),
            #logging.StreamHandler(stream=sys.stdout)
        ]
    )
