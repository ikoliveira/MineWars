# import random
#
#
# def posicao_inicial(linha):
#     """
#         Função que exerce o papel de dar um índice possível inicial para ser utilizado
#         posteriormente para a posição inicial de 'x'.
#         :return: O valor entre 0 e 7
#         """
#     valor = random.randint(0, linha - 1)
#     return valor
#
#
# def zero_ou_um():
#     """
#     Função que exerce o papel de crial um valor randômico entre 0 e 1 para ser utilizado posteriormente
#     na linha das matrizes criadas.
#     :return:
#     """
#     valor = random.randint(0, 1)
#     return valor
#
# CONST = 20
#
#
# # posicao inicial = posicao do x advinda do main
# # tamanho da matriz representa a fase do jogo
# def criaCenarioInimigo(pos_x, pos_y, tamanho):
#     matriz_zerada = []
#     cenarioIntroduzido = CriaMatrizInimigo(matriz_zerada, pos_x, pos_y, tamanho)  # cenario com caminho nao seguro
#     caminhoAnalisado = analisaCaminhoInimigo(
#         cenarioIntroduzido)  # posicao das bombas para liberar o caminho para o personagem
#     caminhoLivre = preparaCamiho(cenarioIntroduzido, caminhoAnalisado)
#     return caminhoLivre
#
#
# def CriaMatrizInimigo(lista_matriz, pos_x, pos_y, tamanho):
#     linha_de_um = []
#     for linha in range(tamanho):
#         linhas = []
#         for coluna in range(tamanho):
#             linhas.append(zero_ou_um())
#             if linha == 0:
#                 linha_de_um.append(1)
#         while True:
#             if linhas == linha_de_um:
#                 linhas = []
#                 for j in range(tamanho):
#                     linhas.append(zero_ou_um())
#             else:
#                 lista_matriz.append(linhas)
#                 break
#     lista_matriz[tamanho - 1][pos_x] = 'x'
#     lista_matriz[0][pos_y] = 'v'
#     return lista_matriz
#
#
# def analisaCaminhoInimigo(lista_matriz):
#     lista_indices = []
#     """
#     Este for em sua totalidade serve para armazenar os indices 0 (de cada linha)em uma lista para
#     posteriormente ser escolhido de maneira aleatória e assim fazer um caminho entre as bombas.
#     """
#     for linhas in range(len(lista_matriz)):
#         indices_zeros = []
#         # um for destinado para criar uma lista onde fica armazenado o indices do zero em cada linha
#         for colunas_para_zeros in range(len(lista_matriz[linhas])):
#             if linhas != (len(lista_matriz) - 1):
#                 if lista_matriz[linhas][colunas_para_zeros] == 0:
#                     indices_zeros.append(colunas_para_zeros)
#
#         for colunas in range(len(lista_matriz[linhas])):
#             # Nesta condição informa qual o primeiro zero da linha 0 e armazena na (indice_zero)
#             if linhas == 0:
#                 if lista_matriz[linhas][colunas] == 'v':
#                     lista_indices.append(colunas)
#                     break
#             # Nesta condição foi utilizada a lista de indices zeros na lista para ser selecionado aleatoriamente
#             # para ser o caminho de x até a linha de chegada.
#             if 0 < linhas < (len(lista_matriz) - 1):
#                 indice_aleatorio = random.choice(indices_zeros)
#                 lista_indices.append(indice_aleatorio)
#                 break
#
#             # Esta condição serve para colocar a posição do 'x' como último indice da lista lista_indices
#             elif linhas == (len(lista_matriz) - 1):
#                 if lista_matriz[linhas][colunas] == 'x':
#                     lista_indices.append(colunas)
#                     break
#     return lista_indices
#
#
# def preparaCamiho(lista_matriz, lista_indices):
#     """
#         Neste for é onde acontece a substituição das bombas por zero para gerar o caminho do x de acordo com a escolha aleatória
#         feita por x anteriormente
#         """
#     for linha in range(len(lista_matriz)):
#         for coluna in range(len(lista_matriz)):
#             if linha != 0:
#                 if lista_indices[linha - 1] > lista_indices[linha]:
#                     if lista_indices[linha] < coluna <= lista_indices[linha - 1]:
#                         lista_matriz[linha].insert(coluna, 0)
#                         lista_matriz[linha].pop(coluna + 1)
#
#                 else:
#                     if lista_indices[linha - 1] <= coluna < lista_indices[linha]:
#                         lista_matriz[linha].insert(coluna, 0)
#                         lista_matriz[linha].pop(coluna + 1)
#     return lista_matriz
#
#
# x = criaCenarioInimigo(posicao_inicial(20), posicao_inicial(20), 20)
#
# for linha in range(len(x)):
#     for coluna in range(len(x)):
#         if x[linha][coluna] == 0:
#             if coluna == (len(x) - 1):
#                 print('\U0001F33F'.format(x))
#             else:
#                 print('\U0001F33F', end='')
#         elif x[linha][coluna] == 1:
#             if coluna == (len(x) - 1):
#                 print('\U0001F4A3'.format(x))
#             else:
#                 print('\U0001F4A3', end='')
#         elif x[linha][coluna] == 'x':
#             if coluna == (len(x) - 1):
#                 print('\U0001F46E'.format(x))
#             else:
#                 print('\U0001F46E', end='')
#         else:
#             if coluna == (len(x) - 1):
#                 print('\U0001F479'.format(x))
#             else:
#                 print('\U0001F479', end='')