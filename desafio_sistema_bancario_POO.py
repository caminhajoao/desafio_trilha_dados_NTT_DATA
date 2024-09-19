class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def exibir(self):
        print("\n================ EXTRATO ================")
        if not self.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in self.transacoes:
                print(transacao)
        print("==========================================")


class Transacao:
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(f"Depósito: R$ {self.valor:.2f}")
        print("\n=== Depósito realizado com sucesso! ===")


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.saldo < self.valor:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
        else:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(f"Saque: R$ {self.valor:.2f}")
            print("\n=== Saque realizado com sucesso! ===")


class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self.saldo = 0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)

    def sacar(self, valor):
        saque = Saque(valor)
        saque.registrar(self)

    def exibir_extrato(self):
        self.historico.exibir()


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques >= self.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > self.limite:
            print("\n@@@ Operação falhou! Valor excede o limite de saque. @@@")
        else:
            super().sacar(valor)
            self.numero_saques += 1


class Cliente:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, endereco, cpf, data_nascimento):
        super().__init__(nome, endereco)
        self.cpf = cpf
        self.data_nascimento = data_nascimento


# Funções auxiliares para simular o menu
def criar_usuario():
    nome = input("Informe o nome completo: ")
    cpf = input("Informe o CPF: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    return PessoaFisica(nome, endereco, cpf, data_nascimento)


def criar_conta(cliente, numero_conta):
    return ContaCorrente(cliente, numero_conta)


def obter_valor_float(mensagem):
    while True:
        valor_str = input(mensagem)
        try:
            # Substitui a vírgula por ponto e tenta converter para float
            valor = float(valor_str.replace(",", "."))
            if valor <= 0:
                print("\n@@@ O valor deve ser positivo! Tente novamente. @@@")
            else:
                return valor
        except ValueError:
            print("\n@@@ Entrada inválida! Insira um número válido. @@@")


def main():
    usuarios = []
    contas = []
    
    while True:
        print("\n================ MENU ================")
        print("[1] Novo usuário")
        print("[2] Nova conta")
        print("[3] Depositar")
        print("[4] Sacar")
        print("[5] Extrato")
        print("[0] Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            usuario = criar_usuario()
            usuarios.append(usuario)
            print("=== Usuário criado com sucesso! ===")

        elif opcao == "2":
            if not usuarios:
                print("\n@@@ Nenhum usuário cadastrado! Crie um usuário primeiro. @@@")
                continue

            for i, usuario in enumerate(usuarios):
                print(f"[{i}] {usuario.nome} (CPF: {usuario.cpf})")
            
            try:
                usuario_index = int(input("Selecione o usuário para criar a conta (insira o número correspondente): "))
                if usuario_index < 0 or usuario_index >= len(usuarios):
                    raise IndexError

                numero_conta = len(contas) + 1
                conta = criar_conta(usuarios[usuario_index], numero_conta)
                usuarios[usuario_index].adicionar_conta(conta)
                contas.append(conta)

                print(f"\n=== Conta criada com sucesso! Número da conta: {numero_conta} ===")

            except ValueError:
                print("\n@@@ Entrada inválida! Digite um número válido. @@@")
            except IndexError:
                print("\n@@@ Usuário não encontrado! Escolha um número de usuário válido. @@@")

        elif opcao == "3":
            try:
                numero_conta = int(input("Informe o número da conta para depósito: "))
                
                if numero_conta < 1 or numero_conta > len(contas):
                    raise IndexError

                valor = obter_valor_float("Informe o valor do depósito: ")
                conta = contas[numero_conta - 1]
                conta.depositar(valor)

            except ValueError:
                print("\n@@@ Entrada inválida! Use um número válido. @@@")
            except IndexError:
                print("\n@@@ Conta não encontrada! Verifique o número da conta. @@@")

        elif opcao == "4":
            try:
                numero_conta = int(input("Informe o número da conta para saque: "))
                valor = obter_valor_float("Informe o valor do saque: ")

                if numero_conta < 1 or numero_conta > len(contas):
                    raise IndexError

                conta = contas[numero_conta - 1]
                conta.sacar(valor)

            except ValueError:
                print("\n@@@ Entrada inválida! Use um número válido. @@@")
            except IndexError:
                print("\n@@@ Conta não encontrada! Verifique o número da conta. @@@")

        elif opcao == "5":
            try:
                numero_conta = int(input("Informe o número da conta para extrato: "))

                if numero_conta < 1 or numero_conta > len(contas):
                    raise IndexError

                conta = contas[numero_conta - 1]
                conta.exibir_extrato()

            except ValueError:
                print("\n@@@ Entrada inválida! Use um número válido. @@@")
            except IndexError:
                print("\n@@@ Conta não encontrada! Verifique o número da conta. @@@")

        elif opcao == "0":
            break

        else:
            print("Opção inválida! Tente novamente.")


main()
