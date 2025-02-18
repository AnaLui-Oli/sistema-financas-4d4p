from models import Conta, conexao, Bancos, Status, Historico, Tipos
from sqlmodel import select, Session
from datetime import date, timedelta

def criar_conta(conta: Conta):
    with Session(conexao) as sessao:
        comando = select(Conta).where(Conta.banco == conta.banco, Conta.user == conta.user)
        resposta = sessao.exec(comando).all()
        print(resposta)

        if resposta:
            print("Você ja possui conta neste banco.")
            #ver se está ativo ou inativo
        else:
            sessao.add(conta)
            sessao.commit()
    return conta

def listar_contas():
    with Session(conexao) as sessao:
        comando = select(Conta)
        resposta = sessao.exec(comando).all()
    return resposta

def desativar_conta(id):
     with Session(conexao) as sessao:
        comando = select(Conta).where(Conta.id == id)
        conta = sessao.exec(comando).first()
        if conta.saldo < 0:
            print("Você não pode desativar sua conta antes de quitar suas dívidas")
        elif conta.saldo > 0:
            desativar = input("Você ainda possui saldo em sua conta, tem certeza que deseja desativar?(y/n)")
            if desativar.title() == "Y":
                conta.status = Status.INATIVO
                print("sua conta foi inativada")
        else:
            conta.status = Status.INATIVO
            print("sua conta foi inativada")
        sessao.commit()

def transferir_saldo(id_remetente, id_destinatario, valor):
    with Session(conexao) as sessao:
        comando = select(Conta).where(Conta.id == id_remetente)
        conta_saida = sessao.exec(comando).first()
        
        if conta_saida.saldo < valor:
            raise ValueError("saldo insuficiente!")
        
        comando = select(Conta).where(Conta.id == id_destinatario)
        conta_entrada = sessao.exec(comando).first()

        conta_saida.saldo -= valor
        conta_entrada.saldo += valor 
        print("transação efetuada com sucesso!")
        sessao.commit()

def movimentacao_valores(historico: Historico):
    with Session(conexao) as sessao:
        comando = select(Conta).where(Conta.id==historico.conta_id)
        conta = sessao.exec(comando).first()

        #TODO: verificar se a conta esta inativa!

        if historico.tipo == Tipos.ENTRADA:
            conta.saldo += historico.valor
        else:
            if conta.saldo < historico.valor:
                raise ValueError("Saldo insuficiente")
            conta.saldo -= historico.valor
        
        sessao.add(historico)
        sessao.commit()
        return historico

def total_contas(user):
    with Session(conexao) as sessao:
        comando = select(Conta).where(Conta.user==user)
        contas = sessao.exec(comando).all()
    
    total = 0 
    for conta in contas:
        total += conta.saldo
    return float(total)

def buscar_historico_entre_datas(data_inicio:date,data_fim:date):
    with Session(conexao) as sessao:
        comando = select(Historico).where(Historico.data>=data_inicio, Historico.data<=data_fim) #clausulas where separadas por , e não por and
        resposta = sessao.exec(comando).all()
        return resposta

def criar_grafico_por_conta(user):
    with Session(conexao) as sessao:
        comando = select(Conta).where(Conta.status==Status.ATIVO, Conta.user==user)
        contas = sessao.exec(comando).all()
        
        bancos = [i.banco.value for i in contas]
        valores = []
        for i in contas:
            valores.append(i.saldo)

        import matplotlib.pyplot as plt 

        plt.bar(bancos, valores)
        plt.show()
        

nova_conta = Conta(user='afonsobruto@gmail.com',saldo=-9540,banco=Bancos.NUBANK)
criar_conta(nova_conta)
nova_conta = Conta(user='joseluis@gmail.com',saldo=-100,banco=Bancos.INTER)
criar_conta(nova_conta)
nova_conta = Conta(user='robertaamaral@gmail.com',saldo=2000,banco=Bancos.CAIXA)
criar_conta(nova_conta)
nova_conta = Conta(user='afonsobruto@gmail.com',saldo=-40,banco=Bancos.BANCO_BRASIL)
criar_conta(nova_conta)
nova_conta = Conta(user='afonsobruto@gmail.com',saldo=-540,banco=Bancos.ITAU)
criar_conta(nova_conta)
nova_conta = Conta(user='afonsobruto@gmail.com',saldo=-0,banco=Bancos.SANTANDER)
criar_conta(nova_conta)

desativar_conta(5)
desativar_conta(4)
desativar_conta(3)

# transferir_saldo(1,2, 50.50)
# transferir_saldo(2,0, 5)
# transferir_saldo(0,1, 0.75)
ontem = date.today() - timedelta(days=1)

historico = Historico(conta_id=2, tipo=Tipos.ENTRADA, valor=96, data=date.today())
movimentacao_valores(historico)

# print(total_contas('afonsobruto@gmail.com'))

# amanha = date.today() + timedelta(days=1)

# r = buscar_historico_entre_datas(ontem, amanha)
# print(r)

# criar_grafico_por_conta('afonsobruto@gmail.com')

# import matplotlib.pyplot as plt 

# # plt.bar(['opcao 1', 'opcao 2'], [100, 1])
# # plt.show()