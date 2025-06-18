import pickle
import os

USUARIOS_FILE = "usuarios.pkl"
CONTAS_FILE = "contas.pkl"

def carregar_usuarios():
    """
    Carrega a lista de usuários do arquivo de persistência.
    :return: Lista de usuários, ou lista vazia se o arquivo não existir.
    """
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "rb") as f:
            return pickle.load(f)
    return []

def salvar_usuarios(usuarios):
    """
    Salva a lista de usuários no arquivo de persistência.
    :param usuarios: Lista de usuários a ser salva.
    """
    with open(USUARIOS_FILE, "wb") as f:
        pickle.dump(usuarios, f)

def carregar_contas():
    """
    Carrega a lista de contas do arquivo de persistência.
    :return: Lista de contas, ou lista vazia se o arquivo não existir.
    """
    if os.path.exists(CONTAS_FILE):
        with open(CONTAS_FILE, "rb") as f:
            return pickle.load(f)
    return []

def salvar_contas(contas):
    """
    Salva a lista de contas no arquivo de persistência.
    :param contas: Lista de contas a ser salva.
    """
    with open(CONTAS_FILE, "wb") as f:
        pickle.dump(contas, f)