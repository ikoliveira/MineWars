from partes_logicas import *


def cria_cenario_inimigo(pos_x, pos_y, tamanho):
    """
    funcao que cria um cenario (mapa) propriamente dito onde a partida acontecera
    :param pos_x: indica a posicao em que o jogador inicia o jogo
    :param pos_y: indica a posicao em que o inimigo inicia o jogo
    :param tamanho: Tamanho da matriz
    :return:
    """
    matriz_zerada = []
    cenario_introduzido = cria_matriz_inimigo(matriz_zerada, pos_x, pos_y, tamanho)  # cenario com caminho nao seguro
    caminho_analisado = analisa_caminho_inimigo(cenario_introduzido)
    caminho_livre = prepara_caminho(cenario_introduzido, caminho_analisado)
    return caminho_livre


def get_cenario_inimigo(pos_x, pos_y):
    """
    Função criada para retornar a criação do cenario inimigo.
    :param pos_x: lista indicando linha e coluna do personagem.
    :param pos_y: lista indicando linha e coluna do inimigo.
    :return: a função cria cenario com as informações necessárias.
    """
    return cria_cenario_inimigo(pos_x[1], pos_y[1], 20)


def cria_matriz_inimigo(lista_matriz, pos_x, pos_y, tamanho):
    """
    Serve para criar o mapa inimigo sem o caminho possível e coloca o personagem e o inimigo no mapa
    :param lista_matriz: Recebe uma matriz vazia para zerar.
    :param pos_x: número indicando a coluna do personagem.
    :param pos_y: número indicando a coluna do inimigo.
    :param tamanho: Tamanho da matriz criada.
    :return: retorna a lista matriz criada.
    """
    pos_x = [tamanho - 1, pos_x]
    lista_matriz = introduz_cenario(lista_matriz, pos_x, tamanho)
    lista_matriz[0][pos_y] = INIMIGO
    return lista_matriz


def analisa_caminho_inimigo(lista_matriz):
    """
    Este for em sua totalidade serve para armazenar os indices 0 (de cada linha)em uma lista para
    posteriormente ser escolhido de maneira aleatória e assim fazer um caminho entre as bombas.
    Essa função cria uma lista com os indices que irá servir para posteriomente ser criada o caminho possível.
    :param lista_matriz: A lista matriz que já passou pela função CriaMatrizInimigo
    :return: Retorna a lista com os indices
    """
    lista_indices = []
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
                if lista_matriz[linhas][colunas] == INIMIGO:
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
                if lista_matriz[linhas][colunas] == PERSONAGEM:
                    lista_indices.append(colunas)
                    break
    return lista_indices


def movimenta_inimigo(pos_x, pos_y, lista_matriz):
    """
    Essa função é responsável pela inteligência artificial do inimigo e além disso escolhe as posições possíveis para
    aproximação e em uma escolha aleatória movimenta o inimigo para uma posição mias proxima.
    :param pos_x: Posição do personagem
    :param pos_y: Posição do inimigo
    :param lista_matriz: O cenario a ser analisado e utilizado.
    :return:
    """
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
    if mov == 'W':
        lista_matriz[pos_y[0] - 1][pos_y[1]] = INIMIGO
        lista_matriz[pos_y[0]][pos_y[1]] = 0
        pos_y[0] = (pos_y[0] - 1)
    elif mov == 'S':
        lista_matriz[pos_y[0] + 1][pos_y[1]] = INIMIGO
        lista_matriz[pos_y[0]][pos_y[1]] = 0
        pos_y[0] = (pos_y[0] + 1)
    elif mov == 'A':
        lista_matriz[pos_y[0]][pos_y[1] - 1] = INIMIGO
        lista_matriz[pos_y[0]][pos_y[1]] = 0
        pos_y[1] = (pos_y[1] - 1)
    elif mov == 'D':
        lista_matriz[pos_y[0]][pos_y[1] + 1] = INIMIGO
        lista_matriz[pos_y[0]][pos_y[1]] = 0
        pos_y[1] = (pos_y[1] + 1)


def verifica_se_inimigo_matou(cenario, pos_x):
    """
    Essa função serve para indentificar se após a movimentaçõo do usuário e do inimigo se este(o personagem) não
    está em uma posição adjacente ao inimigo.
    :param cenario: Recebe a matriz referente ao cenário.
    :param pos_x: Posição do personagem.
    :return: retorna True para a validação em outra função.
    """
    if pos_x[0] != len(cenario) - 1:
        if cenario[pos_x[0] + 1][pos_x[1]] == INIMIGO:  # Verifica baixo
            return True
    if pos_x[0] != 0:
        if cenario[pos_x[0] - 1][pos_x[1]] == INIMIGO:  # Verifica cima
            return True
    if pos_x[1] != len(cenario) - 1:
        if cenario[pos_x[0]][pos_x[1] + 1] == INIMIGO:  # Verfica Direita
            return True
    if pos_x[1] != 0:
        if cenario[pos_x[0]][pos_x[1] - 1] == INIMIGO:  # Verifica Esquerda
            return True
