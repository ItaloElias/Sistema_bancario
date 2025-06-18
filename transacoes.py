from decimal import Decimal
import datetime
from abc import ABC, abstractmethod

class Historico:
    """
    Classe responsável por armazenar o histórico de transações de uma conta.
    """
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        """
        Adiciona uma transação ao histórico.
        :param transacao: Instância de uma transação (Deposito ou Saque).
        """
        self.transacoes.append(transacao)

class Transacao(ABC):
    """
    Classe abstrata base para transações bancárias.
    """
    @abstractmethod
    def registrar(self, conta):
        """
        Executa a transação na conta informada.
        :param conta: Conta na qual a transação será realizada.
        """
        pass

class Deposito(Transacao):
    """
    Classe que representa uma transação de depósito.
    """
    def __init__(self, valor):
        """
        Inicializa um depósito com valor, data e hora.
        :param valor: Valor a ser depositado.
        """
        self.valor = Decimal(str(valor))
        agora = datetime.datetime.now()
        self.data = agora.strftime("%d/%m/%Y")
        self.hora = agora.strftime("%H:%M:%S")

    def registrar(self, conta):
        """
        Realiza o depósito na conta e registra no histórico se bem-sucedido.
        :param conta: Conta a receber o depósito.
        :return: True se realizado, False caso contrário.
        """
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False

class Saque(Transacao):
    """
    Classe que representa uma transação de saque.
    """
    def __init__(self, valor):
        """
        Inicializa um saque com valor, data e hora.
        :param valor: Valor a ser sacado.
        """
        self.valor = Decimal(str(valor))
        agora = datetime.datetime.now()
        self.data = agora.strftime("%d/%m/%Y")
        self.hora = agora.strftime("%H:%M:%S")

    def registrar(self, conta):
        """
        Realiza o saque na conta e registra no histórico se bem-sucedido.
        :param conta: Conta a ser debitada.
        :return: True se realizado, False caso contrário.
        """
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            return True