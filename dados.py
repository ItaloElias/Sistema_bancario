import json
import os

USUARIOS_FILE = "usuarios.json"
CONTAS_FILE = "contas.json"

def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=4)

def carregar_contas():
    if os.path.exists(CONTAS_FILE):
        with open(CONTAS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_contas(contas):
    with open(CONTAS_FILE, "w", encoding="utf-8") as f:
        json.dump(contas, f, ensure_ascii=False, indent=4)