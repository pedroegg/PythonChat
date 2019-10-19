from socket import *
import _thread
from time import strftime

import urllib.request


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


clientesObjeto = []
palavraChave = 'Lampada'


def getHorario():
    return strftime("%d/%m/%Y %H:%M:%S")


def criptografar(texto):
    textoRetorno = ''
    kIterador = 0
    x = 0
    while x < len(texto):
        textoRetorno = textoRetorno + chr(soma(ord(texto[x]), ord(palavraChave[kIterador])))
        if kIterador < len(palavraChave)-1:
            kIterador = kIterador + 1
        else:
            kIterador = 0
        x = x + 1
    return textoRetorno


def descriptografar(texto):
    textoRetorno = ''
    kIterador = 0
    x = 0
    while x < len(texto):
        try:
            textoRetorno = textoRetorno + chr(subtrair(ord(texto[x]), ord(palavraChave[kIterador])))
            if kIterador < len(palavraChave)-1:
                kIterador = kIterador + 1
            else:
                kIterador = 0
            x = x + 1
        except ValueError as e:
            print("DEU RUIM, NAO CRIPTOGRAFOU")
            print("Erro = " + str(e))

    return textoRetorno


def soma(valor1, valor2):

    if valor1 + valor2 > 126:
        valorReal = valor1
        for x in range(0, valor2, 1):
            if valorReal + 1 == 127:
                valorReal = 32
            else:
                valorReal = valorReal + 1
        return valorReal
    else:
        return valor1 + valor2


def subtrair(valor1, valor2):

    if valor1 - valor2 < 32:
        valorReal = valor1
        for x in range(0, valor2, 1):
            if valorReal - 1 == 31:
                valorReal = 126
            else:
                valorReal = valorReal - 1
        return valorReal
    else:
        return valor1 - valor2


def conectado(clienteConectado):
    nomeCliente = clienteConectado.getNomeCliente()
    conexaoCliente = clienteConectado.getConexaoCliente()
    print('{}: Server conectado por {}'.format(getHorario(), nomeCliente))

    while True:
        try:
            mensagem = conexaoCliente.recv(1024)
            if not mensagem:
                print('{}: Cliente {} finalizou a conexão.'.format(getHorario(), nomeCliente))
                clientesObjeto.remove(clienteConectado)
                for k in clientesObjeto:
                    k.getConexaoCliente().sendall(criptografar('xls8123476-211 ' + 'Cliente {} desconectou-se!'.format('{' + nomeCliente + '}')).encode('utf-8'))
                break
            print('{}: Cliente {} enviou -> {}'.format(getHorario(), nomeCliente, descriptografar(mensagem.decode('utf-8'))))
            if ('xls8123476-209' in descriptografar(mensagem.decode('utf-8'))) or ('xls8123476-210' in descriptografar(mensagem.decode('utf-8'))):
                for k in clientesObjeto:
                    k.getConexaoCliente().sendall(criptografar(descriptografar(mensagem.decode('utf-8')) + ' {' + nomeCliente + '}').encode('utf-8'))
            else:
                for k in clientesObjeto:
                    k.getConexaoCliente().sendall(criptografar(nomeCliente + ': ' + descriptografar(mensagem.decode('utf-8'))).encode('utf-8'))
        except Exception as e:
            print('{}: Deu ruim na conexão com o cliente {}.'.format(getHorario(), nomeCliente))
            print('Mensagem do erro : ' + str(e))
            clientesObjeto.remove(clienteConectado)
            for k in clientesObjeto:
                k.getConexaoCliente().sendall(criptografar('xls8123476-211 ' + 'Cliente {} desconectou-se!'.format('{' + nomeCliente + '}')).encode('utf-8'))
            break

    print('Finalizando conexão do cliente', nomeCliente)
    conexaoCliente.close()
    _thread.exit()


sockObj = socket(AF_INET, SOCK_STREAM)

meuHost = '127.0.0.1'
minhaPort = 5000

orig = (meuHost, minhaPort)

sockObj.bind(orig)
sockObj.listen(1)

while True:
    con, cliente = sockObj.accept()
    msg = descriptografar(con.recv(1024).decode('utf-8'))
    print("MensagemRecebida = " + msg)
    if 'xls8123476-212' in msg:
        clienteNovo = Cliente(msg.split(' ', 1)[1], con, cliente)
        clientesObjeto.append(clienteNovo)
        for x in clientesObjeto:
            x.getConexaoCliente().sendall(criptografar('xls8123476-213 Cliente {} conectado!'.format('{' + clienteNovo.getNomeCliente() + '}')).encode('utf-8'))
        for k in clientesObjeto:
            if k.getNomeCliente() != clienteNovo.getNomeCliente():
                clienteNovo.getConexaoCliente().sendall(criptografar('xls8123476-208 {' + k.getNomeCliente() + '}').encode('utf-8'))
        _thread.start_new_thread(conectado, tuple([clienteNovo]))
    else:
        print('Cliente {} desatualizado!'.format(cliente[1]))
        con.sendall(criptografar('Seu cliente está desatualizado! Favor atualizar e tentar novamente!').encode('utf-8'))
        con.close()
        print('Conexão com cliente {} finalizada'.format(cliente[1]))
