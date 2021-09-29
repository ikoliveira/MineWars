# coding: utf-8
# projeto para a disciplina de programacao 1 do IFPB
# alunos: Diego Cardoso e Igor Kadson
import random
from constantes import *
import configparser
import copy
import time

def posicao_inicial(linha):
    """
        Função que exerce o papel de dar um índice possível inicial para ser utilizado
        posteriormente para a posição inicial de 'x'.
        :return: O valor entre 0 e 7
        """
    valor = random.randint(0, linha - 1)
    return valor


def criaCenario(pos_x, fase):
    """
    funcao que cria um cenario (mapa) propriamente dito onde a partida acontecera
    :param pos_x: indica a posicao em que o jogador inicia o jogo
    :param fase: matriz que define o tamanho da fase.
    :return: uma matriz de tamanho x indicado pela fase
    """
    matriz_zerada = []
    cenarioIntroduzido = introduzCenario(matriz_zerada, pos_x, fase)  # cenario com caminho nao seguro
    caminhoAnalisado = analisaCaminho(cenarioIntroduzido)  # posicao das bombas para liberar o caminho para o personagem
    caminhoLivre = preparaCamiho(cenarioIntroduzido, caminhoAnalisado)
    return caminhoLivre


def zero_ou_um():
    """
    Função que exerce o papel de crial um valor randômico entre 0 e 1 para ser utilizado posteriormente
    na linha das matrizes criadas.
    :return: int
    """
    valor = random.randint(0, 1)
    return valor


def introduzCenario(lista_matriz, pos_x, fase):
    """
    cria a matriz indexando a posicao do jogador no mapa.
    :param lista_matriz: a lista onde o mapa sera armazenado
    :param pos_x: posicao inicial onde o jogador sera indexado
    :param fase: mapa da fase
    :return: arraylist
    """
    linha_de_um = []
    for linha in range(fase):
        linhas = []
        for coluna in range(fase):
            linhas.append(zero_ou_um())
            if linha == 0:
                linha_de_um.append(1)
        while True:
            if linhas == linha_de_um:
                linhas = []
                for j in range(fase):
                    linhas.append(zero_ou_um())
            else:
                lista_matriz.append(linhas)
                break
    lista_matriz[pos_x[0]][pos_x[1]] = PERSONAGEM
    return lista_matriz


def analisaCaminho(lista_matriz):
    lista_indices = []
    """
    Este for em sua totalidade serve para armazenar os indices 0 (de cada linha)em uma lista para 
    posteriormente ser escolhido de maneira aleatória e assim fazer um caminho entre as bombas. 
    """
    for linhas in range(len(lista_matriz)):
        indices_zeros = []
        # um for destinado para criar uma lista onde fica armazenado o indices do zero em cada linha
        for colunas_para_zeros in range(len(lista_matriz[linhas])):
            if linhas != (len(lista_matriz) - 1):
                if lista_matriz[linhas][colunas_para_zeros] == 0:
                    indices_zeros.append(colunas_para_zeros)

        for colunas in range(len(lista_matriz[linhas])):
            # Nesta condição informa qual o primeiro zero da linha 0 e armazena na (indice_zero)
            if linhas == 0:
                if lista_matriz[linhas][colunas] == 0:
                    lista_indices.append(colunas)
                    break
            # Nesta condição foi utilizada a lista de indices zeros na lista para ser selecionado aleatoriamente
            # para ser o caminho de x até a linha de chegada.
            if 0 < linhas < (len(lista_matriz) - 1):
                indice_aleatorio = random.choice(indices_zeros)
                lista_indices.append(indice_aleatorio)
                break

            # Esta condição serve para colocar a posição do 'x' como último indice da lista lista_indices
            elif linhas == (len(lista_matriz) - 1):
                if lista_matriz[linhas][colunas] == 'x':
                    lista_indices.append(colunas)
                    break
    return lista_indices


def preparaCamiho(lista_matriz, lista_indices):
    """
    abre a matriz para garantir que exista ao menos um caminho livre
    :param lista_matriz: mapa
    :param lista_indices:
    :return:
    """
    for linha in range(len(lista_matriz)):
        for coluna in range(len(lista_matriz)):
            if linha != 0:
                if lista_indices[linha - 1] > lista_indices[linha]:
                    if lista_indices[linha] < coluna <= lista_indices[linha - 1]:
                        lista_matriz[linha].insert(coluna, 0)
                        lista_matriz[linha].pop(coluna + 1)
                else:
                    if lista_indices[linha - 1] <= coluna < lista_indices[linha]:
                        lista_matriz[linha].insert(coluna, 0)
                        lista_matriz[linha].pop(coluna + 1)
    return lista_matriz


def controlaPersonagem(movimentacao, lista_matriz, pos_x):
    """
    causa o efeito de movimento na partida
    :param movimentacao: a string que indica a direcao do personagem
    :param lista_matriz: mapa da fase
    :param pos_x: posical atual do jogador
    :return: void
    """
    if movimentacao == 'W':
        lista_matriz[pos_x[0] - 1][pos_x[1]] = 'x'
        lista_matriz[pos_x[0]][pos_x[1]] = 0
        pos_x[0] = (pos_x[0] - 1)

    elif movimentacao == 'S':
        lista_matriz[pos_x[0] + 1][pos_x[1]] = 'x'
        lista_matriz[pos_x[0]][pos_x[1]] = 0
        pos_x[0] = (pos_x[0] + 1)

    elif movimentacao == 'A':
        lista_matriz[pos_x[0]][pos_x[1] - 1] = 'x'
        lista_matriz[pos_x[0]][pos_x[1]] = 0
        pos_x[1] = (pos_x[1] - 1)

    elif movimentacao == 'D':
        lista_matriz[pos_x[0]][pos_x[1] + 1] = 'x'
        lista_matriz[pos_x[0]][pos_x[1]] = 0
        pos_x[1] = (pos_x[1] + 1)


def posicaoInvalida(lista_matriz, pos_x):
    """
    verifica se o personagem esta tentando ultrapassar uma borda
    :param lista_matriz: cenario do jogo
    :param pos_x: onde o personagem se encontra no momento
    :return: true se o jogador esta tentando ultrapassar uma borda
    """
    tentou_bordaBaixo = (pos_x[0] == len(lista_matriz) - 1)
    tentou_bordaDir = (pos_x[1] == 0)
    tentou_bordaE = (pos_x[1] == len(lista_matriz) - 1)

    if tentou_bordaDir or tentou_bordaE or tentou_bordaBaixo:
        return True


def verificaSeMorreu(movimento, lista_matriz, pos_x):
    """
    indexa a matriz verificando se o jogador pisou em uma bomba
    :param movimento: indica a posicao da jogada
    :param lista_matriz: mapa iteravel
    :param pos_x: posicao atual do jogador
    :return: true se tiver pisado em uma bomba
    """
    if movimento == "W":
        if lista_matriz[pos_x[0] - 1][pos_x[1]] == 1:
            return True
    elif movimento == "S":
        if lista_matriz[pos_x[0] + 1][pos_x[1]] == 1:
            return True
    elif movimento == "A":
        if lista_matriz[pos_x[0]][pos_x[1] - 1] == 1:
            return True
    elif movimento == "D":
        if lista_matriz[pos_x[0]][pos_x[1] + 1] == 1:
            return True


def venceu(lista_matriz):
    """
    verifica se o jogador atingiu o topo do mapa em uma posicao segura
    :param lista_matriz: mapa da fase
    :return: true se tiver atingido, ou seja, vencido a fase
    """
    for coluna in range(len(lista_matriz[0])):
        if lista_matriz[0][coluna] == "x":
            return True


def passou_fase(tamanhomatriz):
    """
    essa funcao roda sempre que o jogador vence uma partida e passa de fase
    :return: void
    """
    faseFinal = 14
    if tamanhomatriz < faseFinal:
        tamanhomatriz += 1
    return tamanhomatriz


def limpaFase():
    """
    funcao chamada para limpar o cenario e garantir que na proxima fase o jogador esteja na posicao correta
    :return: void, apenas varre a fase e reestabelece as posicoes
    """
    global posicaopersonagem
    global cenarioDaFase
    global tamanho_matriz
    posicaopersonagem.clear()
    cenarioDaFase.clear()
    posicaopersonagem = resetaPosicaoJogador()
    cenarioDaFase = refazMapa(posicaopersonagem, tamanho_matriz)


def limpaJogoInimigo():
    posInimi = getPosicaoInimigo()
    posPerso = get_posicao()
    posInimi.clear()
    posPerso.clear()


def preparaPosicoes():
    limpaJogoInimigo()
    global posicaopersonagem
    global posicaoInimigo
    global posInitModInim
    posicaopersonagem = [posInitModInim - 1, posicao_inicial(tamanho_matriz)]
    posicaoInimigo = [0, posicao_inicial(tamanho_matriz)]


def refazMapa(pos_x, fase):
    """
    cria um novo mapa ao fim de cada partida
    :param pos_x: posicao atual do personagem
    :param fase: mapa da partida
    :return:
    """
    novoCenario = criaCenario(pos_x, fase)
    return novoCenario


def resetaPosicaoJogador():
    """
    reseta uma nova posicao para o x
    :return: arraylist representando a posical inicial do jogador
    """
    global tamanho_matriz
    novaPosicao = [tamanho_matriz - 1, posicao_inicial(tamanho_matriz)]
    return novaPosicao


def passouFase(moedasganhas):
    """
    roda sempre que o jogador passa de fase e incrementa a fase
    :param moedasganhas: quantidade de moedas ganhas
    :return: void, causa alteracoes nas variaveis globais
    """
    global tamanho_matriz
    tamanho_matriz += 1
    somaCoins(moedasganhas)
    somaCoinsTotais(moedasganhas)


def get_cenario():
    global cenarioDaFase
    return cenarioDaFase.copy()


def get_posicao():
    global posicaopersonagem
    return posicaopersonagem


def incrementa_vezesRodando():
    global qtd_vezes
    qtd_vezes += 1


def getTimming():
    global qtd_vezes
    return qtd_vezes

def setTimming(timm):
    global qtd_vezes
    qtd_vezes = int(timm)

def getCoins():
    global coins
    return coins


def somaCoins(valor):
    global coins
    coins += valor

def setCoins(valo):
    global coins
    coins = int(valo)


def gastouCoins(valor):
    global coins
    coins -= valor


def getCoinsTotais():
    global coins_totais
    return coins_totais


def somaCoinsTotais(valor):
    global coins_totais
    coins_totais += valor

def setCoinsTotais(va):
    global coins_totais
    coins_totais = int(va)


def setPowerUps(power):
    global powerUps
    powerUps.append(power)


def getPowerUps():
    global powerUps
    return powerUps


def getPosicaoInimigo():
    global posicaoInimigo
    return posicaoInimigo


def getFase():
    global tamanho_matriz
    return tamanho_matriz

def setFase(val):
    global tamanho_matriz
    tamanho_matriz = int(val)

def setUsuario(nomeUsuario,):
    global usuario
    usuario = nomeUsuario



def setEmoji(emoti):
    global emoji
    emoji = emoti

def getUsuario():
    global usuario
    return usuario


def zerou():
    if getFase() >= 14:
        return True


def organizaUsuario(nome, emoticon):
    emote = ""
    if emoticon == "1":
        emote = MACACO
    elif emoticon == "2":
        emote = GATO
    elif emoticon == "3":
        emote = ET
    elif emoticon == "4":
        emote = CAVALO
    elif emoticon == "5":
        emote = UNICORNIO
    setUsuario(nome)
    setEmoji(emote)


def getEmoji():
    global emoji
    return emoji


def novaCampanha():
    global tamanho_matriz
    tamanho_matriz = 4
    limpaFase()


def salvarProgresso(save_name):
    template_save = {"usuario": getUsuario(), "emoji": getEmoji(), "tamanho_matriz": getFase(), "qtd_vezes": getTimming(), "coins": getCoins(), "coins_totais": getCoinsTotais()}
    config.read("save.ini")
    config[save_name] = copy.deepcopy(template_save)
    with open("save.ini", "w") as save_file:
        config.write(save_file)


def carregarProgresso(nome_usuario):
    config.read("save.ini")
    time.sleep(3)
    if nome_usuario in config:
        setUsuario(config[nome_usuario].get("usuario"))
        setEmoji(config[nome_usuario].get("emoji"))
        setFase(config[nome_usuario].get("tamanho_matriz"))
        setTimming(config[nome_usuario].get("qtd_vezes"))
        setCoins(config[nome_usuario].get("coins"))
        setCoinsTotais(config[nome_usuario].get("coins_totais"))


tamanho_matriz = 4
posInitModInim = 20
posicaopersonagem = [tamanho_matriz - 1, posicao_inicial(tamanho_matriz)]
posicaoInimigo = [0, posicao_inicial(tamanho_matriz)]
cenarioDaFase = criaCenario(posicaopersonagem, tamanho_matriz)
qtd_vezes = 0
coins = 0
coins_totais = 0
powerUps = []
usuario = "user"
emoji = "\U0001F3C7"
config = configparser.ConfigParser()