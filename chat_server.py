from socket import *
import _thread

import chat_model as model
import chat_utils as utils

clientesObjeto = []

sockObj = socket(AF_INET, SOCK_STREAM)

meuHost = 'localhost'

minhaPort = 5000

orig = (meuHost, minhaPort)

sockObj.bind(orig)
sockObj.listen(1)


def connectionHandler(clienteConectado):
    nomeCliente = clienteConectado.getNomeCliente()

    conexaoCliente = clienteConectado.getConexaoCliente()

    print('{}: Server conectado por {}'.format(
        utils.getHorario(), nomeCliente))

    while True:
        try:
            mensagem = conexaoCliente.recv(1024)

            if not mensagem:
                print('{}: Cliente {} finalizou a conexão.'.format(
                    utils.getHorario(), nomeCliente))

                clientesObjeto.remove(clienteConectado)

                for k in clientesObjeto:
                    utils.sendMessageTo(k, utils.DISCONNECTEVENT + ' Cliente {} desconectou-se!'.format(
                        '{' + nomeCliente + '}'))

                break

            mensagemDecrypted = utils.decryptMessage(mensagem)
            print('{}: Cliente {} enviou -> {}'.format(utils.getHorario(),
                                                       nomeCliente, mensagemDecrypted))

            if utils.checkEvent(mensagemDecrypted, utils.TYPINGEVENT) or utils.checkEvent(mensagemDecrypted, utils.STOPPEDTYPINGEVENT):
                for k in clientesObjeto:
                    utils.sendMessageTo(
                        k, mensagemDecrypted + ' {' + nomeCliente + '}')
            else:
                if utils.checkEvent(mensagemDecrypted, utils.PRIVATEMESSAGE):
                    clientToSend = utils.getClientByName(
                        clientesObjeto, utils.pegarNickMensagem(mensagemDecrypted, 2))

                    if clientToSend != None:
                        utils.sendMessageTo(
                            clientToSend, utils.PRIVATEMESSAGE + ' ' + mensagemDecrypted)

                else:
                    for k in clientesObjeto:
                        utils.sendMessageTo(
                            k, nomeCliente + ': ' + utils.decryptMessage(mensagem))

        except Exception as e:
            print('{}: Deu ruim na conexão com o cliente {}.'.format(
                utils.getHorario(), nomeCliente))

            print('Mensagem do erro : ' + str(e))

            clientesObjeto.remove(clienteConectado)

            for k in clientesObjeto:
                utils.sendMessageTo(
                    k, utils.DISCONNECTEVENT + ' Cliente {} desconectou-se!'.format('{' + nomeCliente + '}'))

            break

    print('Finalizando conexão do cliente', nomeCliente)

    conexaoCliente.close()

    _thread.exit()


while True:
    con, cliente = sockObj.accept()

    msg = utils.decryptMessage(con.recv(1024))

    print("MensagemRecebida = " + msg)

    if utils.checkEvent(msg, utils.NEWCONNECTIONEVENT):
        print("Nova conexão!")

        clienteNovo = model.Cliente(msg.split(' ', 1)[1], con, cliente)

        for x in clientesObjeto:
            utils.sendMessageTo(clienteNovo, utils.GETCLIENTS +
                                ' {' + x.getNomeCliente() + '}')

        for k in clientesObjeto:
            utils.sendMessageTo(k, utils.NEWCLIENTEVENT + ' Cliente {} conectado!'.format(
                '{' + clienteNovo.getNomeCliente() + '}'
            ))

        utils.sendMessageTo(clienteNovo, utils.NEWCLIENTEVENT + ' Cliente {} conectado!'.format(
            '{' + clienteNovo.getNomeCliente() + '}'
        ))

        clientesObjeto.append(clienteNovo)

        _thread.start_new_thread(connectionHandler, tuple([clienteNovo]))
    else:
        print('Cliente {} desatualizado!'.format(cliente[1]))

        con.sendall(
            'Seu cliente está desatualizado! Favor atualizar e tentar novamente!'.encode('utf-8'))

        con.close()

        print('Conexão com cliente {} finalizada'.format(cliente[1]))
