import pyfiglet

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
    pass

def modo2():
    pass

def modo3():
    pass

def main():
    print("Bem-vindo à".center(69))
    print(pyfiglet.figlet_format("Batalha Naval", font="slant")) # Título usando biblioteca "pyfiglet"
    modo = int(input("Escolha um dos modos de jogo:\n[1] - Humano x Computador\n[2] - Caça-Água\n[3] - Batalha Aérea\n"))

    if modo == 1:
        modo1()
    elif modo == 2:
        modo2()
    else:
        modo3()

main()