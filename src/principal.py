# coding: utf-8
# projeto para a disciplina de programacao 1 do IFPB
# alunos: Diego Cardoso e Igor Kadson
# este modulo funciona como uma interface de interação entre o usuario e as partes logicas do jogo, pode ser facilmente substituido por uma interfaces
# grafica que quiçá será implementada futuramente

import time

from PartesLogicas import *
import os

# metodo chave que sorteia a posicao inicial do x a ser inserido na linha ultima linha da matriz, coluna qualquer
def posicao_inicial(linha):
    """
        Função que exerce o papel de dar um índice possível inicial para ser utilizado
        posteriormente para a posição inicial de 'x'.
        :return: O valor entre 0 e 7
        """
    valor = random.randint(0, linha - 1)
    return valor


tamanhoMatriz = 10 # variavel sobrecarregada que indica o tamanho da matriz e define ao mesmo tempo a posicao inicial do personagem

posicaoPersonagem = [tamanhoMatriz - 1, posicao_inicial(tamanhoMatriz)]
cenarioDaFase = criaCenario(posicaoPersonagem, tamanhoMatriz)
# mapaInimigo = criaCenarioInimigo(posicao_inicial(20), posicao_inicial(20), 20)


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


def cls():
    """
    funcao que limpa o terminal sempre que invocada
    :return: void
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def joga(cenario, posicao):

    '''
    funcao que inicia o jogo propriamente dito, onde serao setados os movimentos e verificado se o jogador vence ou perde a partida.
    :param cenario: mapa da fase
    :param posicao: lugar onde o jogador inicia a partida
    :return: void
    '''
    global tamanhoMatriz
    while True:
        cls()
        mapaReal(cenario)
        movimento = str(input()).upper()
        #se esquecer e precisar corrigir essa parte, basta excluir o intervalo de 95 - 99 linhas
        #que o codigo volta ao normal, com movimentacao adequada... lembrar de excluir o caput
        # da validacao
        if(movimento == "CAPUT"):
            cls()
            mapa_com_bombas(cenario)
            movimentos = str(input()).upper()
            movimento = validaMovimentacao(movimentos, cenario, posicao)
        else:
            movimento = validaMovimentacao(movimento, cenario, posicao)

        if verificaSeMorreu(movimento, cenario, posicao):
            cls()
            mapa_com_bombas(cenario)
            print("Que pena...\nVocê perdeu!")
            time.sleep(5)
            cls()
            break

        controlaPersonagem(movimento, cenario, posicao)

        if venceu(cenario):
            print("Congratulations!")
            tamanhoMatriz = passou_fase(tamanhoMatriz)
            time.sleep(3)
            cls()
            break


def validaMovimentacao(movimento, cenario, pos_x):
    """
    :param movimento: parametro a ser validado
    :param cenario: para analisar o mapa e tentar adivinhar o proximo movimento do x
    :param pos_x: naquele instante 't'
    :return: o input do movimento adequadamente atualizado
    """
    possibilities = ["W", "S", "A", "D", "CAPUT"]
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


def iniciandoJogo(cenario):
    """
    imprime a primeira tela que o jogador vera, mostrando as bombas e caminhos livres. apos 6s, o cenario eh ocultado
    :param cenario: mapa da fase "cru" a ser printado na tela com as bombas
    :return: void, printa o mapa
    """

    print("\nVocê está preparado?\n")
    time.sleep(1)
    mapa_com_bombas(cenario)
    time.sleep(4)
    print("\nSerá mesmo??????")
    time.sleep(1)
    joga(cenarioDaFase, posicaoPersonagem)


def comoJogar():
    while True:
        print("Deseja aprender como jogar?")
        resposta = str(input()).lower()
        if (resposta == "não" or resposta == "n"):
            break
        else:
            print("regras do jogo: blablala")


def seletorOpcoes(option):
    opcoes = ["I", "C", "L", "S"]
    while True:
        if option not in opcoes:
            print("Por favor selecione uma opção válida")
            option = str(input())
        else:
            if option == "I":
                comoJogar()
                time.sleep(2)
                iniciandoJogo(cenarioDaFase)
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
    time.sleep(3)
    opcao = str(input("O que temos para hoje? ")).upper()
    cls()
    time.sleep(1)
    seletorOpcoes(opcao)


while True:
    menuInicial()
    posicaoPersonagem.clear()
    posicaoPersonagem = [tamanhoMatriz - 1, posicao_inicial(tamanhoMatriz)]
    cenarioDaFase.clear()
    cenarioDaFase = criaCenario(posicaoPersonagem, tamanhoMatriz)
    