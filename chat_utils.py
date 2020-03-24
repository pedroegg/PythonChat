from time import strftime

TYPINGEVENT = 'typing...'
STOPPEDTYPINGEVENT = 'stoppedTyping'
DISCONNECTEVENT = 'disconnect'
NEWCONNECTIONEVENT = 'newConnection'
NEWCLIENTEVENT = 'newClient'
GETCLIENTS = 'getClients'
PRIVATEMESSAGE = 'privateMessage'
key = 'Lampada'


def checkEvent(message, event):
    return event in message and message[:1] != '"'


def sendMessageTo(client, message):
    client.getConexaoCliente().sendall(encryptMessage(message))


def decryptMessage(message):
    return __descriptografar(key, message.decode('utf-8'))


def encryptMessage(message):
    return __criptografar(key, message).encode('utf-8')


def getHorario():
    return strftime("%d/%m/%Y %H:%M:%S")


def getClientByName(lista, name):
    objeto = None

    for x in lista:
        if x.getNomeCliente() == name:
            objeto = x
            break

    return objeto


def pegarNickMensagem(mensagemParametro, indice):
    nickRetorno = ''

    x = 0

    for k in range(0, indice, 1):
        while mensagemParametro[x] != '{':
            x += 1

        x += 1

    while mensagemParametro[x] != '}':
        nickRetorno += mensagemParametro[x]

        x += 1

    return nickRetorno


def __criptografar(key, texto):
    textoRetorno = ''

    kIterador = 0

    x = 0

    while x < len(texto):
        textoRetorno = textoRetorno + \
            chr(__soma(ord(texto[x]), ord(key[kIterador])))

        if kIterador < len(key)-1:
            kIterador = kIterador + 1
        else:
            kIterador = 0

        x = x + 1

    return textoRetorno


def __descriptografar(key, texto):
    textoRetorno = ''

    kIterador = 0

    x = 0

    while x < len(texto):
        try:
            textoRetorno = textoRetorno + \
                chr(__subtrair(ord(texto[x]), ord(key[kIterador])))

            if kIterador < len(key) - 1:
                kIterador = kIterador + 1
            else:
                kIterador = 0

            x = x + 1
        except ValueError as e:
            print("DEU RUIM, NAO DESCRIPTOGRAFOU")

            print("Erro = " + str(e))

    return textoRetorno


def __soma(valor1, valor2):

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


def __subtrair(valor1, valor2):

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
