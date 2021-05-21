from time import time

import load_balance
from config import logging

logger = logging.getLogger("topaz_test")


def main():
    """Processamento principal."""
    time_start = time()
    logger.info("Balanceamento de carga foi iniciado")
    try:
        load_balance.run()
    except BaseException as error:
        logger.error(error)
    execution_time = "{:.3f}".format(time() - time_start)
    logger.info(f"Execução finalizada em {execution_time}s")


if __name__ == "__main__":
    main()
