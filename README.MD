# Otimizando Sistema Bancário com Funções Python

Projeto proposto pelo bootcamp **Santander 2025 - Backend Python** da DIO/Santander.

## Sobre o Projeto

Este é um sistema bancário simples, desenvolvido em Python, com foco em aprendizado de funções, manipulação de arquivos, persistência de dados e boas práticas de programação. O projeto é **open source** e voltado para fins educacionais.

O sistema permite:
- Cadastro de usuários e contas bancárias
- Depósitos, saques e extratos vinculados a contas
- Busca automática de endereço pelo CEP (ViaCEP)
- Persistência dos dados em arquivos `.pkl` (pickle)
- Exclusão de usuários e contas
- Interface de menus para navegação

## Estrutura do Projeto

- [`sistema_bancario.py`](sistema_bancario.py): Arquivo principal com toda a lógica do sistema e menus.
- [`dados.py`](dados.py): Responsável por carregar e salvar os dados de usuários e contas em arquivos pickle (`.pkl`).
- `usuarios.pkl` e `contas.pkl`: Arquivos gerados automaticamente para armazenar os dados.
- [`requirements.txt`](requirements.txt): Lista de dependências do projeto.
- `.gitignore.txt`: Arquivo para ignorar arquivos e pastas desnecessários no controle de versão.
- Requer a biblioteca `requests` para consulta de CEP.

## Como Executar

1. **Clone ou baixe este repositório.**
2. Instale as dependências com:
   ```
   pip install -r requirements.txt
   ```
3. Execute o arquivo principal:
   ```
   python sistema_bancario.py
   ```

## Regras de Utilização

### Menu Inicial

- `[ec] Entrar na Conta`: Acesse uma conta existente informando o número da conta.
- `[nu] Novo Usuário`: Cadastre um novo usuário, informando CPF, nome, data de nascimento e endereço (buscado automaticamente pelo CEP).
- `[nc] Nova Conta`: Crie uma nova conta para um usuário já cadastrado (informe o CPF).
- `[lc] Listar Contas`: Exibe todas as contas cadastradas.
- `[au] Apagar Usuário`: Remove um usuário pelo CPF (só é possível se não houver contas vinculadas).
- `[q] Sair`: Encerra o sistema.

### Menu da Conta

Após acessar uma conta pelo número:
- `[d] Depositar`: Realize um depósito na conta.
- `[s] Sacar`: Realize um saque (máximo R$500 por saque, até 3 saques diários).
- `[e] Extrato`: Veja o extrato e saldo da conta.
- `[ac] Apagar Conta`: Remove a conta atual.
- `[voltar] Voltar ao menu inicial`: Retorna ao menu principal.

### Outras Regras

- **CPF**: Validado conforme regras brasileiras. Não é possível cadastrar dois usuários com o mesmo CPF.
- **Data de nascimento**: Deve estar no formato `dd-mm-aaaa`.
- **Endereço**: Buscado automaticamente pelo CEP informado (necessário internet).
- **Persistência**: Todos os dados são salvos automaticamente em arquivos `.pkl` na mesma pasta do projeto.
- **Exclusão**: Não é possível excluir um usuário que possua contas vinculadas.

## Geração de Dados de Teste

Para facilitar os testes, utilizei a ferramenta [4Devs](https://www.4devs.com.br/) para gerar CPFs e CEPs válidos.

## Arquivo `.gitignore.txt`

O projeto contém um arquivo `.gitignore.txt` para evitar o versionamento de arquivos desnecessários, como:

```
# Bytecode do Python
__pycache__/
*.py[cod]
*.pyo

# Arquivos temporários
*.log
*.tmp

# Arquivos JSON
*.json

# Ambiente virtual
venv/
.env/

# Configurações de IDEs
.vscode/
.idea/

# Arquivos de sistema
.DS_Store
Thumbs.db
```

## Licença

Este projeto é open source e de uso livre para fins educacionais.

---

Projeto proposto por [DIO](https://www.dio.me/) no bootcamp **Santander 2025 - Backend Python**.