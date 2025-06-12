import datetime
import requests
from abc import ABC, abstractmethod
from dados import carregar_usuarios, salvar_usuarios, carregar_contas, salvar_contas

LIMITE_SAQUES = 3
AGENCIA = "0001"

# --- CLASSES DO SISTEMA ---

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
            print("Depósito realizado com sucesso!")
        else:
            print("Operação falhou! Valor inválido.")

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            print("Saque realizado com sucesso!")
        else:
            print("Operação falhou! Verifique saldo, limite ou número de saques.")

class Conta:
    def __init__(self, cliente, numero, agencia=AGENCIA):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        return False

    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=LIMITE_SAQUES):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques >= self.limite_saques:
            print("Limite de saques excedido.")
            return False
        
        self.numero_saques += 1
        saques_restantes = self.limite_saques - self.numero_saques
        print(f"Saques restantes: {saques_restantes}")
        return True 

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

# --- FUNÇÕES AUXILIARES ---

usuarios = carregar_usuarios()
contas = carregar_contas()

def buscar_conta_por_numero(contas, numero_conta):
    for conta in contas:
        if str(conta.numero) == str(numero_conta):
            return conta
    return None

def buscar_cliente_por_cpf(usuarios, cpf):
    for cliente in usuarios:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None

def depositar_na_conta(conta):
    valor = float(input("Valor do depósito: "))
    transacao = Deposito(valor)
    conta.cliente.realizar_transacao(conta, transacao)
    salvar_contas(contas)

def sacar_da_conta(conta):
    valor = float(input("Valor do saque: "))
    transacao = Saque(valor)
    conta.cliente.realizar_transacao(conta, transacao)
    salvar_contas(contas)

def exibir_extrato_da_conta(conta):
    print("\n========== EXTRATO ==========")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for t in conta.historico.transacoes:
            tipo = t.__class__.__name__
            sinal = "+" if tipo == "Deposito" else "-"
            print(f"{tipo}: {sinal}R$ {t.valor:.2f}")
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("=============================")

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

def validar_data(data):
    try:
        datetime.datetime.strptime(data, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def buscar_endereco_por_cep(cep):
    cep = ''.join(filter(str.isdigit, cep))
    if len(cep) != 8:
        print("CEP inválido! Deve conter 8 dígitos.")
        return None
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        resposta = requests.get(url, timeout=5)
        dados = resposta.json()
        if "erro" in dados:
            print("CEP não encontrado.")
            return None
        endereco = f"{dados['logradouro']}, {dados['bairro']} - {dados['localidade']}/{dados['uf']}"
        return endereco
    except Exception as e:
        print("Erro ao buscar o endereço:", e)
        return None

def criar_usuario(usuarios):
    while True:
        cpf = input("Informe o CPF (somente números): ")
        if not validar_cpf(cpf):
            print("CPF inválido! Tente novamente.")
            continue
        if buscar_cliente_por_cpf(usuarios, cpf):
            print("Já existe usuário com esse CPF!")
            return
        break

    nome = input("Nome completo: ")
    while True:
        nascimento = input("Data de nascimento (dd-mm-aaaa): ")
        if not validar_data(nascimento):
            print("Data de nascimento inválida! Tente novamente.")
            continue
        break

    while True:
        cep = input("Informe o CEP (somente números): ")
        endereco_base = buscar_endereco_por_cep(cep)
        if endereco_base:
            print(f"Endereço encontrado: {endereco_base}")
            numero = input("Informe o número da residência: ")
            endereco = f"{endereco_base}, Nº {numero}"
            break

    cliente = PessoaFisica(nome, cpf, nascimento, endereco)
    usuarios.append(cliente)
    salvar_usuarios(usuarios)
    print("Usuário criado com sucesso!")

def criar_conta(contas, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    cliente = buscar_cliente_por_cpf(usuarios, cpf)
    if not cliente:
        print("Usuário não encontrado!")
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    salvar_contas(contas)
    print(f"Conta criada com sucesso! Número da conta: {numero_conta}")

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for conta in contas:
        cliente = conta.cliente
        print(f"Agência: {conta.agencia}, Conta: {conta.numero}, Titular: {cliente.nome}")

def apagar_usuario(usuarios, contas, cpf):
    for conta in contas:
        if conta.cliente.cpf == cpf:
            print("Não é possível apagar o usuário: existe uma conta associada a este CPF.")
            return False
    # Remove usuário se não houver conta
    for i, usuario in enumerate(usuarios):
        if usuario.cpf == cpf:
            del usuarios[i]
            salvar_usuarios(usuarios)
            print("Usuário apagado com sucesso.")
            return True
    print("Usuário não encontrado.")
    return False

def apagar_conta(contas, conta):
    contas.remove(conta)
    conta.cliente.contas.remove(conta)
    salvar_contas(contas)
    print("Conta apagada com sucesso!")

def menu_conta(conta):
    primeira_vez = True    
    while True:
        if primeira_vez:
            print(f"\nBem-vindo, {conta.cliente.nome}! (Conta: {conta.numero})")
            primeira_vez = False    
        print("""
[d] Depositar
[s] Sacar
[e] Extrato
[ac] Apagar Conta
[voltar] Voltar ao menu inicial
""")
        opcao = input("=> ").lower()
        if opcao == "d":
            depositar_na_conta(conta)
        elif opcao == "s":
            sacar_da_conta(conta)
        elif opcao == "e":
            exibir_extrato_da_conta(conta)
        elif opcao == "ac":
            apagar_conta(contas, conta)
            break
        elif opcao == "voltar":
            break
        else:
            print("Opção inválida!")

def menu_inicial():
    while True:
        print("""
[ec] Entrar na Conta
[nu] Novo Usuário
[nc] Nova Conta
[lc] Listar Contas
[au] Apagar Usuário
[q] Sair
""")
        opcao = input("=> ").lower()
        if opcao == "ec":
            numero_conta = input("Informe o número da conta: ")
            conta = buscar_conta_por_numero(contas, numero_conta)
            if not conta:
                print("Conta não encontrada!")
            else:
                menu_conta(conta)
        elif opcao == "nu":
            criar_usuario(usuarios)
        elif opcao == "nc":
            criar_conta(contas, usuarios)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "au":
            cpf = input("Informe o CPF do usuário a ser apagado: ")
            apagar_usuario(usuarios, contas, cpf)
        elif opcao == "q":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_inicial()