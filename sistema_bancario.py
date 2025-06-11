import datetime
import requests
from dados import carregar_usuarios, salvar_usuarios, carregar_contas, salvar_contas

LIMITE_SAQUES = 3
AGENCIA = "0001"

usuarios = carregar_usuarios()
contas = carregar_contas()

def buscar_conta_por_numero(contas, numero_conta):
    for conta in contas:
        if str(conta["numero_conta"]) == str(numero_conta):
            return conta
    return None

def buscar_conta_por_cpf(contas, cpf):
    for conta in contas:
        if conta["usuario"]["cpf"] == cpf:
            return conta
    return None

def depositar_na_conta(conta):
    valor = float(input("Valor do depósito: "))
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
        salvar_contas(contas)
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! Valor inválido.")

def sacar_da_conta(conta):
    valor = float(input("Valor do saque: "))
    if valor > conta["saldo"]:
        print("Operação falhou! Saldo insuficiente.")
    elif valor > 500:
        print("Operação falhou! Valor excede o limite por saque.")
    elif conta["numero_saques"] >= LIMITE_SAQUES:
        print("Operação falhou! Limite de saques excedido.")
    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        conta["numero_saques"] += 1
        salvar_contas(contas)
        print("Saque realizado com sucesso!")
    else:
        print("Operação falhou! Valor inválido.")

def exibir_extrato_da_conta(conta):
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
    print(f"\nSaldo: R$ {conta['saldo']:.2f}")
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
        usuario = filtrar_usuario(cpf, usuarios)
        if usuario:
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

    usuarios.append({"nome": nome, "nascimento": nascimento, "cpf": cpf, "endereco": endereco})
    salvar_usuarios(usuarios)
    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    return next((u for u in usuarios if u["cpf"] == cpf), None)

def criar_conta(contas, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("Usuário não encontrado!")
        return

    numero_conta = len(contas) + 1
    contas.append({
        "agencia": AGENCIA,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": "",
        "numero_saques": 0
    })
    salvar_contas(contas)
    print(f"Conta criada com sucesso! Número da conta: {numero_conta}")

def listar_contas(_):
    contas = carregar_contas()
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for conta in contas:
        usuario = conta["usuario"]
        print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Titular: {usuario['nome']}")

def apagar_usuario(usuarios, contas):
    cpf = input("Informe o CPF do usuário a ser apagado: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("Usuário não encontrado!")
        return
    contas_vinculadas = [conta for conta in contas if conta["usuario"]["cpf"] == cpf]
    if contas_vinculadas:
        print("Não é possível apagar o usuário. Existem contas vinculadas a este CPF.")
        return
    usuarios.remove(usuario)
    salvar_usuarios(usuarios)
    print("Usuário apagado com sucesso!")

def apagar_conta(contas, conta):
    contas.remove(conta)
    salvar_contas(contas)
    print("Conta apagada com sucesso!")

def menu_conta(conta):
    primeira_vez = True    
    while True:
        if primeira_vez:
            print(f"\nBem-vindo, {conta['usuario']['nome']}! (Conta: {conta['numero_conta']})")
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
            apagar_usuario(usuarios, contas)
        elif opcao == "q":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_inicial()