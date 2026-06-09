import os
import time
import random

# ─────────────────────────────────────────────
#  BATALHA AÉREA  –  modo4()
#
#  Regras:
#   • Cada "avião" ocupa 3 casas consecutivas (horizontal ou vertical).
#   • Ao posicionar, o jogador escolhe a direção de deslocamento do avião.
#   • A cada RODADA completa (jogador ataca + CPU ataca), todos os aviões
#     se movem UMA casa na sua direção. Se atingirem a borda, retornam
#     pelo lado oposto (wrap-around).
#   • Não há registro de água/explosão no tabuleiro — as posições mudam
#     a cada turno, então o "histórico de tiros" não faz sentido.
#   • Acertar QUALQUER parte de um avião o destrói por completo (ele cai).
#   • Cada jogador/CPU tem 3 aviões.
# ─────────────────────────────────────────────

DIRECOES = {
    "W": (-1,  0),   # cima
    "S": ( 1,  0),   # baixo
    "A": ( 0, -1),   # esquerda
    "D": ( 0,  1),   # direita
}

COLUNAS = list("ABCDEFGHIJ")

# ── helpers ───────────────────────────────────

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_tabuleiro_aereo(avioes, nome, mostrar=True):
    """Monta e imprime um tabuleiro 10×10 com os aviões visíveis."""
    grade = [['⬛'] * 10 for _ in range(10)]
    if mostrar:
        for av in avioes:
            for (r, c) in av["casas"]:
                grade[r][c] = av["emoji"]
    print(f"\033[1mTabuleiro {nome}\033[0m")
    print(" " * 7, end="")
    for ch in COLUNAS:
        print(f"{ch}  ", end="")
    print()
    for i, row in enumerate(grade):
        prefixo = f"| {i+1} |  " if i < 9 else f"| {i+1} | "
        print(prefixo + " ".join(row))
    print("─" * 37)

def escolher_linha_aereo():
    v = input("Linha (1-10): ").strip()
    while v not in [str(x) for x in range(1, 11)]:
        v = input("Linha válida (1-10): ").strip()
    return int(v) - 1

def escolher_coluna_aereo():
    v = input("Coluna (A-J): ").strip().upper()
    while v not in COLUNAS:
        v = input("Coluna válida (A-J): ").strip().upper()
    return COLUNAS.index(v)

def casas_aviao(linha, coluna, orientacao, tamanho=3):
    """Retorna lista de (linha, coluna) para as casas do avião."""
    casas = []
    for i in range(tamanho):
        if orientacao == "H":
            casas.append((linha, coluna + i))
        else:
            casas.append((linha + i, coluna))
    return casas

def posicoes_ocupadas(avioes):
    ocupadas = set()
    for av in avioes:
        for c in av["casas"]:
            ocupadas.add(c)
    return ocupadas

def mover_avioes(avioes):
    """Move cada avião uma casa na sua direção com wrap-around."""
    for av in avioes:
        dr, dc = DIRECOES[av["direcao"]]
        novas = []
        for (r, c) in av["casas"]:
            nr = (r + dr) % 10
            nc = (c + dc) % 10
            novas.append((nr, nc))
        av["casas"] = novas

def checar_acerto(avioes, linha, coluna):
    """
    Verifica se (linha, coluna) acerta algum avião.
    Retorna o índice do avião atingido ou -1.
    """
    for i, av in enumerate(avioes):
        if (linha, coluna) in av["casas"]:
            return i
    return -1

def emojis_avioes():
    return ["✈️", "🛩️", "🚁"]   # um emoji por avião (distinção visual)

# ── posicionamento do jogador ─────────────────

def posicionar_avioes_jogador(n=3):
    avioes = []
    emojis = emojis_avioes()
    for i in range(n):
        cls()
        exibir_tabuleiro_aereo(avioes, "do Jogador")
        print(f"\n\033[1mPosicione o {i+1}º avião ({emojis[i]}).\033[0m")
        print("O avião ocupa 3 casas consecutivas.")

        # orientação
        ori = input("Orientação — [H]orizontal ou [V]ertical: ").strip().upper()
        while ori not in ("H", "V"):
            ori = input("Digite H ou V: ").strip().upper()

        # posição inicial (canto superior-esquerdo do avião)
        print("\nPosição inicial (canto superior-esquerdo do avião):")
        while True:
            linha  = escolher_linha_aereo()
            coluna = escolher_coluna_aereo()
            casas  = casas_aviao(linha, coluna, ori)
            # validar limites
            if any(r < 0 or r > 9 or c < 0 or c > 9 for (r, c) in casas):
                print("⚠️  O avião não cabe nessa posição. Tente novamente.")
                continue
            # validar colisão
            ocupadas = posicoes_ocupadas(avioes)
            if any(p in ocupadas for p in casas):
                print("⚠️  Posição já ocupada. Tente novamente.")
                continue
            break

        # direção de movimento
        print("\nDireção de movimento a cada rodada:")
        print("  W = Cima  |  S = Baixo  |  A = Esquerda  |  D = Direita")
        direcao = input("Direção: ").strip().upper()
        while direcao not in DIRECOES:
            direcao = input("Digite W, A, S ou D: ").strip().upper()

        avioes.append({
            "casas":    casas,
            "direcao":  direcao,
            "emoji":    emojis[i],
            "nome":     f"Avião {i+1}",
        })

    return avioes

# ── posicionamento da CPU ─────────────────────

def posicionar_avioes_cpu(n=3, avioes_jogador=None):
    avioes = []
    emojis = emojis_avioes()
    ocupadas_j = posicoes_ocupadas(avioes_jogador) if avioes_jogador else set()

    for i in range(n):
        while True:
            ori    = random.choice(("H", "V"))
            linha  = random.randint(0, 9)
            coluna = random.randint(0, 9)
            casas  = casas_aviao(linha, coluna, ori)
            if any(r < 0 or r > 9 or c < 0 or c > 9 for (r, c) in casas):
                continue
            ocupadas = posicoes_ocupadas(avioes)
            if any(p in ocupadas for p in casas):
                continue
            break
        direcao = random.choice(list(DIRECOES.keys()))
        avioes.append({
            "casas":   casas,
            "direcao": direcao,
            "emoji":   emojis[i],
            "nome":    f"Avião CPU {i+1}",
        })
    return avioes

# ── animações leves (texto) ───────────────────

def anim_abate():
    frames = [
        "         ✈️",
        "        ✈️💨",
        "       💥✈️",
        "      💥💥",
        "    💥💥💥",
        "  ╔══════════╗\n  ║  ABATIDO! ║\n  ╚══════════╝",
    ]
    for f in frames:
        cls()
        print("\n\n" + f)
        time.sleep(0.2)
    time.sleep(0.6)

def anim_erro():
    frames = ["         💣", "\n         💣", "\n\n         💣", "\n\n💨  💨  💨  💨"]
    for f in frames:
        cls()
        print("\n\n" + f)
        time.sleep(0.18)
    cls()
    print("\n\n  ╔════════════╗\n  ║  ERROU!    ║\n  ╚════════════╝")
    time.sleep(0.8)

# ── loop principal do modo ────────────────────

def modo4():
    cls()
    print("\033[1m" + "=" * 40)
    print("       ✈️  BATALHA AÉREA  ✈️")
    print("=" * 40 + "\033[0m")
    print("""
Regras:
  • Cada avião ocupa 3 casas consecutivas.
  • Ao posicionar, escolha a DIREÇÃO de voo.
  • Após cada rodada completa, os aviões se
    movem 1 casa nessa direção (wrap-around).
  • Acerte QUALQUER parte do avião para
    derrubá-lo por completo!
  • Não há registro de água/explosão —
    o tabuleiro é limpo a cada turno.
""")
    input("Pressione Enter para começar...")

    # ── posicionamento ──
    avioes_jogador = posicionar_avioes_jogador(n=3)
    cls()
    print("Posicionando aviões da CPU...")
    avioes_cpu = posicionar_avioes_cpu(n=3)
    time.sleep(1)
    cls()

    rodada = 1

    while avioes_jogador and avioes_cpu:
        # ── exibir estado ──
        cls()
        print(f"\033[1m{'─'*40}\n  RODADA {rodada}\n{'─'*40}\033[0m\n")

        exibir_tabuleiro_aereo(avioes_cpu, "do Computador (alvo)", mostrar=False)
        print(f"Aviões inimigos restantes: {len(avioes_cpu)}\n")

        exibir_tabuleiro_aereo(avioes_jogador, "do Jogador")
        print(f"Seus aviões restantes: {len(avioes_jogador)}\n")

        # ── ataque do jogador ──
        print("\033[1mEscolha onde atacar:\033[0m")
        linha  = escolher_linha_aereo()
        coluna = escolher_coluna_aereo()
        cls()

        idx = checar_acerto(avioes_cpu, linha, coluna)
        if idx >= 0:
            abatido = avioes_cpu.pop(idx)
            anim_abate()
            print(f"💥 Você abateu o {abatido['nome']} da CPU!")
            if not avioes_cpu:
                input("\nEnter para ver o resultado...")
                cls()
                break
        else:
            anim_erro()
            print("Tiro no vazio — o inimigo está em outro lugar!")

        input("\nEnter para o ataque da CPU...")
        cls()

        # ── ataque da CPU ──
        # A CPU escolhe aleatoriamente (poderia ser "inteligente", mas mantemos simples)
        linha_cpu  = random.randint(0, 9)
        coluna_cpu = random.randint(0, 9)

        print(f"\nA CPU escolheu a linha \033[1m{linha_cpu+1}\033[0m.")
        print(f"A CPU escolheu a coluna \033[1m{COLUNAS[coluna_cpu]}\033[0m.")
        time.sleep(2)
        cls()

        idx_j = checar_acerto(avioes_jogador, linha_cpu, coluna_cpu)
        if idx_j >= 0:
            abatido = avioes_jogador.pop(idx_j)
            anim_abate()
            print(f"💥 A CPU abateu o seu {abatido['nome']}!")
            if not avioes_jogador:
                input("\nEnter para ver o resultado...")
                cls()
                break
        else:
            anim_erro()
            print("A CPU errou! Seus aviões continuam no ar.")

        input("\nEnter para a próxima rodada (os aviões se moverão)...")
        cls()

        # ── movimento ──
        mover_avioes(avioes_cpu)
        mover_avioes(avioes_jogador)
        print("🌐 Os aviões se moveram!")
        time.sleep(1)

        rodada += 1
        cls()

    # ── resultado ──
    if not avioes_cpu and avioes_jogador:
        print("\033[1m🎉 PARABÉNS! Você venceu a Batalha Aérea! 🎉\033[0m")
    elif not avioes_jogador and avioes_cpu:
        print("\033[1m😞 A CPU venceu a Batalha Aérea...\033[0m")
    else:
        print("\033[1m🤝 Empate! Ambos ficaram sem aviões.\033[0m")

    input("\nEnter para continuar...")
    cls()
