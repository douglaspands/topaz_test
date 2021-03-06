import sys
from time import time

from config import FILE_INPUT, FILE_OUTPUT, logging
from server_manager import ServerManager

logger = logging.getLogger("topaz_test")


def main() -> int:
    """Processamento principal.

    Returns:
        int: 0 = Resultado OK.
    """
    return_code = 0
    time_start = time()
    logger.info("Balanceamento de carga foi iniciado")
    try:
        ttask = None
        umax = None
        server_manager = None
        with open(FILE_OUTPUT, "w") as file_output:
            with open(FILE_INPUT, "r") as file_input:
                for num, line in enumerate(file_input):
                    if num == 0:
                        ttask = int(line)
                        continue
                    elif num == 1:
                        umax = int(line)
                        server_manager = ServerManager(ttask=ttask, umax=umax)
                        continue
                    else:
                        if line.strip().isdigit():
                            report = server_manager.new_task_for_each_user(
                                amount_users=int(line)
                            )
                            file_output.write(f"{report}\n")
            if server_manager:
                while server_manager.has_busy_server:
                    report = server_manager.use_report
                    file_output.write(f"{report}\n")
                file_output.write(str(server_manager.amount))
    except BaseException as error:
        logger.error(error, exc_info=True)
        return_code = 1
    execution_time = "{:.3f}".format(time() - time_start)
    logger.info(f"Execução finalizada em {execution_time}s")
    return return_code


def init():
    if __name__ == "__main__":
        sys.exit(main())


init()
