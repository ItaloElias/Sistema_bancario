import datetime

def validar_cpf(cpf):
    """
    Valida um CPF brasileiro.
    :param cpf: String contendo o CPF (com ou sem formatação).
    :return: True se válido, False caso contrário.
    """
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
    """
    Valida uma data no formato dd-mm-aaaa.
    :param data: String da data.
    :return: True se a data for válida, False caso contrário.
    """
    try:
        datetime.datetime.strptime(data, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def buscar_endereco_por_cep(cep):
    """
    Busca o endereço correspondente a um CEP usando a API ViaCEP.
    :param cep: String do CEP (com ou sem formatação).
    :return: String formatada com o endereço ou None se não encontrado/erro.
    """
    import requests
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
        print("Não foi possível buscar o endereço no momento. Tente novamente mais tarde.")
        return None