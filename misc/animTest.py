import pygame
import time
import os

pygame.init()
pygame.mixer.init()

som_explosao = pygame.mixer.Sound("sounds/explosao.wav")
som_splash = pygame.mixer.Sound("sounds/splash.wav")

def animacao_explosao():
    os.system('cls')
    print("\n\n         💣")
    time.sleep(0.15)

    os.system('cls')
    print("\n\n\n         💣")
    time.sleep(0.15)

    os.system('cls')
    print("\n\n\n\n         💣")
    time.sleep(0.15)

    som_explosao.play()

    os.system('cls')
    print("\n\n\n\n          ✸\n         💥\n          ✸")
    time.sleep(0.1)

    os.system('cls')
    print("\n\n\n\n        💥💥\n       💥💥💥\n        💥💥")
    time.sleep(0.2)

    os.system('cls')
    print("\n\n\n      💥   💥\n     💥💥💥💥💥\n  💥💥💥💥💥💥💥💥\n     💥💥💥💥💥\n      💥   💥")
    time.sleep(0.35)

    os.system('cls')
    print("\n\n\n   💥         💥\n     💥💥💥💥💥\n 💥💥💥💥💥💥💥💥💥\n     💥💥💥💥💥\n   💥         💥")
    time.sleep(0.4)

    os.system('cls')
    print("\n\n\n\n" + "╔════════════╗".center(20) + "\n" + "║  ACERTOU!  ║".center(20) + "\n" + "╚════════════╝".center(20))
    time.sleep(0.9)

def animacao_splash():
    os.system('cls')
    print("\n\n         💣")
    time.sleep(0.15)

    os.system('cls')
    print("\n\n\n         💣")
    time.sleep(0.15)

    os.system('cls')
    print("\n\n\n\n         💣")
    time.sleep(0.15)

    som_splash.play()

    os.system('cls')
    print("\n\n\n\n          💧\n        🌊💧🌊")
    time.sleep(0.25)

    os.system('cls')
    print("\n\n\n        💧    💧\n      💧🌊🌊🌊🌊💧\n     🌊🌊🌊🌊🌊🌊🌊")
    time.sleep(0.4)

    os.system('cls')
    print("\n\n\n" + "╔════════════╗".center(25) + "\n" + "║   ERROU!   ║".center(25) + "\n" + "╚════════════╝".center(25))
    time.sleep(0.9)

while True:
    animacao_explosao()
    animacao_splash()