# coding: UTF-8
# projeto para a disciplina de programacao 1 do IFPB
# alunos: Diego Cardoso e Igor Kadson

import os

from modo_inimigo import *


def cls():
    """
    Funcao que limpa o terminal sempre que invocada.
    :return: void.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def mapa_com_bombas(cenario_criado):
    """
    Exibe o mapa com as bombas na tela.
    :param cenario_criado: importa o cenario criado.
    :return: void, printa o cenario.
    """
    contador_linhas = 0
    for linha in range(len(cenario_criado)):
        for coluna in range(len(cenario_criado)):
            if cenario_criado[linha][coluna] == 0:
                if coluna == (len(cenario_criado) - 1):
                    print(MATO)
                else:
                    print(MATO, end='')
            elif cenario_criado[linha][coluna] == 1:
                if coluna == (len(cenario_criado) - 1):
                    print(BOMBA)
                else:
                    print(BOMBA, end='')
            else:
                if coluna == (len(cenario_criado) - 1):
                    print(get_emoji().format(contador_linhas))
                else:
                    print(get_emoji(), end='')


def mapa_real(cenario):
    """
    Imprime o mapa da fase com as bombas e caminhos livres ocultos.
    :param cenario: mapa da fase a ser iterado.
    :return: void, printa o mapa da fase.
    """
    for linha in range(len(cenario)):
        for coluna in range(len(cenario[linha])):
            if cenario[linha][coluna] != PERSONAGEM:
                print(MATO, end='')
            else:
                print(get_emoji(), end='')
            if coluna + 1 == len(cenario):
                print()


def jogando(cenario, posicao):
    """
    Starta o game e controla o fluxo da aplicacao. verifica se o player morre, vive ou passa de fase.
    :param cenario: mapa da fase.
    :param posicao: lugar onde o jogador inicia a partida.
    :return: void.
    """
    while True:
        cls()
        power = get_power_ups()
        mapa_real(cenario)
        movimento = str(input()).upper()
        movimento = valida_movimentacao(movimento, cenario, posicao)

        if movimento in power:
            cls()
            print("Voc?? consumiu uma quantidade de " + movimento)
            aplica_power_up(movimento)
            power.remove(movimento)
            time.sleep(2.5)

        if verifica_se_morreu(movimento, cenario, posicao):
            if "REVIVER" in power:
                power.remove("REVIVER")
                print("Voc?? consumiu seu REVIVER.\nNa pr??xima n??o haver?? escapat??ria, esteja atento.")
                time.sleep(3)
            else:
                incrementa_vezes_rodando()
                cls()
                mapa_com_bombas(cenario)
                print("Que pena...\nVoc?? perdeu!")
                time.sleep(5)
                cls()
                break

        controla_personagem(movimento, cenario, posicao)

        if venceu(cenario):
            cls()
            mapa_com_bombas(cenario)
            moedasganhas = 10
            incrementa_vezes_rodando()
            passou_fase(moedasganhas)
            time.sleep(3)
            cls()
            break
    terminou_partida()


def aplica_power_up(movimento):
    """
    Roda quando um powerup ?? utilizado e aplica este.
    :param movimento: dado da entrada respectivo ao c??digo a ser analisado.
    :return: Void.
    """
    bombas = get_cenario()
    if movimento == PW1:
        mapa_com_bombas(bombas)


def como_jogar():
    """
    Esta fun????o ?? dada no come??o da fase, onde h?? a op????o do usu??rio escolher se quer acessar o tutorial n??o,
    de acordo com a respota do usu??rio ("sim" ou "n??o").
    :return: prints respectivos.
    """
    while True:
        print("Deseja aprender como jogar? (S/N)")
        resposta = str(input()).lower()
        if resposta == "n":
            break
        else:
            print("Analise cuidadosamente onde as bombas ir??o aparecer e tome cuidado para n??o pisar nelas.")
            print("Para realizar um movimento pressione a tecla de dire????o (W, S, A, D)", end=" ")
            print("e em seguida pressione Enter para movimentar o personagem")
            str(input("Se est?? pronto, pessione qualquer tecla para continuar: "))
            cls()
            break


def valida_movimentacao(movimento, cenario, pos_x):
    """
    :param movimento: parametro a ser validado.
    :param cenario: para analisar o mapa e tentar adivinhar o proximo movimento do x.
    :param pos_x: naquele instante 't'.
    :return: o input do movimento adequadamente atualizado.
    """
    possibilities = ["W", "S", "A", "D"]
    power_upx = get_power_ups()
    possibilities.extend(power_upx)
    while True:
        if movimento not in possibilities:
            print("Movementacao inv??lida, por favor tente novamente")
            movimento = str(input()).upper()
        else:
            if movimento == "S":
                if pos_x[0] == len(cenario) - 1:
                    print("Escolha uma movimenta????o dentro do mapa")
                    movimento = str(input()).upper()
                else:
                    return movimento
            elif movimento == "A":
                if pos_x[1] == 0:
                    print("Escolha uma movimenta????o dentro do mapa")
                    movimento = str(input()).upper()
                else:
                    return movimento
            elif movimento == "D":
                if pos_x[1] == len(cenario) - 1:
                    print("Escolha uma movimenta????o dentro do mapa")
                    movimento = str(input()).upper()
                else:
                    return movimento
            elif movimento == "W":
                return movimento
            else:
                return movimento


def iniciando_jogo():
    """
    Imprime a primeira tela que o jogador vera, mostrando as bombas e caminhos livres.
    apos alguns instantes o cenario eh ocultado.
    :return: void, printa o mapa.
    """

    if get_timming() == 0:
        reseta_posicao_jogador()
        limpa_fase()
        print("\nVoc?? est?? preparado?\n")
        time.sleep(1)
        mapa_com_bombas(get_cenario())
        time.sleep(4)
        print("\nSer?? mesmo??????")
        time.sleep(1)
        jogando(get_cenario(), get_posicao())

    else:
        limpa_fase()
        reseta_posicao_jogador()
        print("Boa sorte!")
        time.sleep(1)
        cls()
        carregando()
        time.sleep(0.5)
        mapa_com_bombas(get_cenario())
        time.sleep(3)
        jogando(get_cenario(), get_posicao())


def seletor_opcoes(option):
    """
    Recebe a opcao advinda do menu e interpreta. funciona de forma similar a um switch case.
    :param option: inidica a acao a ser tomada.
    :return: void, da continuidade com a execucao do programa.
    """
    opcoes = ["N", "C", "L", "S", "F", "T", "G"]  # lista de opcoes possiveis
    if zerou():
        if "M" in opcoes:
            pass
        else:
            opcoes.append("M")

    while True:
        if option not in opcoes:
            print("Por favor selecione uma op????o v??lida")
            menu_inicial()
        else:
            if option == "N":
                if get_timming() == 0:
                    como_jogar()
                    cls()
                time.sleep(2)
                if get_fase() > 4:
                    resposta = str(input("Deseja realmente iniciar uma nova campanha? "))
                    if resposta == "sim" or resposta == "s":
                        nova_campanha()
                        cls()

                    else:
                        print("Tente decidir melhor e retorne novamente se tiver certeza.")
                        time.sleep(2)
                        decide_menus()
                        cls()
                iniciando_jogo()
                break
            if option == "L":
                carregando()
                cls()
                loja()
                break
            if option == "C":
                iniciando_jogo()
                break
            if option == "S":
                salvar_progresso(get_usuario())
                config.read(PROGRESSOS_ARQ)
                print("Score do Acumulado de Coins:")
                time.sleep(.4)
                for i in range(len(config.sections())):
                    print(f"{config.sections()[i]}: {config[config.sections()[i]]['coins_totais']}")
                str(input("Pressione qualquer tecla para continuar... "))
                cls()
                decide_menus()
                break
            if option == "M":
                prepara_posicoes()
                inimigo_plays(get_posicao(), get_posicao_inimigo())
                break
            if option == "F":
                salvar_progresso(get_usuario())
                print("J?? vai!?!?")
                time.sleep(1.5)
                print("Sentiremos saudades...")
                time.sleep(2.5)
                exit()
            if option == "T":
                salvar_progresso(get_usuario())
                print("Progresso salvo com sucesso!")
                time.sleep(.4)
                break
            if option == "G":
                salvar_progresso(get_usuario())
                print("Progresso salvo com sucesso!")
                time.sleep(.4)
                cls()
                decide_menus()
                break


def menu_inicial():
    """
    Fun????o que printa o menu inicial al??m de pedir a escolha de onde ele quer ir.
    :return: a fun????o QualVaiSer.
    """
    print("????????????????????????????????????????????????????????????????????????????????????????????????\n"
          "     Bem vind@ ao MineWars\n\n"
          "       ??????  ???? ovo jogo\n"
          "       ??????  ???? ontinuar\n"
          "       ??????  ???? oja\n"
          "       ??????  ???? rocar Perfil\n"
          "       ??????  ???? core\n"
          "       ??????  ???? uardar Progresso\n"
          "       ??????  ???? im\n\n"
          "       Voc?? est?? pront@\n" + "        " + get_usuario() + " " + get_emoji() +
          " ?\n ????????????????????????????????????????????????????????????????????????????????????????????????")
    intermedia_seletor()


def intermedia_seletor():
    """
    Faz o interm??dio entre o menu e o seletor de opcoes, direcionando a opcao selecionada no menu para o mesmo.
    :return: void, apenas chama outra funcao.
    """
    time.sleep(0.5)
    if qtd_vezes == 0:
        opcao = str(input("O que temos para hoje? ")).upper()
    else:
        opcao = str(input("Como posso ajudar dessa vez? ")).upper()
    cls()
    time.sleep(1)
    seletor_opcoes(opcao)


def loja():
    """
    Printa a loja, al??m de dar o input para o usu??rio escolher o que quer comprar.
    :return: outra fun????o que exerce a fun????o da tentativa de pagamento ou compra deste.
    """
    print("???????????????????????????????????????????????????????????????????????????????????????????????????\n"
          "  ???(?????????)??? MineShopping! ???(?????????)???\n\n"
          "\n|| Voc?? tem %d coins dispon??veis\n  "
          "     \n-> ??? Show Bomb (consum??vel) - 1000 coins\n"
          "     \n-> ??? Reviver (consum??vel) - 1500 coins\n"
          "     \n-> ??? Stun - 2000 coins\n"
          "     \n-> ???? etornar\n\n"
          "????????????????????????????????????????????????????????????????????????????????????????????????" % get_coins())
    opcao = str(input("E a??, o que vai ser?\nSelecione um dos n??meros\nOu pressione R para retornar: ")).upper()
    cls()
    manipula_loja(opcao)


def manipula_loja(opcao):
    """
    Nesta fun????o ?? onde est?? localizado os valores e os itens dispon??veis para compra.
    :param opcao: A op????o de item que o usu??rio digitou.
    :return: Se tem op????o poss??vel ou n??o.
    """
    opcoes = ["1", "2", "3", "R"]
    while opcao not in opcoes:
        print("Por favor, selecione uma opcao v??lida (1, 2, 3, R)")
        opcao = str(input()).upper()

    if opcao == "R":
        decide_menus()

    if opcao == "1":
        time.sleep(.9)
        preco = 1000
        if get_coins() >= preco:
            print("Dica: Para usar, tecle SB")
        item = PW1
        valida_compra(preco, item)
        loja()

    if opcao == "2":
        preco = 1500
        item = PW2
        valida_compra(preco, item)
        loja()

    if opcao == "3":
        time.sleep(.9)
        preco = 2000
        if get_coins() >= preco:
            print("Dica: Para usar, tecle ST")
        valida_compra(preco, PW3)
        loja()


def valida_compra(preco, item):
    """
    Verifica se o usu??rio tem coins o suficiente para comprar um item respectivo, se sim, a compra ?? efetuada.
    :param preco: O pre??o da compra.
    :param item: E o item que o usu??rio quer comprar.
    :return: Retorna as respostas respectivas.
    """
    if get_coins() < preco:
        time.sleep(1)
        print("\nVoc?? n??o possui dinheiro suficiente.\nJogue mais um pouco e retorne mais tarde...\n\n(???? ???? ????)(???? "
              "???? ????)")
        time.sleep(2)
        cls()
    else:
        gastou_coins(preco)
        set_power_ups(item)
        time.sleep(1)
        print("(????????? ) Obrigado por comprar na MineShopping! (????????? )")
        time.sleep(1.5)
        print("Dica: Voc?? pode comprar mais de um consum??vel.\nSeja criativo e sempre estar?? preparado!")
        time.sleep(2.5)
        cls()
        print("Voc?? possui %d coins ap??s a sua compra" % get_coins())
        time.sleep(1.5)
        cls()


def terminou_partida():
    """
    Funcao executada no fim de cada partida, da continuidade com o funcionamento do jogo.
    redireciona o jogador para o menu ou para um novo jogo.
    :return: void, continua o funcionamento do c??digo.
    """
    limpa_fase()

    if zerou():
        print("PARAB??NS, VOC?? CHEGOU AO FIM DO JOGO\nMODO INIMIGO LIBERADO!")
        time.sleep(1)
        cls()

    opcao = str(input("Fase conclu??da! Pressione qualquer tecla para continuar ou R para retornar ao menu: ")).upper()
    if opcao == "R":
        cls()
        decide_menus()
    else:
        cls()
        iniciando_jogo()


def terminou_partida_inimigo():
    """
    Funcao executada no fim de uma partida com o inimigo, tem a mesma semantica da funcao terminou_partida().
    :return: void, da continuidade com o funcionamento do jogo.
    """
    ganhoumoedas = 60
    soma_coins(ganhoumoedas)
    soma_coins_totais(ganhoumoedas)
    opcao = str(input("Est??gio encerrado. Digite qualquer bot??o para continuar ou R para retornar ao menu: ")).upper()
    if opcao == "R":
        menu_com_inimigo()
    else:
        prepara_posicoes()
        print("Boa sorte!")
        time.sleep(1)
        cls()
        carregando()
        cls()
        inimigo_plays(get_posicao(), get_posicao_inimigo())


def menu_com_inimigo():
    """
    Essa funcao eh executada depois que o jogador zera o jogo.
    libera a opcao de modo inimigo e se tb se comunica com o seletor de opcoes
    para dar direcionamento ao game.
    :return: void, direciona o jogo de acordo com a acao escolhida.
    """
    print("???????????????????????????????????????????????????????????????????????????????????????????????????\n"
          "  Bem vind@ ao MineWars " + get_usuario() + " " + get_emoji() +
          "\n\n       ??????  ???? niciar jogo\n"
          "       ??????  ???? ontinuar?\n"
          "       ??????  ???? oja\n"
          "       ??????  ???? odo Inimigo!!!\n"
          "       ??????  ???? rocar Perfil \n"
          "       ??????  ???? core\n"
          "       ??????  ???? uardar Progresso\n"
          "       ??????  ???? im\n\n"
          "       Voc?? est?? pronto?\n"
          "???????????????????????????????????????????????????????????????????????????????????????????????????")
    intermedia_seletor()


def inimigo_plays(posicao_pers, posicaoinimigo):
    """
    Essa funcao roda quando o usuario libera e acessa o modo de jogo com o inimigo.
    :param posicao_pers: in     if verificaSeMorreu(movimento, cenario, getPosicao()):
                MapaInimigo(cenario)
                print("Que pena...\nVoc?? perdeu, pisou na bomba!")
                time.sleep(.9)
                break

            controlaPersonagem(movimento, cenario, getPosicao())

            if verificaSeInimigoMatou(cenario, getPosicao()):
                MapaInimigo(cenario)dica a posicao inicial do personagem.
    :param posicaoinimigo: indica a posicao inicial do inimigo.
    :return: void, executa o conjunto de funcoes que imprimem o mapa, controlam o personagem e inimigo simultaneamente.
    """
    cenario = get_cenario_inimigo(posicao_pers, posicaoinimigo)
    while True:
        cls()
        mapa_inimigo(cenario)
        movimento = str(input()).upper()
        movimento = valida_movimentacao(movimento, cenario, get_posicao())
        if movimento == PW3:
            movimento = str(input()).upper()

            movimento = valida_movimentacao(movimento, cenario, get_posicao())

            if verifica_se_morreu(movimento, cenario, get_posicao()):
                cls()
                mapa_inimigo(cenario)
                print("Que pena...\nVoc?? perdeu, pisou na bomba!")
                time.sleep(.9)
                break

            controla_personagem(movimento, cenario, get_posicao())

            if estado_jogo(cenario):
                cls()
                break

        else:

            if verifica_se_morreu(movimento, cenario, get_posicao()):
                cls()
                mapa_inimigo(cenario)
                print("Que pena...\nVoc?? perdeu, pisou na bomba!")
                time.sleep(.9)
                break

            controla_personagem(movimento, cenario, get_posicao())

            if verifica_se_inimigo_matou(cenario, get_posicao()):
                mapa_inimigo(cenario)
                print("O dem??nio te matou fela da puta")
                time.sleep(.9)
                break

            movimenta_inimigo(get_posicao(), get_posicao_inimigo(), cenario)

            if estado_jogo(cenario):
                cls()
                break

    time.sleep(1)
    cls()
    terminou_partida_inimigo()


def estado_jogo(cenario):
    """
    roda dentro da partida com o inimigo para verificar se o cidad??o venceu a partida
    ou se morreu para o inimigo
    :param cenario: mapa da fase onde o jogador esta andando
    :return: True se morreu ou venceu
    """
    if verifica_se_inimigo_matou(cenario, get_posicao()):
        cls()
        mapa_inimigo(cenario)
        print("O dem??nio te matou fela da puta")
        time.sleep(.9)
        return True

    if venceu(cenario):
        cls()
        mapa_inimigo(cenario)
        print("Congratulations!")
        time.sleep(.9)
        return True


def primeira_tela():
    """
    Primeira tela do jogo, sempre executada quando o jogo eh iniciado.
    caso exista algum progresso salvo, simplesmente invoca o menu correspondente.
    :return: void, colhe informacoes do usuario e da direcionamento ao jogo.
    """
    config.read(PROGRESSOS_ARQ)
    carregando()
    print("???????????????????????????????????????????????????????????????????????????????????????????????????\n"
          "    Bem vindo ao MineWars ???%s ???\n"
          "   Lista de perfis j?? salvos\n" % BOMBA)
    for i in range(len(config.sections())):
        print(f"{i+1} - {config.sections()[i]}")
    print("????????????????????????????????????????????????????????????????????????????????????????????????")
    usuario_selecionado = str(input("Insira seu nome de usu??rio para continuar\n"
                                    "Ou um novo nick para iniciar uma campanha: "))
    if usuario_selecionado not in config.sections():
        print("Entendido!")
        time.sleep(.5)
        print("Criando um novo usu??rio...")
        time.sleep(.4)
        cls()
        entre_telas(usuario_selecionado)
    else:
        carregar_progresso(usuario_selecionado)
        cls()
        decide_menus()


def decide_menus():
    """
    Essa fun????o escolhe se vai ser printada a op????o com modo inimigo ou n??o. Para caso o inimigo zere.
    :return: As fun????es referentes aos menus.
    """
    if zerou():
        menu_com_inimigo()
    else:
        menu_inicial()


def entre_telas(user):
    """
    Essa fun????o ?? executada entre a tela de login, ou seja, onde ?? carregada o perfil e o menu inicial.
    S?? ?? rodada quando um novo perfil for criado.
    :param user: Nome do usu??rio
    :return: void
    """
    time.sleep(2)
    print("Muito bom, agora...\nDentre as op????es a seguir, qual voc?? escolheria para definir seu personagem? ")
    time.sleep(2)
    print("??? - ???" + MACACO + "???\n??? - ???" + GATO + "???\n??? - ???" + ET + "???\n??? - ???" + CAVALO + "???\n??? - ???" + UNICORNIO + "???")
    emote = str(input())
    while emote not in OPCOES_EMOJI:
        print("Por favor, selecione uma op????o v??lida...")
        time.sleep(2)
        print("Informe um dos n??meros anteriormente citados para selecionar seu personagem.")
        time.sleep(2)
        emote = str(input())
    organiza_usuario(user, emote)
    time.sleep(1)
    print("Obrigado pela ajuda! Divirta-se " + get_usuario() + " " + get_emoji())
    time.sleep(3)
    cls()
    decide_menus()


def carregando():
    """
    Imprime um conjunto de palavras que controla o fluxo de tempo do jogo.
    :return: void, apenas imprime na tela alguns dados.
    """
    print("??????????????????????????????")
    time.sleep(1)
    cls()
    print("??????????????????????????????")
    time.sleep(.5)
    cls()
    print("??????????????????????????????")
    time.sleep(.5)
    cls()
    print("?????????????????????????????? - 100%")
    time.sleep(.5)
    cls()


def mapa_inimigo(cenario):
    """
    Exibe o mapa inimigo para ser usado na interface com o usu??rio.
    :param cenario: A lista matriz referente ao mapa do modo inimigo.
    :return: Print's do cen??rio
    """
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
                    print(get_emoji().format(cenario))
                else:
                    print(get_emoji(), end='')
            else:
                if coluna == (len(cenario) - 1):
                    print(CAPETA.format(cenario))
                else:
                    print(CAPETA, end='')


if __name__ == "__main__":
    while True:
        primeira_tela()
