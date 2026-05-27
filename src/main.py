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

def modo1():
    print(" " * 8, end="")
    for i in range(65, 75):
            print(f"{chr(i)} ", end=" ")
    print()
    for i in range(len(real_jogador)):
        if i < 9:
            print(f"| {i+1} |  {real_jogador[i]}")
        else:
            print(f"| {i+1} | {real_jogador[i]}\n")

    for i in range(5):
        print(f"Posicione o {i+1}º navio.")
        linha = input("Linha (1-10): ")
        while not linha in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            linha = input("\nLinha válida (1-10): ") 
        linha = int(linha) - 1

        coluna = input("Coluna (A-J): ").lower()
        while not coluna in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
            coluna = input("\nColuna válida (A-J): ").lower()

def modo2():
    pass # Placeholder enquanto não tiver nada

def modo3():
    pass # Placeholder enquanto não tiver nada

def main():
    print("Bem-vindo à".center(69))
    print(pyfiglet.figlet_format("Batalha Naval", font="slant")) # Título usando biblioteca "pyfiglet"

    modo = input("Escolha um dos modos de jogo:\n[1] - Humano x Computador\n[2] - Caça-Água\n[3] - Batalha Aérea\n")
    while not modo in ["1", "2", "3"]:
        modo = input("\nInsira uma opção válida (1, 2 ou 3): ")
    modo = int(modo)

    print("\033[H\033[J", end="") 

    if modo == 1:
        modo1()
    elif modo == 2:
        modo2()
    else:
        modo3()

main()