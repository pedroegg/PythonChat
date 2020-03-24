class Cliente:
    def __init__(self, nomeCliente, conexaoCliente, cliente):
        self.nome = nomeCliente
        self.conexao = conexaoCliente
        self.cliente = cliente

    def getNomeCliente(self):
        return self.nome

    def getConexaoCliente(self):
        return self.conexao

    def getCliente(self):
        return self.cliente
