import random


def posicao_inicial(linha):
    """
        Função que exerce o papel de dar um índice possível inicial para ser utilizado
        posteriormente para a posição inicial de 'x'.
        :return: O valor entre 0 e 7
        """
    valor = random.randint(0, linha - 1)
    return valor


def zero_ou_um():
    """
    Função que exerce o papel de crial um valor randômico entre 0 e 1 para ser utilizado posteriormente
    na linha das matrizes criadas.
    :return:
    """
    valor = random.randint(0, 1)
    return valor


# posicao inicial = posicao do x advinda do main
# tamanho da matriz representa a fase do jogo
def criaCenarioInimigo(pos_x, pos_y, tamanho):
    matriz_zerada = []
    cenarioIntroduzido = CriaMatrizInimigo(matriz_zerada, pos_x, pos_y, tamanho)  # cenario com caminho nao seguro
    caminhoAnalisado = analisaCaminhoInimigo(
        cenarioIntroduzido)  # posicao das bombas para liberar o caminho para o personagem
    caminhoLivre = preparaCamiho(cenarioIntroduzido, caminhoAnalisado)
    return caminhoLivre


def CriaMatrizInimigo(lista_matriz, pos_x, pos_y, tamanho):
    linha_de_um = []
    for linha in range(tamanho):
        linhas = []
        for coluna in range(tamanho):
            linhas.append(zero_ou_um())
            if linha == 0:
                linha_de_um.append(1)
        while True:
            if linhas == linha_de_um:
                linhas = []
                for j in range(tamanho):
                    linhas.append(zero_ou_um())
            else:
                lista_matriz.append(linhas)
                break
    lista_matriz[tamanho - 1][pos_x] = 'x'
    lista_matriz[0][pos_y] = 'v'
    return lista_matriz


def analisaCaminhoInimigo(lista_matriz):
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
                if lista_matriz[linhas][colunas] == 'v':
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
        Neste for é onde acontece a substituição das bombas por zero para gerar o caminho do x de acordo com a escolha aleatória
        feita por x anteriormente
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


def validaMovimentacao(movimento, cenario, pos_x):
    """
    :param movimento: parametro a ser validado
    :param cenario: para analisar o mapa e tentar adivinhar o proximo movimento do x
    :param pos_x: naquele instante 't'
    :return: o input do movimento adequadamente atualizado
    """
    possibilities = ["W", "S", "A", "D"]
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


def verificaSeMorreu(movimento, lista_matriz, pos_x):
    '''
    analisa se a movimentacao escolhida pelo usuario fez com que ele morresse
    :param lista_matriz: cenario onde o personagem esta se movimentando
    :param pos_x: posicao de x para verificar se o personagem pisou na bomba
    :return: true se o personagem tiver sido explodido
    '''
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
    '''
    verifica se o jogador atingiu o topo do mapa em uma posicao segura
    :param lista_matriz: mapa da fase
    :return: true se tiver atingido, ou seja, vencido a fase
    '''
    for coluna in range(len(lista_matriz[0])):
        if lista_matriz[0][coluna] == "x":
            return True


def MovimentaInimigo(pos_x, pos_y, lista_matriz):
    lista_movimento = []
    if pos_y[1] < pos_x[1]:  # Direita
        lista_movimento.append("D")
    if pos_y[1] > pos_x[1]:  # Esquerda
        lista_movimento.append("A")
    if pos_y[0] < pos_x[0]:  # Baixo
        lista_movimento.append("S")
    if pos_y[0] > pos_x[0]:  # Cima
        lista_movimento.append("W")
    mov = random.choice(lista_movimento)
    print(mov)
    print(lista_movimento)
    if mov == 'W':
        lista_matriz[pos_y[0] - 1][pos_y[1]] = 'y'
        lista_matriz[pos_y[0]][pos_y[1]] = 0
        pos_y[0] = (pos_y[0] - 1)
    elif mov == 'S':
        lista_matriz[pos_y[0] + 1][pos_y[1]] = 'y'
        lista_matriz[pos_y[0]][pos_y[1]] = 0
        pos_y[0] = (pos_y[0] + 1)
    elif mov == 'A':
        lista_matriz[pos_y[0]][pos_y[1] - 1] = 'y'
        lista_matriz[pos_y[0]][pos_y[1]] = 0
        pos_y[1] = (pos_y[1] - 1)
    elif mov == 'D':
        lista_matriz[pos_y[0]][pos_y[1] + 1] = 'y'
        lista_matriz[pos_y[0]][pos_y[1]] = 0
        pos_y[1] = (pos_y[1] + 1)


tamanhoMatriz = 25
posicaoPersonagem = [tamanhoMatriz - 1, posicao_inicial(tamanhoMatriz)]
posicaoInimigo = [0, posicao_inicial(tamanhoMatriz)]
cenarioDaFase = criaCenarioInimigo(posicaoPersonagem[1], posicaoInimigo[1], tamanhoMatriz)


def MapaInimigo(cenario):
    for linha in range(len(cenario)):
        for coluna in range(len(cenario)):
            if cenario[linha][coluna] == 0:
                if coluna == (len(cenario) - 1):
                    print('\U0001F33F'.format(cenario))
                else:
                    print('\U0001F33F', end='')
            elif cenario[linha][coluna] == 1:
                if coluna == (len(cenario) - 1):
                    print('\U0001F4A3'.format(cenario))
                else:
                    print('\U0001F4A3', end='')
            elif cenario[linha][coluna] == 'x':
                if coluna == (len(cenario) - 1):
                    print('\U0001F3C7'.format(cenario))
                else:
                    print('\U0001F3C7', end='')
            else:
                if coluna == (len(cenario) - 1):
                    print('\U0001F47A'.format(cenario))
                else:
                    print('\U0001F47A', end='')


def verificaSeInimigoMatou(cenario, pos_x):
    if pos_x[0] != len(cenario) - 1:
        if cenario[pos_x[0] + 1][pos_x[1]] == 'y':  # Verifica baixo
            return True
    if pos_x[0] != 0:
        if cenario[pos_x[0] - 1][pos_x[1]] == 'y':  # Verifica cima
            return True
    if pos_x[1] != len(cenario) - 1:
        if cenario[pos_x[0]][pos_x[1] + 1] == 'y':  # Verfica Direita
            return True
    if pos_x[1] != 0:
        if cenario[pos_x[0]][pos_x[1] - 1] == 'y':  # Verifica Esquerda
            return True


def controlaPersonagem(movimentacao, lista_matriz, pos_x):
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


def joga(cenario, posicao_x, posicao_y):
    '''
    funcao que inicia o jogo propriamente dito, onde serao setados os movimentos e verificado se o jogador vence ou perde a partida.
    :param cenario: mapa da fase
    :param posicao: lugar onde o jogador inicia a partida
    :return: void
    '''
    while True:
        MapaInimigo(cenario)
        movimento = str(input()).upper()
        # se esquecer e precisar corrigir essa parte, basta excluir o intervalo de 95 - 99 linhas
        # que o codigo volta ao normal, com movimentacao adequada... lembrar de excluir o caput
        # da validacao

        movimento = validaMovimentacao(movimento, cenario, posicao_x)

        if verificaSeMorreu(movimento, cenario, posicao_x):
            MapaInimigo(cenario)
            print("Que pena...\nVocê perdeu, pisou na bomba!")
            break

        controlaPersonagem(movimento, cenario, posicao_x)
        if verificaSeInimigoMatou(cenario, posicao_x):
            MapaInimigo(cenario)
            print("O demônio te matou fela da puta")
            break

        MovimentaInimigo(posicao_x, posicao_y, cenario)
        if verificaSeInimigoMatou(cenario, posicao_x):
            MapaInimigo(cenario)
            print("O demônio te matou fela da puta")
            break

        if venceu(cenario):
            MapaInimigo(cenario)
            print("Congratulations!")
            break


joga(cenarioDaFase, posicaoPersonagem, posicaoInimigo)