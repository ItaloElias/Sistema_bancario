import pickle
import os

USUARIOS_FILE = "usuarios.pkl"
CONTAS_FILE = "contas.pkl"

def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "rb") as f:
            return pickle.load(f)
    return []

def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, "wb") as f:
        pickle.dump(usuarios, f)

def carregar_contas():
    if os.path.exists(CONTAS_FILE):
        with open(CONTAS_FILE, "rb") as f:
            return pickle.load(f)
    return []

def salvar_contas(contas):
    with open(CONTAS_FILE, "wb") as f:
        pickle.dump(contas, f)