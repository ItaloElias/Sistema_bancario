from decimal import Decimal
from transacoes import Historico

class Conta:
    """
    Classe que representa uma conta bancária genérica.
    """
    def __init__(self, cliente, numero, agencia):
        """
        Inicializa uma conta com saldo zero, número, agência, cliente e histórico.
        :param cliente: Cliente titular da conta.
        :param numero: Número da conta.
        :param agencia: Número da agência.
        """
        self.saldo = Decimal("0.00")
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def depositar(self, valor):
        """
        Realiza um depósito na conta.
        :param valor: Valor a ser depositado.
        :return: True se realizado, False caso contrário.
        """
        valor = Decimal(str(valor))
        if valor > 0:
            self.saldo += valor
            return True
        return False

    def sacar(self, valor):
        """
        Realiza um saque na conta.
        :param valor: Valor a ser sacado.
        :return: True se realizado, False caso contrário.
        """
        valor = Decimal(str(valor))
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            return True
        return False

class ContaCorrente(Conta):
    """
    Classe que representa uma conta corrente, com limite de valor e de saques.
    """
    def __init__(self, cliente, numero, agencia, limite=Decimal("500.00"), limite_saques=3):
        """
        Inicializa uma conta corrente.
        :param cliente: Cliente titular da conta.
        :param numero: Número da conta.
        :param agencia: Número da agência.
        :param limite: Limite de valor por saque.
        :param limite_saques: Limite de saques diários.
        """
        super().__init__(cliente, numero, agencia)
        self.limite = Decimal(str(limite))
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        """
        Realiza um saque na conta corrente, considerando limites.
        :param valor: Valor a ser sacado.
        :return: True se realizado, ou string indicando motivo da recusa.
        """
        valor = Decimal(str(valor))
        if self.numero_saques >= self.limite_saques:
            return "limite_saques"
        if valor > self.limite:
            return "limite_valor"
        if super().sacar(valor):
            self.numero_saques += 1
            return True
        else:
            return "saldo"

class Cliente:
    """
    Classe base para clientes do banco.
    """
    def __init__(self, endereco):
        """
        Inicializa um cliente com endereço e lista de contas.
        :param endereco: Endereço do cliente.
        """
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        """
        Adiciona uma conta à lista de contas do cliente.
        :param conta: Conta a ser adicionada.
        """
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        """
        Realiza uma transação em uma conta do cliente.
        :param conta: Conta a ser movimentada.
        :param transacao: Instância de uma transação.
        :return: Resultado da transação.
        """
        return transacao.registrar(conta)

class PessoaFisica(Cliente):
    """
    Classe que representa um cliente pessoa física.
    """
    def __init__(self, nome, cpf, data_nascimento, endereco):
        """
        Inicializa uma pessoa física.
        :param nome: Nome completo.
        :param cpf: CPF do cliente.
        :param data_nascimento: Data de nascimento.
        :param endereco: Endereço do cliente.
        """
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento