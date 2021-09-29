from PartesLogicas import *


def criaCenarioInimigo(pos_x, pos_y, tamanho):
    matriz_zerada = []
    cenarioIntroduzido = CriaMatrizInimigo(matriz_zerada, pos_x, pos_y, tamanho)  # cenario com caminho nao seguro
    caminhoAnalisado = analisaCaminhoInimigo(cenarioIntroduzido)
    caminhoLivre = preparaCamiho(cenarioIntroduzido, caminhoAnalisado)
    return caminhoLivre


def getCenarioInimigo(pos_x, pos_y):
    return criaCenarioInimigo(pos_x[1], pos_y[1], 20)


def CriaMatrizInimigo(lista_matriz, pos_x, pos_y, tamanho):
    pos_x = [tamanho - 1, pos_x]
    lista_matriz = introduzCenario(lista_matriz, pos_x, tamanho)
    lista_matriz[0][pos_y] = INIMIGO
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


def MapaInimigo(cenario):
    for linha in range(len(cenario)):
        for coluna in range(len(cenario)):
            if cenario[linha][coluna] == 0:
                if coluna == (len(cenario) - 1):
                    print(MATO.format(cenario))
                else:
                    print(MATO, end='')
            elif cenario[linha][coluna] == 1:
                if coluna == (len(cenario) - 1):
                    print(BOMBA.format(cenario))
                else:
                    print(BOMBA, end='')
            elif cenario[linha][coluna] == PERSONAGEM:
                if coluna == (len(cenario) - 1):
                    print(getEmoji().format(cenario))
                else:
                    print(getEmoji(), end='')
            else:
                if coluna == (len(cenario) - 1):
                    print(CAPETA.format(cenario))
                else:
                    print(CAPETA, end='')


def verificaSeInimigoMatou(cenario, pos_x):
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
