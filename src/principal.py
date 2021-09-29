# coding: utf-8
# projeto para a disciplina de programacao 1 do IFPB
# alunos: Diego Cardoso e Igor Kadson

from modoInimigo import *
import os


def cls():
    """
    funcao que limpa o terminal sempre que invocada
    :return: void
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def mapa_com_bombas(cenariocriado):
    """
    exibe o mapa com as bombas na tela
    :param cenariocriado: importa o cenario criado
    :return: void, printa o cenario
    """
    contador_linhas = 0
    for linha in range(len(cenariocriado)):
        for coluna in range(len(cenariocriado)):
            if cenariocriado[linha][coluna] == 0:
                if coluna == (len(cenariocriado) - 1):
                    print(MATO)
                else:
                    print(MATO, end='')
            elif cenariocriado[linha][coluna] == 1:
                if coluna == (len(cenariocriado) - 1):
                    print(BOMBA)
                else:
                    print(BOMBA, end='')
            else:
                if coluna == (len(cenariocriado) - 1):
                    print(getEmoji().format(contador_linhas))
                else:
                    print(getEmoji(), end='')


def mapaReal(cenario):
    """
    imprime o mapa da fase com as bombas e caminhos livres ocultos
    :param cenario: mapa da fase a ser iterado
    :return: void, printa o mapa da fase
    """
    for linha in range(len(cenario)):
        for coluna in range(len(cenario[linha])):
            if cenario[linha][coluna] != PERSONAGEM:
                print(MATO, end='')
            else:
                print(getEmoji(), end='')
            if coluna + 1 == len(cenario):
                print()


def jogando(cenario, posicao):
    """
    starta o game e controla o fluxo da aplicacao. verifica se o player morre, vive ou passa de fase
    :param cenario: mapa da fase
    :param posicao: lugar onde o jogador inicia a partida
    :return: void
    """
    while True:
        cls()
        power = getPowerUps()
        mapaReal(cenario)
        movimento = str(input()).upper()
        movimento = validaMovimentacao(movimento, cenario, posicao)

        if movimento in power:
            cls()
            print("Você consumiu uma quantidade de " + movimento)
            aplicaPowerUp(movimento)
            power.remove(movimento)
            time.sleep(2.5)

        if verificaSeMorreu(movimento, cenario, posicao):
            if "REVIVER" in power:
                power.remove("REVIVER")
                print("Você consumiu seu REVIVER.\nNa próxima não haverá escapatória, esteja atento.")
                time.sleep(3)
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
            cls()
            mapa_com_bombas(cenario)
            MOEDASGANHAS = 10
            incrementa_vezesRodando()
            passouFase(MOEDASGANHAS)
            time.sleep(3)
            print("Você passou de fase! O que deseja fazer?")
            cls()
            break
    terminou_partida()


def aplicaPowerUp(movimento):
    bombas = get_cenario()
    if movimento == PW1:
        mapa_com_bombas(bombas)


def comoJogar():
    while True:
        print("Deseja aprender como jogar?")
        resposta = str(input()).lower()
        if resposta == "não" or resposta == "n":
            break
        else:
            print("Analise cuidadosamente onde as bombas irão aparecer e tome cuidado para não pisar nelas.")
            print("Para realizar um movimento pressione a tecla de direção (W, S, A, D)", end=" ")
            print("e em seguida pressione Enter para movimentar o personagem")
            a = str(input("Se está pronto, pessione qualquer tecla para continuar: "))
            cls()
            break


def validaMovimentacao(movimento, cenario, pos_x):
    """
    :param movimento: parametro a ser validado
    :param cenario: para analisar o mapa e tentar adivinhar o proximo movimento do x
    :param pos_x: naquele instante 't'
    :return: o input do movimento adequadamente atualizado
    """
    possibilities = ["W", "S", "A", "D"]
    power_ups = getPowerUps()
    possibilities.extend(power_ups)
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
    imprime a primeira tela que o jogador vera, mostrando as bombas e caminhos livres.
    apos alguns instantes o cenario eh ocultado
    :return: void, printa o mapa
    """

    if getTimming() == 0:
        resetaPosicaoJogador()
        limpaFase()
        print("\nVocê está preparado?\n")
        time.sleep(1)
        mapa_com_bombas(get_cenario())
        time.sleep(4)
        print("\nSerá mesmo??????")
        time.sleep(1)
        jogando(get_cenario(), get_posicao())

    else:
        limpaFase()
        resetaPosicaoJogador()
        print("Boa sorte!")
        time.sleep(1)
        cls()
        carregando()
        time.sleep(0.5)
        mapa_com_bombas(get_cenario())
        time.sleep(3)
        jogando(get_cenario(), get_posicao())


def seletorOpcoes(option):
    """
    recebe a opcao advinda do menu e interpreta. funciona de forma similar a um switch case
    :param option: inidica a acao a ser tomada
    :return: void, da continuidade com a execucao do programa
    """
    opcoes = ["N", "C", "L", "S", "F", "T"]  # lista de opcoes possiveis
    if zerou():
        if "M" in opcoes:
            pass
        else:
            opcoes.append("M")

    while True:
        if option not in opcoes:
            print("Por favor selecione uma opção válida")
            menuInicial()
        else:
            if option == "N":
                if getTimming() == 0:
                    comoJogar()
                    cls()
                time.sleep(2)
                if getFase() > 4:
                    resposta = str(input("Deseja realmente iniciar uma nova campanha? "))
                    if resposta == "sim" or resposta == "s":
                        novaCampanha()
                        cls()

                    else:
                        print("Tente decidir melhor e retorne novamente se tiver certeza.")
                        time.sleep(2)
                        decideMenus()
                        cls()
                iniciandoJogo()
                break
            if option == "L":
                carregando()
                cls()
                loja()
                break
            if option == "C":
                iniciandoJogo()
                break
            if option == "S":
                config.read("save.ini")
                print("Score do Acumulado de Coins:")
                time.sleep(.4)
                for i in range(len(config.sections())):
                    print(f"{config.sections()[i]}: {config[config.sections()[i]]['coins_totais']}")
                continuar = str(input("Pressione qualquer tecla para continuar... "))
                cls()
                decideMenus()
                break
            if option == "M":
                preparaPosicoes()
                inimigoPlays(get_posicao(), getPosicaoInimigo())
                break
            if option == "F":
                salvarProgresso(getUsuario())
                print("Já vai!?!?")
                time.sleep(1.5)
                print("Sentiremos saudades...")
                time.sleep(2.5)
                exit()
            if option == "T":
                salvarProgresso(getUsuario())
                print("Progresso salvo com sucesso!")
                time.sleep(.9)
                break


def menuInicial():
    print("◥▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀◤\n"
          "     Bem vind@ ao MineWars\n\n"
          "       ┃➲  🄽 ovo jogo\n"
          "       ┃➲  🄲 ontinuar\n"
          "       ┃➲  🄻 oja\n"
          "       ┃➲  🅃 rocar Perfil\n"
          "       ┃➲  🅂 core\n"
          "       ┃➲  🄵 im\n\n"
          "       Você está pront@\n" + "        " + getUsuario() + " " + getEmoji() +
          " ?\n ◢▅▄▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▄▅◣")
    qual_vai_ser()


def qual_vai_ser():
    """
    direciona a opcao selecionada no menu para o seletor de opcoes
    :return: void, apenas chama outra funcao
    """
    time.sleep(0.5)
    if qtd_vezes == 0:
        opcao = str(input("O que temos para hoje? ")).upper()
    else:
        opcao = str(input("Como posso ajudar dessa vez? ")).upper()
    cls()
    time.sleep(1)
    seletorOpcoes(opcao)


def loja():
    print("◥▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀◤\n"
          "  ╰(▔∀▔)╯ MineShopping! ╰(▔∀▔)╯\n\n"
          "\n|| Você tem %d coins disponíveis\n  "
          "     \n-> ① Show Bomb (consumível) - 1000 coins\n"
          "     \n-> ② Reviver (consumível) - 1500 coins\n"
          "     \n-> ③ Stun - 2000 coins\n"
          "     \n-> 🅁 etornar\n\n"
          "◢▅▄▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▄▅◣" % getCoins())
    opcao = str(input("E aí, o que vai ser?\nSelecione um dos números\nOu pressione R para retornar: ")).upper()
    cls()
    manipulaLoja(opcao)


def manipulaLoja(opcao):
    opcoes = ["1", "2", "3", "R"]
    while opcao not in opcoes:
        print("Por favor, selecione uma opcao válida (1, 2, 3, R)")
        opcao = str(input()).upper()

    if opcao == "R":
        decideMenus()

    if opcao == "1":

        time.sleep(.9)
        preco = 1000
        if getCoins() >= preco:
            print("Dica: Para usar, tecle SB")
        item = PW1
        validaCompra(preco, item)

    if opcao == "2":
        preco = 1500
        item = PW2
        validaCompra(preco, item)

    if opcao == "3":
        time.sleep(.9)
        preco = 2000
        if getCoins() >= preco:
            print("Dica: Para usar, tecle ST")
        validaCompra(preco, PW3)
    loja()


def validaCompra(preco, item):

    if getCoins() < preco:
        time.sleep(1)
        print("\nVocê não possui dinheiro suficiente.\nJogue mais um pouco e retorne mais tarde...\n\n(͡° ͜ʖ ͡°)(͡° "
              "͜ʖ ͡°)")
        time.sleep(2)
        cls()
    else:
        gastouCoins(preco)
        setPowerUps(item)
        time.sleep(1)
        print("(✯◡✯ ) Obrigado por comprar na MineShopping! (✯◡✯ )")
        time.sleep(1.5)
        print("Dica: Você pode comprar mais de um consumível.\nSeja criativo e sempre estará preparado!")
        time.sleep(2.5)
        cls()
        print("Você possui %d coins após a sua compra" % getCoins())
        time.sleep(1.5)
        cls()


def terminou_partida():
    """
    funcao executada no fim de cada partida, da continuidade com o funcionamento do jogo
    redireciona o jogador para o menu ou para um novo jogo
    :return: void, continua o funcionamento do código
    """
    limpaFase()
    opcao = str(input("Fase concluída! Pressione qualquer tecla para continuar ou R para retornar ao menu: ")).upper()
    if opcao == "R":
        decideMenus()
    else:
        iniciandoJogo()


def terminou_partidaInimigo():
    """
    funcao executada no fim de uma partida com o inimigo, tem a mesma semantica da funcao terminou_partida()
    :return: void, da continuidade com o funcionamento do jogo.
    """
    GANHOUMOEDAS = 60
    somaCoins(GANHOUMOEDAS)
    somaCoinsTotais(GANHOUMOEDAS)
    opcao = str(input("Estágio encerrado. Digite qualquer botão para continuar ou R para retornar ao menu: ")).upper()
    if opcao == "R":
        menuComInimigo()
    else:
        preparaPosicoes()
        print("Boa sorte!")
        time.sleep(1)
        cls()
        carregando()
        cls()
        inimigoPlays(get_posicao(), getPosicaoInimigo())


def menuComInimigo():
    """
    essa funcao eh executada depois que o jogador zera o jogo.
    libera a opcao de modo inimigo e se tb se comunica com o seletor de opcoes
    para dar direcionamento ao game
    :return: void, direciona o jogo de acordo com a acao escolhida
    """
    print("◥▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀◤\n"
          "  Bem vind@ ao MineWars " + getUsuario() + " " + getEmoji() + "\n\n"
                                                      "       ┃➲  🄸 niciar jogo\n"
                                                      "       ┃➲  🄲 ontinuar?\n"
                                                      "       ┃➲  🄻 oja\n"
                                                      "       ┃➲  🄼 odo Inimigo!!!\n"
                                                      "       ┃➲  🅃 rocar Perfil \n"
                                                      "       ┃➲  🅂 core\n"
                                                      "       ┃➲  🄵 im\n\n"
                                                      "       Você está pronto?\n"
                                                      "◢▅▄▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▄▅◣")
    qual_vai_ser()


def inimigoPlays(posicaopersonagem, posicaoinimigo):
    """
    essa funcao roda quando o usuario libera e acessa o modo de jogo com o inimigo
    :param posicaopersonagem: indica a posicao inicial do personagem
    :param posicaoinimigo: indica a posicao inicial do inimigo
    :return: void, executa o conjunto de funcoes que imprimem o mapa, controlam o personagem e inimigo simultaneamente.
    """
    cenario = getCenarioInimigo(posicaopersonagem, posicaoinimigo)
    while True:
        cls()
        MapaInimigo(cenario)
        movimento = str(input()).upper()
        movimento = validaMovimentacao(movimento, cenario, get_posicao())
        if movimento == PW3:
            movimento = str(input()).upper()

            movimento = validaMovimentacao(movimento, cenario, get_posicao())

            if verificaSeMorreu(movimento, cenario, get_posicao()):
                MapaInimigo(cenario)
                print("Que pena...\nVocê perdeu, pisou na bomba!")
                time.sleep(.9)
                break

            controlaPersonagem(movimento, cenario, get_posicao())

            if verificaSeInimigoMatou(cenario, get_posicao()):
                MapaInimigo(cenario)
                print("O demônio te matou fela da puta")
                time.sleep(.9)
                break

            if venceu(cenario):
                MapaInimigo(cenario)
                print("Congratulations!")
                time.sleep(.9)
                break

        else:

            if verificaSeMorreu(movimento, cenario, get_posicao()):
                MapaInimigo(cenario)
                print("Que pena...\nVocê perdeu, pisou na bomba!")
                time.sleep(.9)
                break

            controlaPersonagem(movimento, cenario, get_posicao())

            if verificaSeInimigoMatou(cenario, get_posicao()):
                MapaInimigo(cenario)
                print("O demônio te matou fela da puta")
                time.sleep(.9)
                break

            MovimentaInimigo(get_posicao(), getPosicaoInimigo(), cenario)

            if verificaSeInimigoMatou(cenario, get_posicao()):
                MapaInimigo(cenario)
                print("O demônio te matou fela da puta")
                time.sleep(.9)
                break

            if venceu(cenario):
                MapaInimigo(cenario)
                print("Congratulations!")
                time.sleep(.9)
                break

    time.sleep(1)
    cls()
    terminou_partidaInimigo()


def primeiraTela():
    """
    primeira tela do jogo, sempre executada quando o jogo eh iniciado.
    caso exista algum progresso salvo, simplesmente invoca o menu correspondente.
    :return: void, colhe informacoes do usuario e da direcionamento ao jogo
    """
    config.read("save.ini")
    carregando()
    print("◥▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀◤\n"
          "    Bem vindo ao MineWars 『%s 』\n"
          "   Lista de perfis já salvos\n" % BOMBA)
    for i in range(len(config.sections())):
        print(f"{i+1} - {config.sections()[i]}")
    print("◢▅▄▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▄▅◣")
    usuario_selecionado = str(input("Insira seu nome de usuário para continuar\nOu um novo nick para iniciar uma campanha: "))
    if usuario_selecionado not in config.sections():
        print("Entendido!")
        time.sleep(.5)
        print("Criando um novo usuário...")
        time.sleep(.4)
        cls()
        entreTelas(usuario_selecionado)
    else:
        carregarProgresso(usuario_selecionado)
        cls()
        decideMenus()


def decideMenus():
    if zerou():
        menuComInimigo()
    else:
        menuInicial()


def entreTelas(user):
    time.sleep(2)
    print("Muito bom, agora...\nDentre as opções a seguir, qual você escolheria para definir seu personagem? ")
    time.sleep(2)
    opcoesEmoji = ["1", "2", "3", "4", "5"]
    print("① - 『" + MACACO + "』\n② - 『" + GATO + "』\n③ - 『" + ET + "』\n④ - 『" + CAVALO + "』\n⑤ - 『" + UNICORNIO + "』")
    emote = str(input())
    while emote not in opcoesEmoji:
        print("Por favor, selecione uma opção válida...")
        time.sleep(2)
        print("Informe um dos números anteriormente citados para selecionar seu personagem.")
        time.sleep(2)
        emote = str(input())
    organizaUsuario(user, emote)
    time.sleep(1)
    print("Obrigado pela ajuda! Divirta-se " + getUsuario() + " " + getEmoji())
    time.sleep(3)
    cls()
    decideMenus()


def carregando():
    """
    imprime um conjunto de palavras que controla o fluxo de tempo do jogo
    :return: void, apenas imprime na tela alguns dados
    """
    print("███▒▒▒▒▒▒▒")
    time.sleep(1)
    cls()
    print("█████▒▒▒▒▒")
    time.sleep(.5)
    cls()
    print("███████▒▒▒")
    time.sleep(.5)
    cls()
    print("██████████ - 100%")
    time.sleep(.5)
    cls()


if __name__ == "__main__":
    while True:
        primeiraTela()