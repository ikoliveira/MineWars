# coding: utf-8
# projeto para a disciplina de programacao 1 do IFPB
# alunos: Diego Cardoso e Igor Kadson

import configparser
import copy
import random
import time

from constantes import *


def posicao_inicial(linha):
    """
        Função que exerce o papel de dar um índice possível inicial para ser utilizado.
        posteriormente para a posição inicial de 'x'.
        :return: O valor entre 0 e 7.
        """
    valor = random.randint(0, linha - 1)
    return valor


def cria_cenario(pos_x, fase):
    """
    Funcao que cria um cenario (mapa) propriamente dito onde a partida acontecera.
    :param pos_x: indica a posicao em que o jogador inicia o jogo.
    :param fase: matriz que define o tamanho da fase..
    :return: uma matriz de tamanho x indicado pela fase.
    """
    matriz_zerada = []
    cenario_introduzido = introduz_cenario(matriz_zerada, pos_x, fase)  # cenario com caminho nao seguro
    caminho_analisado = analisa_caminho(cenario_introduzido)  # posicao das bombas para liberar o caminho
    # para o personagem
    caminho_livre = prepara_caminho(cenario_introduzido, caminho_analisado)
    return caminho_livre


def zero_ou_um():
    """
    Função que exerce o papel de crial um valor randômico entre 0 e 1 para ser utilizado posteriormente.
    na linha das matrizes criadas.
    :return: int.
    """
    valor = random.randint(0, 1)
    return valor


def introduz_cenario(lista_matriz, pos_x, fase):
    """
    Cria a matriz indexando a posicao do jogador no mapa.
    :param lista_matriz: a lista onde o mapa sera armazenado.
    :param pos_x: posicao inicial onde o jogador sera indexado.
    :param fase: mapa da fase.
    :return: arraylist.
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


def analisa_caminho(lista_matriz):
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


def prepara_caminho(lista_matriz, lista_indices):
    """
    Abre a matriz para garantir que exista ao menos um caminho livre.
    :param lista_matriz: mapa.
    :param lista_indices:
    :return: Void.
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


def controla_personagem(movimentacao, lista_matriz, pos_x):
    """
    causa o efeito de movimento na partida
    :param movimentacao: a string que indica a direcao do personagem
    :param lista_matriz: mapa da fase
    :param pos_x: posical atual do jogador
    :return: void
    """
    if movimentacao == 'W':
        lista_matriz[pos_x[0] - 1][pos_x[1]] = PERSONAGEM
        lista_matriz[pos_x[0]][pos_x[1]] = 0
        pos_x[0] = (pos_x[0] - 1)

    elif movimentacao == 'S':
        lista_matriz[pos_x[0] + 1][pos_x[1]] = PERSONAGEM
        lista_matriz[pos_x[0]][pos_x[1]] = 0
        pos_x[0] = (pos_x[0] + 1)

    elif movimentacao == 'A':
        lista_matriz[pos_x[0]][pos_x[1] - 1] = PERSONAGEM
        lista_matriz[pos_x[0]][pos_x[1]] = 0
        pos_x[1] = (pos_x[1] - 1)

    elif movimentacao == 'D':
        lista_matriz[pos_x[0]][pos_x[1] + 1] = PERSONAGEM
        lista_matriz[pos_x[0]][pos_x[1]] = 0
        pos_x[1] = (pos_x[1] + 1)


def posicao_invalida(lista_matriz, pos_x):
    """
    verifica se o personagem esta tentando ultrapassar uma borda
    :param lista_matriz: cenario do jogo
    :param pos_x: onde o personagem se encontra no momento
    :return: true se o jogador esta tentando ultrapassar uma borda
    """
    tentou_borda_baixo = (pos_x[0] == len(lista_matriz) - 1)
    tentou_borda_dir = (pos_x[1] == 0)
    tentou_borda_e = (pos_x[1] == len(lista_matriz) - 1)

    if tentou_borda_dir or tentou_borda_e or tentou_borda_baixo:
        return True


def verifica_se_morreu(movimento, lista_matriz, pos_x):
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


def passou_de_fase(tamanho_m):
    """
    essa funcao roda sempre que o jogador vence uma partida e passa de fase
    :return: void
    """
    fase_final = 14
    if tamanho_m < fase_final:
        tamanho_m += 1
    return tamanho_m


def limpa_fase():
    """
    funcao chamada para limpar o cenario e garantir que na proxima fase o jogador esteja na posicao correta
    :return: void, apenas varre a fase e reestabelece as posicoes
    """
    global posicao_personagem
    global cenario_da_fase
    global tamanho_matriz
    posicao_personagem.clear()
    cenario_da_fase.clear()
    posicao_personagem = reseta_posicao_jogador()
    cenario_da_fase = refaz_mapa(posicao_personagem, tamanho_matriz)


def limpa_jogo_inimigo():
    """
    Serve para dar um clear na posição do inimigo e do personagem para evitar bug's.
    :return: Listas dos personagens limpas.
    """
    pos_inimi = get_posicao_inimigo()
    pos_perso = get_posicao()
    pos_inimi.clear()
    pos_perso.clear()


def prepara_posicoes():
    """
    Pega as globais referente a posição do personagem e do inimigo e adiciona uma nova posição para as tais.
    :return: Nova posição do inimigo e personagem.
    """
    limpa_jogo_inimigo()
    global posicao_personagem
    global posicao_inimigo
    global pos_init_mod_inim
    posicao_personagem = [pos_init_mod_inim - 1, posicao_inicial(tamanho_matriz)]
    posicao_inimigo = [0, posicao_inicial(tamanho_matriz)]


def refaz_mapa(pos_x, fase):
    """
    Cria um novo mapa ao fim de cada partida.
    :param pos_x: posicao atual do personagem.
    :param fase: mapa da partida.
    :return: O novo cenario criado para ser utilizado.
    """
    novo_cenario = cria_cenario(pos_x, fase)
    return novo_cenario


def reseta_posicao_jogador():
    """
    Reseta uma nova posicao para o x.
    :return: arraylist representando a posical inicial do jogador.
    """
    global tamanho_matriz
    nova_posicao = [tamanho_matriz - 1, posicao_inicial(tamanho_matriz)]
    return nova_posicao


def passou_fase(moedas_ganhas):
    """
    Roda sempre que o jogador passa de fase e incrementa a fase.
    :param moedas_ganhas: quantidade de moedas ganhas.
    :return: void, causa alteracoes nas variaveis globais.
    """
    global tamanho_matriz
    tamanho_matriz += 1
    soma_coins(moedas_ganhas)
    soma_coins_totais(moedas_ganhas)


def get_cenario():
    """
    Recupera o cenário e retorna como global.
    :return: A variável onde o cenario está armazenado.
    """
    global cenario_da_fase
    return cenario_da_fase.copy()


def get_posicao():
    """
    Recupera a posição e retorna como global.
    :return: A variável onde a posição está armazenada.
    """
    global posicao_personagem
    return posicao_personagem


def incrementa_vezes_rodando():
    """
    Esta função serve para adicionar a quantidade de vezes que o usuário jogou alguma partida.
    :return: A variável qtd_vezes com os pontos adicionados.
    """
    global qtd_vezes
    qtd_vezes += 1


def get_timming():
    """
    Recupera a qtd_vezes e retorna como global.
    :return: A variável onde a qtd_vezes está armazenada.
    """
    global qtd_vezes
    return qtd_vezes


def loading_timming(timm):
    """
    Executada quando é feito o carregamento de um perfil e o transforma em inteiro para incrementação em jogo.
    :param timm: Timming recebido na entrada.
    :return: Transforma o Timming em inteiro.
    """
    global qtd_vezes
    qtd_vezes = int(timm)


def get_coins():
    """
    Recupera os coins e retorna como global.
    :return: A variável onde os coins estão armazenados.
    """
    global coins
    return coins


def soma_coins(valor):
    """
    Soma a variável global coins com o valor recebido nos jogos.
    :param valor: coins recebidos nos códigos.
    :return: O coins adicionados.
    """
    global coins
    coins += valor


def set_coins(valor):
    """
    Executada quando é feito o carregamento de um perfil e o transforma em inteiro para incrementação em jogo.
    :param valor: Valor recebido na entrada.
    :return: Transforma o valor em inteiro.
    """
    global coins
    coins = int(valor)


def gastou_coins(valor):
    """
    Função que diminui a variável global coins se algum coin for gastado.
    :param valor: O valor a ser gasto
    :return: o valor diminuido
    """
    global coins
    coins -= valor


def get_coins_totais():
    """
    Recupera os coins Totais e retorna como global.
    :return: A variável onde os coins Totais estão armazenados.
    """
    global coins_totais
    return coins_totais


def soma_coins_totais(valor):
    """
    Soma a variável global coins Totais com o valor recebido nos jogos.
    :param valor: coins recebidos nos códigos.
    :return: O coins adicionados.
    """
    global coins_totais
    coins_totais += valor


def set_coins_totais(va):
    """
    Executada quando é feito o carregamento de um perfil e o transforma em inteiro para incrementação em jogo.
    :param va: Valor recebido na entrada.
    :return: Transforma o valor em inteiro.
    """
    global coins_totais
    coins_totais = int(va)


def set_power_ups(power):
    """
    Função utilizada para incrementar o powerup comprado na loja na variável global.
    :param power: O poder comprado.
    :return: o powerup na lista de powerup's comprados.
    """
    global power_ups
    power_ups.append(power)


def get_power_ups():
    """
    Recupera os PowerUps e retorna como global.
    :return: A variável onde os PowerUps estão armazenados.
    """
    global power_ups
    return power_ups


def get_posicao_inimigo():
    """
    Recupera a posição do inimigo e retorna como global.
    :return: A variável onde a posição do inimigo está armazenada.
    """
    global posicao_inimigo
    return posicao_inimigo


def get_fase():
    """
    Recupera a posição do inimigo e retorna como global.
    :return: A variável onde a posição do inimigo está armazenada.
    """
    global tamanho_matriz
    return tamanho_matriz


def set_fase(val):
    """
    Executada quando é feito o carregamento de um perfil e o transforma em inteiro para incrementação em jogo.
    :param val: Valor recebido na entrada.
    :return: Transforma o valor em inteiro.
    """
    global tamanho_matriz
    tamanho_matriz = int(val)


def set_usuario(nome_usuario):
    """
    Recebe o nome do usuário escolhido na parte de escolha dos perfis e o coloca como a variável global
    respectiva aos perfis.
    :param nome_usuario: Nome que o usuário colocou.
    :return: O nome do usuário modificado.
    """
    global usuario
    usuario = nome_usuario


def set_emoji(emoti):
    """
    Recebe o emoji do usuário escolhido na parte de escolha dos perfis e o coloca como a variável global
    respectiva aos emojis.
    :param emoti: Emoji que o usuário colocou.
    :return: O emoji do usuário modificado.
    """
    global emoji
    emoji = emoti


def get_usuario():
    """
    Recupera o usuário e retorna como global.
    :return: A variável onde o usuário está armazenado.
    """
    global usuario
    return usuario


def zerou():
    """
    Está função serve para reconhecer a condição de parada da adição do tamanho da fase paro o começo do modo
    infinity.
    :return: True ou False.
    """
    if get_fase() >= 14:
        return True


def organiza_usuario(nome, emoticon):
    """
    Recebe os dados da entrada quando o usuário vai criar um perfil e define o nome e o emoji como variaveis globais.
    :param nome: Nome do usuário.
    :param emoticon: Nome do emoji.
    :return: O nome e o emoji novo.
    """
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
    set_usuario(nome)
    set_emoji(emote)


def get_emoji():
    """
    Recupera o emoji e retorna como global.
    :return: A variável onde o emoji está armazenado.
    """
    global emoji
    return emoji


def nova_campanha():
    """
    Está função serve para caso o usuário escolha novamente o iniciar jogo. Onde ele vai recomeçar o jogo com uma
    matriz de tamanho 4.
    :return: Uma matriz de tamanho 4.
    """

    global tamanho_matriz
    tamanho_matriz = 4
    limpa_fase()


def salvar_progresso(save_name):
    """
    Está função realiza o save do game, destribuindo as informações necessárias para o arquivo.
    :param save_name: O nome do usuário que está jogando
    :return: Reescrita do arquivo.
    """
    template_save = {USUARIO: get_usuario(), EMOJI: get_emoji(), TAMANHO_M: get_fase(),
                     QTD_VEZES: get_timming(), COINS: get_coins(), COINS_TOTAIS: get_coins_totais()}
    config.read(PROGRESSOS_ARQ)
    config[save_name] = copy.deepcopy(template_save)
    with open(PROGRESSOS_ARQ, "w") as save_file:
        config.write(save_file)


def carregar_progresso(nome_usuario):
    """
    Carrega as informações salvas no arquivo no início do jogo ou na troca de perfis.
    :param nome_usuario: Nome do usuário a ser carregado nos dados.
    :return: As variáveis globais alteradas respectivamente.
    """
    config.read(PROGRESSOS_ARQ)
    time.sleep(3)
    if nome_usuario in config:
        set_usuario(config[nome_usuario].get(USUARIO))
        set_emoji(config[nome_usuario].get(EMOJI))
        set_fase(config[nome_usuario].get(TAMANHO_M))
        loading_timming(config[nome_usuario].get(QTD_VEZES))
        set_coins(config[nome_usuario].get(COINS))
        set_coins_totais(config[nome_usuario].get(COINS_TOTAIS))


tamanho_matriz = 4
pos_init_mod_inim = 20
posicao_personagem = [tamanho_matriz - 1, posicao_inicial(tamanho_matriz)]
posicao_inimigo = [0, posicao_inicial(tamanho_matriz)]
cenario_da_fase = cria_cenario(posicao_personagem, tamanho_matriz)
qtd_vezes = 0
coins = 0
coins_totais = 0
power_ups = []
usuario = "user"
emoji = "\U0001F3C7"
config = configparser.ConfigParser()
