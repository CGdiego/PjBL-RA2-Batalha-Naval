print("\033[H\033[J", end="") 

import pyfiglet
import random

real_jogador = [
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10
]

vis_jogador = [
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10
]

real_cpu = [
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10
]

vis_cpu = [
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10,
    [0] * 10
]

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
    print(" " * 8, end="")
    for i in range(65, 75):
        print(f"{chr(i)} ", end=" ")
    print()
    for i in range(len(tabuleiro)):
        if i < 9:
            print(f"| {i+1} |  {tabuleiro[i]}")
        else:
            print(f"| {i+1} | {tabuleiro[i]}")
    print("-" * 38)

def main():
    print("Bem-vindo à".center(69))
    print(pyfiglet.figlet_format("Batalha Naval", font="slant")) # Título usando biblioteca "pyfiglet"

    modo = input("Escolha um dos modos de jogo:\n[1] - Humano x Computador (W.I.P.)\n[2] - Simplificado\n[3] - Caça-Água (W.I.P.)\n[4] - Batalha Aérea (W.I.P.)\n")
    while not modo in ["1", "2", "3", "4"]:
        modo = input("\nInsira uma opção válida (1, 2, 3 ou 4): ")
    modo = int(modo)

    print("\033[H\033[J", end="") 

    if modo == 1:
        modo1()
    elif modo == 2:
        modo2()
    elif modo == 3:
        modo3()
    else:
        modo4()

def modo1():
    barco_jogador = 5
    barco_cpu = 5

    exibir_tabuleiro(real_jogador, "do Jogador")

    # Jogador
    for i in range(5):
        print(f"\n\033[1mPosicione o {i+1}º navio.\033[0m")
        linha = escolher_linha()
        coluna = escolher_coluna()

        while real_jogador[linha][coluna] == 1:
            print("\nPosição já ocupada! Escolha outra.")
            linha = escolher_linha()
            coluna = escolher_coluna()
        
        real_jogador[linha][coluna] = 1
    
    # Computador
    for i in range(5):
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)

        while real_cpu[linha][coluna] == 1:
            linha = random.randint(0, 9)
            coluna = random.randint(0, 9)
        
        real_cpu[linha][coluna] = 1

    print("\033[H\033[J", end="") 

    while barco_cpu > 0 and barco_jogador > 0:
        # Tabuleiro do Computador
        exibir_tabuleiro(vis_cpu, "do Computador")
        print(f"Embarcações restantes: {barco_cpu}.\n")
        
        # Tabuleiro do Jogador
        exibir_tabuleiro(vis_jogador, "do Jogador")
        print(f"Embarcações restantes: {barco_jogador}.")

        # Jogador Ataca
        print(f"\n\033[1mEscolha onde atacar.\033[0m")
        linha = escolher_linha()
        coluna = escolher_coluna()

        while real_cpu[linha][coluna] in ["O", "X"]:
            print("\nPosição já atacada! Escolha outra.")
            linha = escolher_linha()
            coluna = escolher_coluna()
        
        print("\033[H\033[J", end="") 

        if real_cpu[linha][coluna] == 1:
            real_cpu[linha][coluna] = "X"
            vis_cpu[linha][coluna] = "X"
            barco_cpu -= 1
            print("Parabéns! Você acertou o alvo.")
            if barco_cpu == 0:
                break
        else:
            real_cpu[linha][coluna] = "O"
            print("Não foi dessa vez... Mas na próxima vai!")

        vis_cpu[linha][coluna] = real_cpu[linha][coluna]

        input("\nEnter para continuar.")

        print("\033[H\033[J", end="")

        # Tabuleiro do Computador
        exibir_tabuleiro(vis_cpu, "do Computador")
        print(f"Embarcações restantes: {barco_cpu}.\n")
        
        # Tabuleiro do Jogador
        exibir_tabuleiro(vis_jogador, "do Jogador")
        print(f"Embarcações restantes: {barco_jogador}.")

        # Computador Ataca
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)

        while real_jogador[linha][coluna] in ["O", "X"]:
            linha = random.randint(0, 9)
            coluna = random.randint(0, 9)
        
        print("\033[H\033[J", end="") 

        print(f"O computador escolheu a linha \033[1m{linha+1}\033[0m.")
        print(f"O computador escolheu a coluna \033[1m{chr(coluna+65)}\033[0m.")

        if real_jogador[linha][coluna] == 1:
            real_jogador[linha][coluna] = "X"
            barco_jogador -= 1
            print("O computador acertou o alvo.")
        else:
            real_jogador[linha][coluna] = "O"
            print("O computador errou o alvo.")

        vis_jogador[linha][coluna] = real_jogador[linha][coluna]

        input("\nEnter para continuar.")

        print("\033[H\033[J", end="")
    
    if barco_cpu == 0:
        print("Parabéns! Você venceu!!!")
    else:
        print("O computador venceu...")
    
    input("\nEnter para continuar.")

    print("Feito por:")
    print(pyfiglet.figlet_format("Diego\nJoao\nLucas", font="slant"))

def modo2():
    barco_jogador = 5
    barco_cpu = 5

    exibir_tabuleiro(real_jogador, "do Jogador")

    # Jogador
    for i in range(5):
        print(f"\n\033[1mPosicione o {i+1}º navio.\033[0m")
        linha = escolher_linha()
        coluna = escolher_coluna()

        while real_jogador[linha][coluna] == 1:
            print("\nPosição já ocupada! Escolha outra.")
            linha = escolher_linha()
            coluna = escolher_coluna()
        
        real_jogador[linha][coluna] = 1
    
    # Computador
    for i in range(5):
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)

        while real_cpu[linha][coluna] == 1:
            linha = random.randint(0, 9)
            coluna = random.randint(0, 9)
        
        real_cpu[linha][coluna] = 1

    print("\033[H\033[J", end="") 

    while barco_cpu > 0 and barco_jogador > 0:
        # Tabuleiro do Computador
        exibir_tabuleiro(vis_cpu, "do Computador")
        print(f"Embarcações restantes: {barco_cpu}.\n")
        
        # Tabuleiro do Jogador
        exibir_tabuleiro(vis_jogador, "do Jogador")
        print(f"Embarcações restantes: {barco_jogador}.")

        # Jogador Ataca
        print(f"\n\033[1mEscolha onde atacar.\033[0m")
        linha = escolher_linha()
        coluna = escolher_coluna()

        while real_cpu[linha][coluna] in ["O", "X"]:
            print("\nPosição já atacada! Escolha outra.")
            linha = escolher_linha()
            coluna = escolher_coluna()
        
        print("\033[H\033[J", end="") 

        if real_cpu[linha][coluna] == 1:
            real_cpu[linha][coluna] = "X"
            vis_cpu[linha][coluna] = "X"
            barco_cpu -= 1
            print("Parabéns! Você acertou o alvo.")
            if barco_cpu == 0:
                break
        else:
            real_cpu[linha][coluna] = "O"
            print("Não foi dessa vez... Mas na próxima vai!")

        vis_cpu[linha][coluna] = real_cpu[linha][coluna]

        input("\nEnter para continuar.")

        print("\033[H\033[J", end="")

        # Tabuleiro do Computador
        exibir_tabuleiro(vis_cpu, "do Computador")
        print(f"Embarcações restantes: {barco_cpu}.\n")
        
        # Tabuleiro do Jogador
        exibir_tabuleiro(vis_jogador, "do Jogador")
        print(f"Embarcações restantes: {barco_jogador}.")

        # Computador Ataca
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)

        while real_jogador[linha][coluna] in ["O", "X"]:
            linha = random.randint(0, 9)
            coluna = random.randint(0, 9)
        
        print("\033[H\033[J", end="") 

        print(f"O computador escolheu a linha \033[1m{linha+1}\033[0m.")
        print(f"O computador escolheu a coluna \033[1m{chr(coluna+65)}\033[0m.")

        if real_jogador[linha][coluna] == 1:
            real_jogador[linha][coluna] = "X"
            barco_jogador -= 1
            print("O computador acertou o alvo.")
        else:
            real_jogador[linha][coluna] = "O"
            print("O computador errou o alvo.")

        vis_jogador[linha][coluna] = real_jogador[linha][coluna]

        input("\nEnter para continuar.")

        print("\033[H\033[J", end="")
    
    if barco_cpu == 0:
        print("Parabéns! Você venceu!!!")
    else:
        print("O computador venceu...")
    
    input("\nEnter para continuar.")

    print("Feito por:")
    print(pyfiglet.figlet_format("Diego\nJoao\nLucas", font="slant"))

def modo3():
    while barco_cpu > 0:
        # Tabuleiro
        exibir_tabuleiro(vis_cpu, "")

        # Jogador Ataca
        print(f"\n\033[1mEscolha onde atacar.\033[0m")
        linha = escolher_linha()
        coluna = escolher_coluna()

        while real_cpu[linha][coluna] in ["O", "X"]:
            print("\nPosição já atacada! Escolha outra.")
            linha = escolher_linha()
            coluna = escolher_coluna()
        
        print("\033[H\033[J", end="") 

        if real_cpu[linha][coluna] == 1:
            real_cpu[linha][coluna] = "X"
            vis_cpu[linha][coluna] = "X"
            barco_cpu -= 1
            print("Parabéns! Você acertou o alvo.")
            if barco_cpu == 0:
                break
        else:
            real_cpu[linha][coluna] = "O"
            print("Não foi dessa vez... Mas na próxima vai!")

        vis_cpu[linha][coluna] = real_cpu[linha][coluna]

        input("\nEnter para continuar.")

        print("\033[H\033[J", end="")

        # Tabuleiro do Computador
        exibir_tabuleiro(vis_cpu, "do Computador")
        print(f"Embarcações restantes: {barco_cpu}.\n")
        
        # Tabuleiro do Jogador
        exibir_tabuleiro(vis_jogador, "do Jogador")
        print(f"Embarcações restantes: {barco_jogador}.")

        # Computador Ataca
        linha = random.randint(0, 9)
        coluna = random.randint(0, 9)

        while real_jogador[linha][coluna] in ["O", "X"]:
            linha = random.randint(0, 9)
            coluna = random.randint(0, 9)
        
        print("\033[H\033[J", end="") 

        print(f"O computador escolheu a linha \033[1m{linha+1}\033[0m.")
        print(f"O computador escolheu a coluna \033[1m{chr(coluna+65)}\033[0m.")

        if real_jogador[linha][coluna] == 1:
            real_jogador[linha][coluna] = "X"
            barco_jogador -= 1
            print("O computador acertou o alvo.")
        else:
            real_jogador[linha][coluna] = "O"
            print("O computador errou o alvo.")

        vis_jogador[linha][coluna] = real_jogador[linha][coluna]

        input("\nEnter para continuar.")

        print("\033[H\033[J", end="")
    
    if barco_cpu == 0:
        print("Parabéns! Você venceu!!!")
    else:
        print("O computador venceu...")
    
    input("\nEnter para continuar.")

    print("Feito por:")
    print(pyfiglet.figlet_format("Diego\nJoao\nLucas", font="slant"))

def modo4():
    pass # Placeholder enquanto não tiver nada

main()