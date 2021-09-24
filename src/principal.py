# coding: utf-8
# projeto para a disciplina de programacao 1 do IFPB
# alunos: Diego Cardoso e Igor Kadson
# este modulo funciona como uma interface de interação entre o usuario e as partes logicas do jogo, pode ser facilmente substituido por uma interfaces
# grafica que quiçá será implementada futuramente

import time

from PartesLogicas import *
import os


timming = 0

def cls():
    """
    funcao que limpa o terminal sempre que invocada
    :return: void
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def mapa_com_bombas(cenarioCriado):
    """
    exibe o mapa com as bombas na tela
    :param cenarioCriado: importa o cenario criado
    :return: void, printa o cenario
    """
    contador_linhas = 0
    for linha in range(len(cenarioCriado)):
        for coluna in range(len(cenarioCriado)):
            if cenarioCriado[linha][coluna] == 0:
                if coluna == (len(cenarioCriado) - 1):
                    print('\U0001F33F')
                else:
                    print('\U0001F33F', end='')
            elif cenarioCriado[linha][coluna] == 1:
                if coluna == (len(cenarioCriado) - 1):
                    print('\U0001F4A3')
                else:
                    print('\U0001F4A3', end='')
            else:
                if coluna == (len(cenarioCriado) - 1):
                    print('\U0001F3C7'.format(contador_linhas))
                else:
                    print('\U0001F3C7', end='')


def mapaReal(cenario):
    """
    imprime o mapa da fase com as bombas e caminhos livres ocultos
    :param cenario: mapa da fase a ser iterado
    :return: void, printa o mapa da fase
    """
    for linha in range(len(cenario)):
        for coluna in range(len(cenario[linha])):
            if cenario[linha][coluna] != 'x':
                print('\U0001F33F', end='')
            else:
                print('\U0001F3C7', end='')
            if coluna + 1 == len(cenario):
                print()


def jogando():
    '''
    funcao que inicia o jogo propriamente dito, onde serao setados os movimentos e verificado se o jogador vence ou perde a partida.
    :param cenario: mapa da fase
    :param posicao: lugar onde o jogador inicia a partida
    :return: void
    '''

    cenario = getCenario()
    posicao = getPosicao()

    while True:
        cls()
        power = getPowerUps()
        mapaReal(cenario)
        movimento = str(input()).upper()
        movimento = validaMovimentacao(movimento, cenario, posicao)

        if movimento in power:
            cls()
            aplicaPowerUp(movimento)
            power.remove(movimento)
            time.sleep(2)

        if verificaSeMorreu(movimento, cenario, posicao):
            if "REVIVER" in power:
                power.remove("REVIVER")
            else:
                incrementa_vezesRodando()
                cls()
                mapa_com_bombas(cenario)
                print("Que pena...\nVocê perdeu!")
                time.sleep(5)
                cls()
                break

        controlaPersonagem(movimento, cenario, posicao)

        if venceu(cenario):
            incrementa_vezesRodando()
            passouFase()
            time.sleep(3)
            print("Você passou de fase! O que deseja fazer?")
            cls()
            break

    terminou_partida()


def aplicaPowerUp(movimento):
    bombas = getCenario()
    if movimento == "SB":
        mapa_com_bombas(bombas)

def comoJogar():
    while True:
        print("Deseja aprender como jogar?")
        resposta = str(input()).lower()
        if (resposta == "não" or resposta == "n"):
            break
        else:
            print("regras do jogo: blablala")
            print("Pressione qualquer tecla para continuar: ")
            break


def validaMovimentacao(movimento, cenario, pos_x):
    """
    :param movimento: parametro a ser validado
    :param cenario: para analisar o mapa e tentar adivinhar o proximo movimento do x
    :param pos_x: naquele instante 't'
    :return: o input do movimento adequadamente atualizado
    """
    possibilities = ["W", "S", "A", "D"]
    powerUps = getPowerUps()
    possibilities.extend(powerUps)
    while True:
        if movimento not in possibilities:
            print("Movementacao inválida, por favor tente novamente")
            movimento = str(input()).upper()
        else:
            if movimento == "S":
                if pos_x[0] == len(cenario) - 1:
                    print("Escolha uma movimentação dentro do mapa")
                    movimento = str(input()).upper()
                else:
                    return movimento
            elif movimento == "A":
                if pos_x[1] == 0:
                    print("Escolha uma movimentação dentro do mapa")
                    movimento = str(input()).upper()
                else:
                    return movimento
            elif movimento == "D":
                if pos_x[1] == len(cenario) - 1:
                    print("Escolha uma movimentação dentro do mapa")
                    movimento = str(input()).upper()
                else:
                    return movimento
            elif movimento == "W":
                return movimento
            else:
                return movimento


def iniciandoJogo():
    """
    imprime a primeira tela que o jogador vera, mostrando as bombas e caminhos livres. apos 6s, o cenario eh ocultado
    :param cenario: mapa da fase "cru" a ser printado na tela com as bombas
    :return: void, printa o mapa
    """
    cenario = getCenario()
    timming = getTimming()
    if timming == 0:
        print("\nVocê está preparado?\n")
        time.sleep(1)
        mapa_com_bombas(cenario)
        time.sleep(4)
        print("\nSerá mesmo??????")
        time.sleep(1)
        jogando()

    else:
        cenario = getCenario()
        print("Boa sorte!")
        time.sleep(1)
        cls()
        print("Carregando. \U000023F3")
        time.sleep(1)
        cls()
        print("Carregando.. \U000023F3")
        time.sleep(0.5)
        cls()
        print("Carregando... \U000023F3")
        time.sleep(0.5)
        cls()
        print("Tudo pronto? \U0000231B")
        time.sleep(0.5)
        mapa_com_bombas(cenario)
        time.sleep(3)
        jogando()


def seletorOpcoes(option):
    opcoes = ["I", "C", "L", "S"]
    timming = getTimming()
    while True:
        if option not in opcoes:
            print("Por favor selecione uma opção válida")
            option = str(input()).upper()
        else:
            if option == "I":
                if timming == 0:
                    comoJogar()
                time.sleep(2)
                iniciandoJogo()
                break
            if option == "L":
                print ("Carregando recursos.")
                time.sleep(1)
                print ("Carregando recursos.. \U000023F3")
                time.sleep(1)
                print ("Carregando recursos... \U000023F3")
                cls()
                loja()
                break
            if option == "C":
                iniciandoJogo()
                break
            if option == "S":
                print (getCoins())
                break


def menuInicial():
    print("◥▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀◤\n"
          "    Bem vindo ao MineWars!\n\n"
          "       ┃➲  🄸niciar jogo\n"
          "       ┃➲  🄲ontinuar?\n"
          "       ┃➲  🄻oja\n"
          "       ┃➲  🅂core\n\n"
          "       Você está pronto?\n"
          "◢▅▄▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▄▅◣")
    time.sleep(0.5)
    if(timming == 0):
        opcao = str(input("O que temos para hoje? ")).upper()
    else:
        opcao = str(input("Como posso ajudar dessa vez? ")).upper()
    cls()
    time.sleep(1)
    seletorOpcoes(opcao)

def loja():
    print("◥▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀◤\n"
          "         MineShopping!\n\n"
          "\n|| Você tem %d coins disponíveis\n  "
          "     \n-> (1) Show Bomb - 30 coins\n"
          "     \n-> (2) Reviver (consumível) - 3000 coins\n"
          "     \n-> (3) Stun - 60 coins\n"
          "     \n-> (R)etornar\n\n"
          "◢▅▄▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▄▅◣" % getCoins())
    opcao = str(input("| E aí, o que vai ser?\n")).upper()
    cls()
    manipulaLoja(opcao)


def manipulaLoja(opcao):
    opcoes = ["1", "2", "3", "R"]
    while opcao not in opcoes:
        print ("Por favor, selecione uma opcao válida (1, 2, 3, R)")
        opcao = str(input()).upper()

    if opcao == "R":
        menuInicial()

    if opcao == "1":
        preco = 1000
        item = "SB"
        validaCompra(preco, item)

    if opcao == "2":
        preco = 3000
        item = "REVIVER"
        validaCompra(preco, item)



def validaCompra(preco, item):
    coins = getCoins()
    if coins < preco:
        print("Você não possui dinheiro suficiente, jogue mais um pouco e retorne mais tarde...")
        time.sleep(3)
        cls()
    else:
        gastouCoins(preco)
        setPowerUps(item)
        time.sleep(1)
        print ("Compra efetuada com sucesso!")
        time.sleep(1.5)
        coins = getCoins()
        print ("Você possui %d coins após a sua compra" % coins)
        time.sleep(3)
        cls()


def terminou_partida():
    """
    funcao executada no fim de cada partida para questionar o jogador o que ele deseja fazer
    :param cenarioDaFase: recebido para fazer a varredura do mapa
    :return: void
    """
    limpaFase()
    opcao = str(input("Digite 1 para continuar e 2 para retornar ao menu: "))
    if opcao == "2":
        menuInicial()
    else:
        iniciandoJogo()

while True:
    """
    laco principal
    """
    menuInicial()
