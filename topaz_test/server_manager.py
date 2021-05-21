import logging
from typing import List, Optional
from decimal import Decimal
from config import TICK_COST

logger = logging.getLogger(__name__)


class User:
    def __init__(self, ttask: int):
        """Usuario que solicitou a tarefa.

        Args:
            ttask (int): Quantidade de ticks da tarefa.
        """
        self.left_ticks = ttask

    def remove_tick(self) -> int:
        """Remove tick de execução.

        Returns:
            int: Retorna a quantidade restante de ticks.
        """
        if not self.left_ticks:
            return 0
        self.left_ticks -= 1
        return self.left_ticks


class Server:
    def __init__(self, umax: int):
        """Servidor/Cluster.

        Args:
            umax (int): Quantidade maxima de usuarios.
        """
        self.left_ticks = 0
        self.limit_users = umax
        self.users: List[User] = []

    @property
    def has_space(self) -> bool:
        """Tem espaço para mais usuarios.

        Returns:
            bool: 'True' se tiver.
        """
        return len(self.users) < self.limit_users

    def add_user(self, ttask: int):
        """Adicionar usuario.

        Args:
            ttask (int): Quantidade de ticks da tarefa.
        """
        self.users.append(User(ttask=ttask))
        self.left_ticks += ttask

    def remove_tick(self) -> int:
        """Remove tick de execução.

        Returns:
            int: Retorna a quantidade restante de ticks.
        """
        if not self.left_ticks:
            return 0
        remove_index = []
        for i in range(len(self.users)):
            self.left_ticks -= 1
            has_tick = self.users[i].remove_tick()
            if not has_tick:
                remove_index.append(i)
        [self.users.pop(idx) for idx in reversed(remove_index)]
        return self.left_ticks


class ServerManager:
    def __init__(self, ttask: int, umax: int):
        """Gerenciador de servidor.

        Args:
            ttask (int): Ticks de uma tarefa.
            umax (int): Quantidade maxima de usuarios simultaneos.

        Raises:
            Exception: Quantidade de ticks precisa ser maior ou igual a 1 e menor ou igual a 10.
            Exception: Quantidade de usuarios precisa ser maior ou igual a 1 e menor ou igual a 10.
        """
        if not isinstance(ttask, int) or not (1 <= ttask <= 10):
            raise Exception(
                "Argumento 'ttask' precisa ser do tipo 'int' e maior ou igual a 1 e menor ou igual a 10."
            )
        if not isinstance(umax, int) or not (1 <= umax <= 10):
            raise Exception(
                "Argumento 'umax' precisa ser do tipo 'int' e maior ou igual a 1 e menor ou igual a 10."
            )
        self.ttask = ttask
        self.umax = umax
        self.servers: List[Server] = []
        self.amount: Decimal = Decimal('0')

    def new_task_for_each_user(self, amount_users: int) -> List[int]:
        """Nova tarefa para cada usuario.

        Args:
            amount_users (int): Quantidade de usuarios.

        Raises:
            Exception: 'amount_users' não é do tipo 'int'

        Returns:
            List[int]: Lista de usuarios para cada servidor em uso.
        """
        if not isinstance(amount_users, int):
            raise Exception("Argumento 'amount_users' precisa ser do tipo 'int'.")
        self._remove_tick()
        [self._add_task() for i in range(amount_users)]
        return self._calc_and_report()

    @property
    def use_report(self) -> str:
        """Gera relatorio do uso dos servidores.

        Returns:
            str: Lista de quantidade de usuarios por servidor.
        """
        self._remove_tick()
        return self._calc_and_report()

    @property
    def has_busy_server(self) -> bool:
        """Tem servidores ocupados.

        Returns:
            bool: 'True' se tiver.
        """
        return len(self.servers) != 0

    def _add_task(self):
        """Adiciona tarefas novas e retorna o ID do usuario"""
        server: Optional[Server] = None
        for i in range(len(self.servers)):
            if self.servers[i].has_space:
                server = self.servers[i]
                break
        if server:
            server.add_user(ttask=self.ttask)
        else:
            server = Server(umax=self.umax)
            server.add_user(ttask=self.ttask)
            self.servers.append(server)

    def _calc_and_report(self) -> str:
        """Calcula valor total de uso dos servidores e gera relatorio.

        Returns:
            str: Retorna o relatorio.
        """
        self.amount = self.amount + (len(self.servers) * TICK_COST)
        return ",".join([str(len(s.users)) for s in self.servers]) or "0"

    def _remove_tick(self):
        """Remove tick de execução"""
        remove_index = []
        for i in range(len(self.servers)):
            has_tick = self.servers[i].remove_tick()
            if not has_tick:
                remove_index.append(i)
        [self.servers.pop(idx) for idx in reversed(remove_index)]


__all__ = ("ServerManager",)
