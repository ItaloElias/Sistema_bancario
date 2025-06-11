import json
import os

# Caminhos dos arquivos de dados
USUARIOS_FILE = "usuarios.json"
CONTAS_FILE = "contas.json"

# Carrega a lista de usuários do arquivo JSON, se existir
def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Salva a lista de usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=4)

# Carrega a lista de contas do arquivo JSON, se existir
def carregar_contas():
    if os.path.exists(CONTAS_FILE):
        with open(CONTAS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Salva a lista de contas no arquivo JSON
def salvar_contas(contas):
    with open(CONTAS_FILE, "w", encoding="utf-8") as f:
        json.dump(contas, f, ensure_ascii=False, indent=4)