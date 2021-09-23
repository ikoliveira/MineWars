# coding: utf-8
# projeto para a disciplina de programacao 1 do IFPB
# alunos: Diego Cardoso e Igor Kadson
import random


# metodo que basicamente retorna um valor entre 0 e 1 que sera utilizado na construcao das matrizes

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
    lista_matriz[pos_x[0]][pos_x[1]] = 'x'
    return lista_matriz


# metodo que guarda as posicoes seguras na matriz a serem utilizadas posteriormente na construcao do cenario com caminho seguro de bombas
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


# utiliza o caminho analisado para indexar as posicoes seguras na matriz do cenario principal, retorna a propria matriz
def preparaCamiho(lista_matriz, lista_indices):
    """
        Este é o método onde acontece a substituição das bombas por zero para gerar o caminho do x de acordo com a escolha aleatória
        feita pelo jogador
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
    '''
    verifica se o personagem esta tentando ultrapassar uma borda
    :param lista_matriz: cenario do jogo
    :param pos_x: onde o personagem se encontra no momento
    :return: true se o jogador esta tentando ultrapassar uma borda
    '''
    tentou_bordaBaixo = (pos_x[0] == len(lista_matriz) - 1)
    tentou_bordaDir = (pos_x[1] == 0)
    tentou_bordaE = (pos_x[1] == len(lista_matriz) - 1)

    if tentou_bordaDir or tentou_bordaE or tentou_bordaBaixo:
        return True


def verificaSeMorreu(movimento, lista_matriz, pos_x):
    '''
    analisa se a movimentacao escolhida pelo usuario fez com que ele morresse
    :param lista_matriz: cenario onde o personagem esta se movimentando
    :param pos_x: posicao de x para verificar se o personagem pisou na bomba
    :return: true se o personagem tiver sido explodido
    '''
    if (movimento == "W"):
        if (lista_matriz[pos_x[0] - 1][pos_x[1]] == 1):
            return True
    elif (movimento == "S"):
        if (lista_matriz[pos_x[0] + 1][pos_x[1]] == 1):
            return True
    elif (movimento == "A"):
        if (lista_matriz[pos_x[0]][pos_x[1] - 1] == 1):
            return True
    elif (movimento == "D"):
        if (lista_matriz[pos_x[0]][pos_x[1] + 1] == 1):
            return True


def venceu(lista_matriz):
    '''
    verifica se o jogador atingiu o topo do mapa em uma posicao segura
    :param lista_matriz: mapa da fase
    :return: true se tiver atingido, ou seja, vencido a fase
    '''
    for coluna in range(len(lista_matriz[0])):
        if lista_matriz[0][coluna] == "x":
            return True

def passou_fase(tamanhoMatriz):
    """
    essa funcao roda sempre que o jogador vence uma partida e passa de fase
    :return: void
    """
    faseFinal = 14
    if tamanhoMatriz < faseFinal:
        tamanhoMatriz += 2
    return tamanhoMatriz

def limpaFase():
    """
    funcao chamada para limpar o cenario e garantir que na proxima fase o jogador esteja na posicao correta
    :param posicaoPersonagem: indica a posicao atual do personagem, que pode ser preso em uma bomba ou na linha de chegada
    :param cenarioDaFase: mapa com as bombas atuais, que referem-se a fase que terminou de ser executada
    :return: void
    """
    global posicaoPersonagem
    global cenarioDaFase
    global tamanhoMatriz
    posicaoPersonagem.clear()
    cenarioDaFase.clear()
    posicaoPersonagem = resetaPosicao(tamanhoMatriz)
    cenarioDaFase = refazMapa(posicaoPersonagem, tamanhoMatriz)

def refazMapa(pos_x, fase):
    """
    cria um novo mapa ao fim de cada partida
    :param pos_x: posicao atual do personagem
    :param fase: mapa da partida
    :return:
    """
    novoCenario = criaCenario(pos_x, fase)
    return novoCenario


def resetaPosicao(pos_x):
    """
    seta uma nova posicao para o x
    :param pos_x: posical a ser indexada
    :return: arraylist representando a posical inicial do jogador
    """
    novaPosicao = [pos_x - 1, posicao_inicial(pos_x)]
    return novaPosicao


def joga():
    pass

def passouFase():
    global tamanhoMatriz
    global coins
    tamanhoMatriz += 1
    coins += 10


def getCenario():
    global cenarioDaFase
    return cenarioDaFase.copy()


def getPosicao():
    global posicaoPersonagem
    return posicaoPersonagem


def incrementa_vezesRodando():
    global timming
    timming += 1


def getTimming():
    global timming
    return timming

def getCoins():
    global coins
    return coins

def setPowerUps(power):
    global powerUps
    powerUps.append(power)

def getPowerUps():
    global powerUps
    return powerUps

############# VARIAVEIS GLOBAIS ######################

tamanhoMatriz = 4  # variavel sobrecarregada que indica o tamanho da matriz e define ao mesmo tempo a posicao inicial do personagem
posicaoPersonagem = [tamanhoMatriz - 1, posicao_inicial(tamanhoMatriz)]
cenarioDaFase = criaCenario(posicaoPersonagem, tamanhoMatriz)
timming = 0
coins = 0
powerUps = ["CAPUT"]
########################################################
