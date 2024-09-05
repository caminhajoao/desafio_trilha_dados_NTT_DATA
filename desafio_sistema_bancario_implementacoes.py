# Funções para operações existentes

def saque(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return saldo, extrato
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return saldo, extrato
    elif numero_saques >= LIMITE_SAQUES:
        print("Operação falhou! Número máximo de saques excedido.")
        return saldo, extrato
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato

def deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato

def extrato(saldo, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Funções para novas funcionalidades

usuarios = []
contas = []
numero_conta = 1
AGENCIA = "0001"

def criar_usuario(nome, data_nascimento, codigo, endereco):
    # Verificar se código já está cadastrado
    if any(usuario['codigo'] == codigo for usuario in usuarios):
        print("Código já cadastrado.")
        return
    
    usuarios.append({
        'nome': nome,
        'data_nascimento': data_nascimento,
        'codigo': codigo,  # Código de 4 dígitos
        'endereco': endereco
    })
    print(f"Usuário {nome} cadastrado com sucesso.")

def criar_conta_corrente(codigo):
    global numero_conta
    
    usuario = next((u for u in usuarios if u['codigo'] == codigo), None)
    if usuario is None:
        print("Usuário não encontrado.")
        return
    
    contas.append({
        'agencia': AGENCIA,
        'numero_conta': numero_conta,
        'usuario': usuario
    })
    numero_conta += 1
    print(f"Conta corrente {numero_conta - 1} criada com sucesso para o usuário {usuario['nome']}.")

# Código principal
menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar Usuário
[5] Criar Conta Corrente
[6] Sair
=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = deposito(saldo, valor, extrato)

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES)

    elif opcao == "3":
        extrato(saldo, extrato=extrato)

    elif opcao == "4":
        nome = input("Nome: ")
        data_nascimento = input("Data de Nascimento: ")
        codigo = input("Código (4 dígitos): ")
        endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        criar_usuario(nome, data_nascimento, codigo, endereco)

    elif opcao == "5":
        codigo = input("Informe o código do usuário para criar conta: ")
        criar_conta_corrente(codigo)

    elif opcao == "6":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
