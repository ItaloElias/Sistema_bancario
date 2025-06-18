# Sistema Bancário em Python

Projeto proposto pelo bootcamp **Santander 2025 - Backend Python** da DIO/Santander.

## Sobre o Projeto

Este é um sistema bancário simples, modularizado e orientado a objetos, desenvolvido em Python. O foco é o aprendizado de boas práticas, funções, manipulação de arquivos, persistência de dados e organização de código. O projeto é **open source** e voltado para fins educacionais.

O sistema permite:
- Cadastro de usuários (Pessoa Física) com validação de CPF e busca automática de endereço via CEP (ViaCEP)
- Criação de contas correntes com limite de saque e controle de número de saques
- Depósitos, saques e extratos vinculados a contas
- Persistência dos dados em arquivos `.pkl` (pickle)
- Exclusão de usuários e contas
- Interface de menus para navegação

## Estrutura do Projeto

```
Sistema_bancario/
│
├── sistema_bancario.py      # Interface principal (menus, entrada do usuário)
├── modelos.py               # Classes: Conta, ContaCorrente, Cliente, PessoaFisica
├── transacoes.py            # Classes: Deposito, Saque, Historico, Transacao
├── utils.py                 # Funções auxiliares: validação de CPF, data, busca de endereço, etc.
├── dados.py                 # Funções de persistência (carregar/salvar usuários e contas)
├── requirements.txt         # Dependências do projeto
├── .gitignore.txt           # Arquivos e pastas ignorados pelo Git
├── usuarios.pkl / contas.pkl# Arquivos gerados automaticamente para armazenar os dados
```

## Como Executar

1. **Clone ou baixe este repositório.**
2. (Opcional) Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate   # Windows
   # ou
   source venv/bin/activate  # Linux/Mac
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Execute o arquivo principal:
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

Para facilitar os testes, utilize ferramentas como [4Devs](https://www.4devs.com.br/) para gerar CPFs e CEPs válidos.

## Principais Dependências

- `requests` (para busca de endereço via CEP)
- `decimal` (precisão em operações financeiras)
- Outras dependências listadas em `requirements.txt`

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

# Arquivos pickle
*.pkl

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

## Boas Práticas Adotadas

- Modularização do código em arquivos separados por responsabilidade
- Uso de docstrings e comentários explicativos
- Separação entre lógica de negócio e interface com o usuário
- Validação de dados de entrada
- Uso de `Decimal` para operações financeiras
- Persistência de dados com pickle
- Padronização de nomes e mensagens

## Licença

Este projeto é open source e de uso livre para fins educacionais.

---

Projeto proposto por [DIO](https://www.dio.me/) no bootcamp **Santander 2025 - Backend Python**.