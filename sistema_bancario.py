import datetime
from decimal import Decimal, ROUND_HALF_UP
from modelos import Conta, ContaCorrente, PessoaFisica
from transacoes import Deposito, Saque, Historico
from utils import validar_cpf, validar_data, buscar_endereco_por_cep
from dados import carregar_usuarios, salvar_usuarios, carregar_contas, salvar_contas

LIMITE_SAQUES = 3
AGENCIA = "0001"

# Carrega usuários e contas do armazenamento persistente
usuarios = carregar_usuarios()
contas = carregar_contas()

def buscar_conta_por_numero(contas, numero_conta):
    """
    Busca uma conta pelo número.
    :param contas: Lista de contas cadastradas.
    :param numero_conta: Número da conta a ser buscada.
    :return: Conta encontrada ou None.
    """
    for conta in contas:
        if str(conta.numero) == str(numero_conta):
            return conta
    return None

def buscar_cliente_por_cpf(usuarios, cpf):
    """
    Busca um cliente pelo CPF.
    :param usuarios: Lista de usuários cadastrados.
    :param cpf: CPF do cliente.
    :return: Cliente encontrado ou None.
    """
    for cliente in usuarios:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None

def depositar_na_conta(conta):
    """
    Realiza um depósito na conta informada.
    :param conta: Conta a receber o depósito.
    """
    try:
        valor = Decimal(input("Valor do depósito: ").replace(",", "."))
    except Exception:
        print("Valor inválido!")
        return
    transacao = Deposito(valor)
    resultado = conta.cliente.realizar_transacao(conta, transacao)
    if resultado:
        print("Depósito realizado com sucesso!")
        salvar_contas(contas)
    else:
        print("Operação falhou! Valor inválido.")

def sacar_da_conta(conta):
    """
    Realiza um saque na conta informada.
    :param conta: Conta a ser debitada.
    """
    try:
        valor = Decimal(input("Valor do saque: ").replace(",", "."))
    except Exception:
        print("Valor inválido!")
        return
    transacao = Saque(valor)
    resultado = conta.cliente.realizar_transacao(conta, transacao)
    if resultado is True:
        if isinstance(conta, ContaCorrente):
            saques_restantes = conta.limite_saques - conta.numero_saques
            print("Saque realizado com sucesso!")
            print(f"Saques restantes: {saques_restantes}")
        else:
            print("Saque realizado com sucesso!")
        salvar_contas(contas)
    elif resultado == "limite_saques":
        print("Limite de saques excedido.")
    elif resultado == "limite_valor":
        print("Valor do saque excede o limite permitido.")
    elif resultado == "saldo":
        print("Saldo insuficiente para saque.")
    else:
        print("Operação falhou! Verifique saldo.")

def exibir_extrato_da_conta(conta):
    """
    Exibe o extrato bancário da conta informada.
    :param conta: Conta a ser exibida.
    """
    print("\n=============================\n")
    print("\nEXTRATO BANCÁRIO")
    print("Banco: Banco Exemplo S.A.")
    print(f"Agência: {conta.agencia}")
    print(f"Conta: {conta.numero}")
    print(f"Titular: {conta.cliente.nome}")
    print(f"Período: 01/06/2025 a {datetime.datetime.now().strftime('%d/%m/%Y')}\n")
    print("Data          Hora         Descrição        Tipo      Valor (R$)   Saldo (R$)")
    
    saldo = Decimal("0.00")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for t in conta.historico.transacoes:
            data = getattr(t, "data", datetime.datetime.now().strftime("%d/%m/%Y"))
            hora = getattr(t, "hora", "--:--:--")
            if isinstance(t, Deposito):
                descricao = "Depósito em dinheiro"
                tipo = "Depósito"
                valor = Decimal(str(t.valor))
                saldo += valor
            elif isinstance(t, Saque):
                descricao = "Saque em dinheiro"
                tipo = "Débito"
                valor = Decimal(str(t.valor))
                saldo -= valor
            else:
                continue
            print(f"{data:<11} {hora:8}  {descricao:<21} {tipo:<9} "
                  f"{valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):>10} "
                  f"{saldo.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):>11}")
    print("\n=============================")

def criar_usuario(usuarios):
    """
    Cria um novo usuário (Pessoa Física) e adiciona à lista de usuários.
    :param usuarios: Lista de usuários cadastrados.
    """
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
    """
    Cria uma nova conta corrente para um usuário existente.
    :param contas: Lista de contas cadastradas.
    :param usuarios: Lista de usuários cadastrados.
    """
    cpf = input("Informe o CPF do usuário: ")
    cliente = buscar_cliente_por_cpf(usuarios, cpf)
    if not cliente:
        print("Usuário não encontrado!")
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente(cliente, numero_conta, AGENCIA)
    conta.historico = Historico()
    contas.append(conta)
    cliente.adicionar_conta(conta)
    salvar_contas(contas)
    print(f"Conta criada com sucesso! Número da conta: {numero_conta}")

def listar_contas(contas):
    """
    Lista todas as contas cadastradas no sistema.
    :param contas: Lista de contas cadastradas.
    """
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for conta in contas:
        cliente = conta.cliente
        print(f"Agência: {conta.agencia}, Conta: {conta.numero}, Titular: {cliente.nome}")

def apagar_usuario(usuarios, contas, cpf):
    """
    Remove um usuário do sistema, se não houver contas associadas.
    :param usuarios: Lista de usuários cadastrados.
    :param contas: Lista de contas cadastradas.
    :param cpf: CPF do usuário a ser removido.
    :return: True se removido, False caso contrário.
    """
    for conta in contas:
        if conta.cliente.cpf == cpf:
            print("Não é possível apagar o usuário: existe uma conta associada a este CPF.")
            return False
    for i, usuario in enumerate(usuarios):
        if usuario.cpf == cpf:
            del usuarios[i]
            salvar_usuarios(usuarios)
            print("Usuário apagado com sucesso.")
            return True
    print("Usuário não encontrado.")
    return False

def apagar_conta(contas, conta):
    """
    Remove uma conta do sistema.
    :param contas: Lista de contas cadastradas.
    :param conta: Conta a ser removida.
    """
    contas.remove(conta)
    conta.cliente.contas.remove(conta)
    salvar_contas(contas)
    print("Conta apagada com sucesso!")

def menu_conta(conta):
    """
    Exibe o menu de operações para uma conta específica.
    :param conta: Conta selecionada.
    """
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
    """
    Exibe o menu inicial do sistema bancário.
    """
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