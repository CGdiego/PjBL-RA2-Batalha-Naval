from modo4_batalha_aerea import modo4
import pyfiglet
import pygame
import random
import time
import os

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

limpar()

pygame.init()
pygame.mixer.init()

try:
    musicas = ["sounds/background.mp3", "sounds/background2.mp3"]

    MUSICA_ACABOU = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(MUSICA_ACABOU)

    musica = random.choice(musicas)
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play()
    
    som_explosao = pygame.mixer.Sound("sounds/explosao.wav")
    som_splash   = pygame.mixer.Sound("sounds/splash.wav")
except:
    som_explosao = None
    som_splash   = None

real_jogador = [
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10
]

vis_jogador = [
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10
]

real_cpu = [
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10
]

vis_cpu = [
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10,
    ["⬛"] * 10
]

def tabuleiro_demo():
    demo = [
        ["⬛","⬛","💧","⬛","⬛","⬛","💥","💧","⬛","⬛"],
        ["⬛","🚢","🚢","⬛","💧","⬛","💥","⬛","⬛","⬛"],
        ["⬛","⬛","⬛","⬛","⬛","⬛","🚢","⬛","💧","⬛"],
        ["💧","⬛","🚢","🚢","🚢","🚢","⬛","⬛","⬛","⬛"],
        ["⬛","⬛","💧","⬛","⬛","⬛","⬛","⬛","⬛","⬛"],
        ["⬛","⬛","⬛","⬛","💧","⬛","⬛","⬛","⬛","💥"],
        ["⬛","💧","⬛","⬛","⬛","⬛","⬛","💧","⬛","🚢"],
        ["⬛","⬛","⬛","💧","⬛","⬛","⬛","⬛","⬛","🚢"],
        ["⬛","⬛","⬛","⬛","⬛","💥","⬛","⬛","⬛","🚢"],
        ["💧","⬛","⬛","⬛","⬛","⬛","⬛","💧","⬛","🚢"]
    ]

    exibir_tabuleiro(demo, "Demo")
    print(f"Embarcações restantes: 4.\n")
    print("Exemplo de partida em andamento:")
    print("🚢 = Navio")
    print("💥 = Explosão")
    print("💧 = Água")
    input("\nPressione Enter para voltar...")

def animacao_explosao(modo):
    limpar()
    print("\n\n         💣")
    time.sleep(0.15)

    limpar()
    print("\n\n\n         💣")
    time.sleep(0.15)

    limpar()
    print("\n\n\n\n         💣")
    time.sleep(0.15)

    if som_explosao:
        som_explosao.play()

    limpar()
    print("\n\n\n\n          ✸\n         💥\n          ✸")
    time.sleep(0.1)

    limpar()
    print("\n\n\n\n        💥💥\n       💥💥💥\n        💥💥")
    time.sleep(0.2)

    limpar()
    print("\n\n\n      💥   💥\n     💥💥💥💥💥\n  💥💥💥💥💥💥💥💥\n     💥💥💥💥💥\n      💥   💥")
    time.sleep(0.35)

    limpar()
    print("\n\n\n   💥         💥\n     💥💥💥💥💥\n 💥💥💥💥💥💥💥💥💥\n     💥💥💥💥💥\n   💥         💥")
    time.sleep(0.4)

    if modo == 3:
        limpar()
        print("\n\n\n" + "╔════════════╗".center(20) + "\n" + "║   ERROU!   ║".center(20) + "\n" + "╚════════════╝".center(20))
        time.sleep(0.9)
    else:
        limpar()
        print("\n\n\n\n" + "╔════════════╗".center(20) + "\n" + "║  ACERTOU!  ║".center(20) + "\n" + "╚════════════╝".center(20))
        time.sleep(0.9)

def animacao_splash(modo):
    limpar()
    print("\n\n         💣")
    time.sleep(0.15)

    limpar()
    print("\n\n\n         💣")
    time.sleep(0.15)

    limpar()
    print("\n\n\n\n         💣")
    time.sleep(0.15)

    if som_splash:
        som_splash.play()

    limpar()
    print("\n\n\n\n          💧\n        🌊💧🌊")
    time.sleep(0.25)

    limpar()
    print("\n\n\n        💧    💧\n      💧🌊🌊🌊🌊💧\n     🌊🌊🌊🌊🌊🌊🌊")
    time.sleep(0.4)

    if modo == 3:
        limpar()
        print("\n\n\n\n" + "╔════════════╗".center(25) + "\n" + "║  ACERTOU!  ║".center(25) + "\n" + "╚════════════╝".center(25))
        time.sleep(0.9)
    else:
        limpar()
        print("\n\n\n" + "╔════════════╗".center(25) + "\n" + "║   ERROU!   ║".center(25) + "\n" + "╚════════════╝".center(25))
        time.sleep(0.9)

def escolher_linha():
    linha = input("Linha (1-10): ")
    while not linha in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
        linha = input("\nLinha válida (1-10): ") 
    return int(linha) - 1

def escolher_coluna():
    coluna = input("Coluna (A-J): ").upper()
    while not coluna in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
        coluna = input("\nColuna válida (A-J): ").upper()
    return ord(coluna) - 65

def exibir_tabuleiro(tabuleiro, nome):
    print(f"\033[1mTabuleiro {nome}\033[0m")
    print(" " * 7, end="")
    for i in range(65, 75):
        print(f"{chr(i)}  ", end="")
    print()
    for i in range(len(tabuleiro)):
        if i < 9:
            print(f"| {i+1} |  ", end="")
        else:
            print(f"| {i+1} | ", end="")
        print(" ".join(tabuleiro[i]))
    print("─" * 37)

barcos = [
    {"nome": "Porta-aviões", "tamanho": 5},
    {"nome": "Navio-tanque", "tamanho": 4},
    {"nome": "Contratorpedeiro", "tamanho": 3},
    {"nome": "Submarino", "tamanho": 2},
    {"nome": "Destróier", "tamanho": 1},
]
 
def posicoes_navio(linha, coluna, tamanho, direcao):
    posicoes = []
    for i in range(tamanho):
        if direcao == "H":
            posicoes.append((linha, coluna + i))
        else:
            posicoes.append((linha + i, coluna))
    return posicoes
 
def posicionamento_valido(tabuleiro, posicoes):
    for l, c in posicoes:
        if not (0 <= l <= 9 and 0 <= c <= 9) or tabuleiro[l][c] != "⬛":
            return False
    return True
 
def escolher_direcao():
    direcao = input("Direção ([H]orizontal / [V]ertical): ").strip().upper()
    while direcao not in ["H", "V"]:
        direcao = input("\nDireção válida ([H]orizontal / [V]ertical): ").strip().upper()
    return direcao

def navio_afundou(tabuleiro, id_navio):
    for linha in tabuleiro:
        if id_navio in linha:
            return False
    return True

hack = False

def main():
    global hack
    while True:
        print("Bem-vindo à".center(69))
        print(pyfiglet.figlet_format("Batalha Naval", font="slant")) # Título usando biblioteca "pyfiglet"

        modo = input("Escolha um dos modos de jogo:\n[1] - Humano x Computador\n[2] - Simplificado\n[3] - Caça-Água\n[4] - Batalha Aérea (W.I.P.)\n").replace(" ", "")
        while not modo in ["1", "2", "3", "4", "anim", "tab", "hack"]:
            modo = input("\nInsira uma opção válida (1, 2, 3 ou 4): ").replace(" ", "")

        limpar()

        if modo == "1":
            modo1()
            break
        elif modo == "2":
            modo2()
            break
        elif modo == "3":
            modo3()
            break
        elif modo == "4":
            modo4()
            break
        elif modo == "anim":
            animacao_splash(1)
            animacao_explosao(1)
            limpar()
            continue
        elif modo == "tab":
            tabuleiro_demo()
            limpar()
            continue
        else:
            limpar()
            if not hack:
                print("O hack foi ativado.\nAguarde 3 segundos...")
                hack = True
            else:
                print("O hack foi desativado.\nAguarde 3 segundos...")
                hack = False
            time.sleep(3)
            limpar()
            continue

# Humano x Computador
def modo1():
    global hack
    barco_jogador = 5
    barco_cpu = 5
 
    # Jogador
    for i, barco in enumerate(barcos):
        tamanho = barco["tamanho"]
        nome = barco["nome"]
        id_navio = i + 2

        exibir_tabuleiro(real_jogador, "do Jogador")
        print(f"\n\033[1mPosicione o {nome} (tamanho: {tamanho}).\033[0m")

        while True:
            linha  = escolher_linha()
            coluna = escolher_coluna()
            direcao = escolher_direcao()
            posicoes = posicoes_navio(linha, coluna, tamanho, direcao)

            if posicionamento_valido(real_jogador, posicoes):
                for l, c in posicoes:
                    real_jogador[l][c] = id_navio
                    vis_jogador[l][c]  = "🚢"
                break
            else:
                print("\nPosição inválida! O navio sai do tabuleiro ou sobrepõe outro. Tente novamente.")

        limpar()
 
    # Computador
    for i, barco in enumerate(barcos):
        tamanho = barco["tamanho"]
        id_navio = i + 2
        while True:
            linha = random.randint(0, 9)
            coluna = random.randint(0, 9)
            direcao = random.choice(["H", "V"])
            posicoes = posicoes_navio(linha, coluna, tamanho, direcao)
            if posicionamento_valido(real_cpu, posicoes):
                for l, c in posicoes:
                    real_cpu[l][c] = id_navio
                break
 
    while barco_cpu > 0 and barco_jogador > 0:
        # Tabuleiro do Computador
        if not hack:
            exibir_tabuleiro(vis_cpu, "do Computador")
        else:
            exibir_tabuleiro(real_cpu, "do Computador")
        print(f"Embarcações restantes: {barco_cpu}.\n")
 
        # Tabuleiro do Jogador
        exibir_tabuleiro(vis_jogador, "do Jogador")
        print(f"Embarcações restantes: {barco_jogador}.")
 
        # Jogador Ataca
        print(f"\n\033[1mEscolha onde atacar.\033[0m")
        linha  = escolher_linha()
        coluna = escolher_coluna()
 
        while real_cpu[linha][coluna] in ["💧", "💥"]:
            print("\nPosição já atacada! Escolha outra.")
            linha  = escolher_linha()
            coluna = escolher_coluna()
 
        limpar()

        id_atingido = real_cpu[linha][coluna]
        if id_atingido != "⬛":
            animacao_explosao(2)
            real_cpu[linha][coluna] = "💥"
            vis_cpu[linha][coluna]  = "💥"
            print("Parabéns! Você acertou o alvo.")

            if navio_afundou(real_cpu, id_atingido):
                barco_cpu -= 1
                print(f"Você afundou o {barcos[id_atingido - 2]['nome']}!")

                if barco_cpu == 0:
                    input("\nEnter para continuar.")
                    limpar()
                    break

                print("Ataque novamente!")
                input("\nEnter para continuar.")
                limpar()
                continue
        else:
            animacao_splash(2)
            real_cpu[linha][coluna] = "💧"
            vis_cpu[linha][coluna]  = "💧"
            print("Não foi dessa vez... Mas na próxima vai!")
 
        input("\nEnter para continuar.")
        limpar()
 
        # Tabuleiro do Computador
        if not hack:
            exibir_tabuleiro(vis_cpu, "do Computador")
        else:
            exibir_tabuleiro(real_cpu, "do Computador")
        print(f"Embarcações restantes: {barco_cpu}.\n")
 
        # Tabuleiro do Jogador
        exibir_tabuleiro(vis_jogador, "do Jogador")
        print(f"Embarcações restantes: {barco_jogador}.")
 
        # Computador Ataca
        linha  = random.randint(0, 9)
        coluna = random.randint(0, 9)
 
        while real_jogador[linha][coluna] in ["💧", "💥"]:
            linha  = random.randint(0, 9)
            coluna = random.randint(0, 9)
 
        print(f"\nO computador escolheu a linha \033[1m{linha+1}\033[0m.")
        print(f"O computador escolheu a coluna \033[1m{chr(coluna+65)}\033[0m.")
 
        time.sleep(3)
 
        id_atingido = real_jogador[linha][coluna]
        if id_atingido != "⬛":
            animacao_explosao(2)
            real_jogador[linha][coluna] = "💥"
            vis_jogador[linha][coluna]  = "💥"
            print("O computador acertou o alvo.")

            if navio_afundou(real_jogador, id_atingido):
                barco_jogador -= 1
                print(f"O computador afundou o seu {barcos[id_atingido - 2]['nome']}!")
        else:
            animacao_splash(2)
            real_jogador[linha][coluna] = "💧"
            vis_jogador[linha][coluna]  = "💧"
            print("O computador errou o alvo.")
 
        vis_jogador[linha][coluna] = real_jogador[linha][coluna]
 
        input("\nEnter para continuar.")
        limpar()
 
    if barco_cpu == 0:
        print("Parabéns! Você venceu!!!")
    else:
        print("O computador venceu...")
 
    input("\nEnter para continuar.")
    limpar()
 
    print("Feito por:")
    print(pyfiglet.figlet_format("Diego\nJoao\nLucas", font="slant"))

# Simplificado
def modo2():
    global hack
    barco_jogador = 5
    barco_cpu = 5

    # Jogador
    for i in range(5):
        exibir_tabuleiro(real_jogador, "do Jogador")
        print(f"\n\033[1mPosicione o {i+1}º navio.\033[0m")
        linha = escolher_linha()
        coluna = escolher_coluna()

        while real_jogador[linha][coluna] == "🚢":
            limpar()
            print("\nPosição já ocupada! Escolha outra.")
            linha = escolher_linha()
            coluna = escolher_coluna()
        
        real_jogador[linha][coluna] = "🚢"
        vis_jogador[linha][coluna] = "🚢"
        
        limpar()
    
    # Computador
    for i in range(5):
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)

        while real_cpu[linha][coluna] == "🚢":
            linha = random.randint(0, 9)
            coluna = random.randint(0, 9)
        
        real_cpu[linha][coluna] = "🚢"

    limpar()

    while barco_cpu > 0 and barco_jogador > 0:
        # Tabuleiro do Computador
        if not hack:
            exibir_tabuleiro(vis_cpu, "do Computador")
        else:
            exibir_tabuleiro(real_cpu, "do Computador")
        print(f"Embarcações restantes: {barco_cpu}.\n")
        
        # Tabuleiro do Jogador
        exibir_tabuleiro(vis_jogador, "do Jogador")
        print(f"Embarcações restantes: {barco_jogador}.")

        # Jogador Ataca
        print(f"\n\033[1mEscolha onde atacar.\033[0m")
        linha = escolher_linha()
        coluna = escolher_coluna()

        while real_cpu[linha][coluna] in ["💧", "💥"]:
            print("\nPosição já atacada! Escolha outra.")
            linha = escolher_linha()
            coluna = escolher_coluna()
        
        limpar()

        if real_cpu[linha][coluna] == "🚢":
            animacao_explosao(2)
            real_cpu[linha][coluna] = "💥"
            vis_cpu[linha][coluna] = "💥"
            barco_cpu -= 1
            print("Parabéns! Você acertou o alvo.")
            if barco_cpu == 0:
                input("\nEnter para continuar.")
                limpar()
                break
        else:
            animacao_splash(2)
            real_cpu[linha][coluna] = "💧"
            vis_cpu[linha][coluna] = "💧"
            print("Não foi dessa vez... Mas na próxima vai!")

        input("\nEnter para continuar.")

        limpar()

        # Tabuleiro do Computador
        if not hack:
            exibir_tabuleiro(vis_cpu, "do Computador")
        else:
            exibir_tabuleiro(real_cpu, "do Computador")
        print(f"Embarcações restantes: {barco_cpu}.\n")
        
        # Tabuleiro do Jogador
        exibir_tabuleiro(vis_jogador, "do Jogador")
        print(f"Embarcações restantes: {barco_jogador}.")

        # Computador Ataca
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)

        while real_jogador[linha][coluna] in ["💧", "💥"]:
            linha = random.randint(0, 9)
            coluna = random.randint(0, 9)

        print(f"\nO computador escolheu a linha \033[1m{linha+1}\033[0m.")
        print(f"O computador escolheu a coluna \033[1m{chr(coluna+65)}\033[0m.")

        time.sleep(3)

        if real_jogador[linha][coluna] == "🚢":
            animacao_explosao(2)
            real_jogador[linha][coluna] = "💥"
            barco_jogador -= 1
            print("O computador acertou o alvo.")
        else:
            animacao_splash(2)
            real_jogador[linha][coluna] = "💧"
            print("O computador errou o alvo.")

        vis_jogador[linha][coluna] = real_jogador[linha][coluna]

        input("\nEnter para continuar.")

        limpar()
    
    if barco_cpu == 0:
        print("Parabéns! Você venceu!!!")
    else:
        print("O computador venceu...")
    
    input("\nEnter para continuar.")

    limpar()

    print("Feito por:")
    print(pyfiglet.figlet_format("Diego\nJoao\nLucas", font="slant"))

# Caça-Água
def modo3():
    global hack
    barco_cpu = 1
    vencedor = ""

    linha = random.randint(0, 9)
    coluna = random.randint(0, 9)

    real_cpu[linha][coluna] = "🚢"

    while barco_cpu > 0:
        # Tabuleiro
        if not hack:
            exibir_tabuleiro(vis_cpu, "")
        else:
            exibir_tabuleiro(real_cpu, "")

        # Jogador Ataca
        print(f"\n\033[1mEscolha onde atacar.\033[0m")
        linha = escolher_linha()
        coluna = escolher_coluna()

        while real_cpu[linha][coluna] in ["💧", "💥"]:
            print("\nPosição já atacada! Escolha outra.")
            linha = escolher_linha()
            coluna = escolher_coluna()
        
        limpar()

        if real_cpu[linha][coluna] == "🚢":
            animacao_splash(3)
            real_cpu[linha][coluna] = "💧"
            vis_cpu[linha][coluna] = "💧"
            barco_cpu -= 1
            vencedor = "jogador"
            print("Parabéns! Você acertou o alvo.")
            input("\nEnter para continuar.")
            limpar()
            break
        else:
            animacao_explosao(3)
            real_cpu[linha][coluna] = "💥"
            vis_cpu[linha][coluna] = "💥"
            print("Não foi dessa vez... Mas na próxima vai!")

        input("\nEnter para continuar.")

        limpar()

        # Tabuleiro
        if not hack:
            exibir_tabuleiro(vis_cpu, "")
        else:
            exibir_tabuleiro(real_cpu, "")

        # Computador Ataca
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)

        while real_cpu[linha][coluna] in ["💧", "💥"]:
            linha = random.randint(0, 9)
            coluna = random.randint(0, 9)

        print(f"O computador escolheu a linha \033[1m{linha+1}\033[0m.")
        print(f"O computador escolheu a coluna \033[1m{chr(coluna+65)}\033[0m.")

        time.sleep(3)

        if real_cpu[linha][coluna] == "🚢":
            animacao_splash(3)
            real_cpu[linha][coluna] = "💧"
            barco_cpu -= 1
            vencedor = "cpu"
            print("O computador acertou o alvo.")
        else:
            animacao_explosao(3)
            real_cpu[linha][coluna] = "💥"
            print("O computador errou o alvo.")

        vis_cpu[linha][coluna] = real_cpu[linha][coluna]

        input("\nEnter para continuar.")

        limpar()
    
    if vencedor == "jogador":
        print("Parabéns! Você encontrou a água primeiro!")
    else:
        print("O computador encontrou a água primeiro...")
    
    input("\nEnter para continuar.")

    limpar()

    print("Feito por:")
    print(pyfiglet.figlet_format("Diego\nJoao\nLucas", font="slant"))

main()