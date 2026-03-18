import logging

def config_log(level=logging.INFO):
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )