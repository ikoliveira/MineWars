# coding: UTF-8
# projeto para a disciplina de programacao 1 do IFPB
# alunos: Diego Cardoso e Igor Kadson

from modoInimigo import *
import os


def cls():
    """
    Funcao que limpa o terminal sempre que invocada.
    :return: void.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def mapaComBombas(cenariocriado):
    """
    Exibe o mapa com as bombas na tela.
    :param cenariocriado: importa o cenario criado.
    :return: void, printa o cenario.
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
    Imprime o mapa da fase com as bombas e caminhos livres ocultos.
    :param cenario: mapa da fase a ser iterado.
    :return: void, printa o mapa da fase.
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
    Starta o game e controla o fluxo da aplicacao. verifica se o player morre, vive ou passa de fase.
    :param cenario: mapa da fase.
    :param posicao: lugar onde o jogador inicia a partida.
    :return: void.
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
                incrementaVezesRodando()
                cls()
                mapaComBombas(cenario)
                print("Que pena...\nVocê perdeu!")
                time.sleep(5)
                cls()
                break

        controlaPersonagem(movimento, cenario, posicao)

        if venceu(cenario):
            cls()
            mapaComBombas(cenario)
            moedasganhas = 10
            incrementaVezesRodando()
            passouFase(moedasganhas)
            time.sleep(3)
            cls()
            break
    terminouPartida()


def aplicaPowerUp(movimento):
    """
    Roda quando um powerup é utilizado e aplica este.
    :param movimento: dado da entrada respectivo ao código a ser analisado.
    :return: Void.
    """
    bombas = getCenario()
    if movimento == PW1:
        mapaComBombas(bombas)


def comoJogar():
    """
    Esta função é dada no começo da fase, onde há a opção do usuário escolher se quer acessar o tutorial não,
    de acordo com a respota do usuário ("sim" ou "não").
    :return: prints respectivos.
    """
    while True:
        print("Deseja aprender como jogar? (S/N)")
        resposta = str(input()).lower()
        if resposta == "n":
            break
        else:
            print("Analise cuidadosamente onde as bombas irão aparecer e tome cuidado para não pisar nelas.")
            print("Para realizar um movimento pressione a tecla de direção (W, S, A, D)", end=" ")
            print("e em seguida pressione Enter para movimentar o personagem")
            str(input("Se está pronto, pessione qualquer tecla para continuar: "))
            cls()
            break


def validaMovimentacao(movimento, cenario, pos_x):
    """
    :param movimento: parametro a ser validado.
    :param cenario: para analisar o mapa e tentar adivinhar o proximo movimento do x.
    :param pos_x: naquele instante 't'.
    :return: o input do movimento adequadamente atualizado.
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
    Imprime a primeira tela que o jogador vera, mostrando as bombas e caminhos livres.
    apos alguns instantes o cenario eh ocultado.
    :return: void, printa o mapa.
    """

    if getTimming() == 0:
        resetaPosicaoJogador()
        limpaFase()
        print("\nVocê está preparado?\n")
        time.sleep(1)
        mapaComBombas(getCenario())
        time.sleep(4)
        print("\nSerá mesmo??????")
        time.sleep(1)
        jogando(getCenario(), getPosicao())

    else:
        limpaFase()
        resetaPosicaoJogador()
        print("Boa sorte!")
        time.sleep(1)
        cls()
        carregando()
        time.sleep(0.5)
        mapaComBombas(getCenario())
        time.sleep(3)
        jogando(getCenario(), getPosicao())


def seletorOpcoes(option):
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
                salvarProgresso(getUsuario())
                config.read("save.ini")
                print("Score do Acumulado de Coins:")
                time.sleep(.4)
                for i in range(len(config.sections())):
                    print(f"{config.sections()[i]}: {config[config.sections()[i]]['coins_totais']}")
                str(input("Pressione qualquer tecla para continuar... "))
                cls()
                decideMenus()
                break
            if option == "M":
                preparaPosicoes()
                inimigoPlays(getPosicao(), getPosicaoInimigo())
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
            if option == "G":
                salvarProgresso(getUsuario())
                print("Progresso salvo com sucesso!")
                time.sleep(.4)
                cls()
                decideMenus()
                break


def menuInicial():
    """
    Função que printa o menu inicial além de pedir a escolha de onde ele quer ir.
    :return: a função QualVaiSer.
    """
    print("◥▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀◤\n"
          "     Bem vind@ ao MineWars\n\n"
          "       ┃➲  🄽 ovo jogo\n"
          "       ┃➲  🄲 ontinuar\n"
          "       ┃➲  🄻 oja\n"
          "       ┃➲  🅃 rocar Perfil\n"
          "       ┃➲  🅂 core\n"
          "       ┃➲  🄶 uardar Progresso\n"
          "       ┃➲  🄵 im\n\n"
          "       Você está pront@\n" + "        " + getUsuario() + " " + getEmoji() +
          " ?\n ◢▅▄▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▄▅◣")
    qualVaiSer()


def qualVaiSer():
    """
    Direciona a opcao selecionada no menu para o seletor de opcoes.
    :return: void, apenas chama outra funcao.
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
    """
    Printa a loja, além de dar o input para o usuário escolher o que quer comprar.
    :return: outra função que exerce a função da tentativa de pagamento ou compra deste.
    """
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
    """
    Nesta função é onde está localizado os valores e os itens disponíveis para compra.
    :param opcao: A opção de item que o usuário digitou.
    :return: Se tem opção possível ou não.
    """
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
    """
    Verifica se o usuário tem coins o suficiente para comprar um item respectivo, se sim, a compra é efetuada.
    :param preco: O preço da compra.
    :param item: E o item que o usuário quer comprar.
    :return: Retorna as respostas respectivas.
    """
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


def terminouPartida():
    """
    Funcao executada no fim de cada partida, da continuidade com o funcionamento do jogo.
    redireciona o jogador para o menu ou para um novo jogo.
    :return: void, continua o funcionamento do código.
    """
    limpaFase()

    if zerou():
        print("PARABÉNS, VOCÊ CHEGOU AO FIM DO JOGO\nMODO INIMIGO LIBERADO!")
        time.sleep(1)
        cls()

    opcao = str(input("Fase concluída! Pressione qualquer tecla para continuar ou R para retornar ao menu: ")).upper()
    if opcao == "R":
        cls()
        decideMenus()
    else:
        cls()
        iniciandoJogo()


def terminouPartidaInimigo():
    """
    Funcao executada no fim de uma partida com o inimigo, tem a mesma semantica da funcao terminou_partida().
    :return: void, da continuidade com o funcionamento do jogo.
    """
    ganhoumoedas = 60
    somaCoins(ganhoumoedas)
    somaCoinsTotais(ganhoumoedas)
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
        inimigoPlays(getPosicao(), getPosicaoInimigo())


def menuComInimigo():
    """
    Essa funcao eh executada depois que o jogador zera o jogo.
    libera a opcao de modo inimigo e se tb se comunica com o seletor de opcoes
    para dar direcionamento ao game.
    :return: void, direciona o jogo de acordo com a acao escolhida.
    """
    print("◥▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀◤\n"
          "  Bem vind@ ao MineWars " + getUsuario() + " " + getEmoji() + "\n\n"
                                                      "       ┃➲  🄸 niciar jogo\n"
                                                      "       ┃➲  🄲 ontinuar?\n"
                                                      "       ┃➲  🄻 oja\n"
                                                      "       ┃➲  🄼 odo Inimigo!!!\n"
                                                      "       ┃➲  🅃 rocar Perfil \n"
                                                      "       ┃➲  🅂 core\n"
                                                      "       ┃➲  🄶 uardar Progresso\n"
                                                      "       ┃➲  🄵 im\n\n"
                                                      "       Você está pronto?\n"
                                                      "◢▅▄▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▄▅◣")
    qualVaiSer()


def inimigoPlays(posicao_personagem, posicaoinimigo):
    """
    Essa funcao roda quando o usuario libera e acessa o modo de jogo com o inimigo.
    :param posicao_personagem: in     if verificaSeMorreu(movimento, cenario, getPosicao()):
                MapaInimigo(cenario)
                print("Que pena...\nVocê perdeu, pisou na bomba!")
                time.sleep(.9)
                break

            controlaPersonagem(movimento, cenario, getPosicao())

            if verificaSeInimigoMatou(cenario, getPosicao()):
                MapaInimigo(cenario)dica a posicao inicial do personagem.
    :param posicaoinimigo: indica a posicao inicial do inimigo.
    :return: void, executa o conjunto de funcoes que imprimem o mapa, controlam o personagem e inimigo simultaneamente.
    """
    cenario = getCenarioInimigo(posicao_personagem, posicaoinimigo)
    while True:
        cls()
        MapaInimigo(cenario)
        movimento = str(input()).upper()
        movimento = validaMovimentacao(movimento, cenario, getPosicao())
        if movimento == PW3:
            movimento = str(input()).upper()

            movimento = validaMovimentacao(movimento, cenario, getPosicao())

            if verificaSeMorreu(movimento, cenario, getPosicao()):
                cls()
                MapaInimigo(cenario)
                print("Que pena...\nVocê perdeu, pisou na bomba!")
                time.sleep(.9)
                break

            controlaPersonagem(movimento, cenario, getPosicao())

            if estadoJogo(cenario):
                cls()
                break

        else:

            if verificaSeMorreu(movimento, cenario, getPosicao()):
                cls()
                MapaInimigo(cenario)
                print("Que pena...\nVocê perdeu, pisou na bomba!")
                time.sleep(.9)
                break

            controlaPersonagem(movimento, cenario, getPosicao())

            if verificaSeInimigoMatou(cenario, getPosicao()):
                MapaInimigo(cenario)
                print("O demônio te matou fela da puta")
                time.sleep(.9)
                break

            MovimentaInimigo(getPosicao(), getPosicaoInimigo(), cenario)

            if estadoJogo(cenario):
                cls()
                break

    time.sleep(1)
    cls()
    terminouPartidaInimigo()


def estadoJogo(cenario):
    """
    roda dentro da partida com o inimigo para verificar se o cidadão venceu a partida
    ou se morreu para o inimigo
    :param cenario: mapa da fase onde o jogador esta andando
    :return: True se morreu ou venceu
    """
    if verificaSeInimigoMatou(cenario, getPosicao()):
        cls()
        MapaInimigo(cenario)
        print("O demônio te matou fela da puta")
        time.sleep(.9)
        return True

    if venceu(cenario):
        cls()
        MapaInimigo(cenario)
        print("Congratulations!")
        time.sleep(.9)
        return True


def primeiraTela():
    """
    Primeira tela do jogo, sempre executada quando o jogo eh iniciado.
    caso exista algum progresso salvo, simplesmente invoca o menu correspondente.
    :return: void, colhe informacoes do usuario e da direcionamento ao jogo.
    """
    config.read("save.ini")
    carregando()
    print("◥▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀◤\n"
          "    Bem vindo ao MineWars 『%s 』\n"
          "   Lista de perfis já salvos\n" % BOMBA)
    for i in range(len(config.sections())):
        print(f"{i+1} - {config.sections()[i]}")
    print("◢▅▄▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▄▅◣")
    usuario_selecionado = str(input("Insira seu nome de usuário para continuar\n"
                                    "Ou um novo nick para iniciar uma campanha: "))
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
    """
    Essa função escolhe se vai ser printada a opção com modo inimigo ou não. Para caso o inimigo zere.
    :return: As funções referentes aos menus.
    """
    if zerou():
        menuComInimigo()
    else:
        menuInicial()


def entreTelas(user):
    """
    Essa função é executada entre a tela de login, ou seja, onde é carregada o perfil e o menu inicial.
    Só é rodada quando um novo perfil for criado.
    :param user: Nome do usuário
    :return: void
    """
    time.sleep(2)
    print("Muito bom, agora...\nDentre as opções a seguir, qual você escolheria para definir seu personagem? ")
    time.sleep(2)
    opcoes_emoji = ["1", "2", "3", "4", "5"]
    print("① - 『" + MACACO + "』\n② - 『" + GATO + "』\n③ - 『" + ET + "』\n④ - 『" + CAVALO + "』\n⑤ - 『" + UNICORNIO + "』")
    emote = str(input())
    while emote not in opcoes_emoji:
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
    Imprime um conjunto de palavras que controla o fluxo de tempo do jogo.
    :return: void, apenas imprime na tela alguns dados.
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


def MapaInimigo(cenario):
    """
    Exibe o mapa inimigo para ser usado na interface com o usuário.
    :param cenario: A lista matriz referente ao mapa do modo inimigo.
    :return: Print's do cenário
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
                    print(getEmoji().format(cenario))
                else:
                    print(getEmoji(), end='')
            else:
                if coluna == (len(cenario) - 1):
                    print(CAPETA.format(cenario))
                else:
                    print(CAPETA, end='')


if __name__ == "__main__":
    while True:
        primeiraTela()
