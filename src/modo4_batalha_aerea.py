"""
modo4_batalha_aerea.py — Batalha Aérea com Pygame

Cada avião tem 3 casas e uma direção de voo.
Aviões só podem voar para frente ou para trás (paralelo ao corpo),
nunca de lado. Após cada rodada, todos se movem uma casa.

Para usar no jogo principal:
    from modo4_batalha_aerea import modo4
"""

import pygame
import random
import sys
import os
import math


# ==============================================================================
# CONFIGURAÇÕES GERAIS
# ==============================================================================

LARGURA, ALTURA = 1200, 820
CELULA   = 46   # tamanho de cada quadrado do grid em pixels
ESPACO   = 3    # espaço entre células
PASSO    = CELULA + ESPACO  # quanto avança por célula
LINHAS = COLUNAS = 10
FPS = 60

LETRAS_COLUNAS = list("ABCDEFGHIJ")

# Layout dos dois tabuleiros na tela
BOARD_W = COLUNAS * PASSO - ESPACO   # largura total de um grid
BOARD_H = LINHAS  * PASSO - ESPACO   # altura total de um grid
MARGEM_X = 73    # margem da borda esquerda até o primeiro grid
PAD_ESQUERDA = 28   # espaço para os números de linha (à esquerda do grid)
PAD_CIMA = 18       # espaço para as letras de coluna (acima do grid)

# Origem (canto superior esquerdo) de cada grid
GRID_P_X = MARGEM_X + PAD_ESQUERDA          # grid do jogador
GRID_E_X = MARGEM_X + BOARD_W + 80 + PAD_ESQUERDA   # grid inimigo
GRID_Y   = 130 + PAD_CIMA                   # mesma altura para os dois

# Centro do painel de controles (tela de posicionamento)
# Fica no espaço à direita do grid do jogador
CTRL_X = GRID_P_X + BOARD_W + (LARGURA - GRID_P_X - BOARD_W) // 2


# ==============================================================================
# CORES
# ==============================================================================

AZUL_ESCURO  = (  8,  16,  36)
OCEANO       = ( 14,  44,  86)
OCEANO_HL    = ( 22,  68, 120)
GRADE        = ( 28,  64, 120)
BRANCO       = (225, 238, 255)
CINZA        = (110, 130, 165)
CIANO        = ( 80, 195, 255)
PAINEL       = ( 12,  24,  56)
BOTAO        = ( 28,  76, 155)
BOTAO_HOVER  = ( 46, 114, 200)
VERDE        = ( 50, 195,  90)
LARANJA      = (235, 135,  25)
ROXO         = (155,  75, 215)
VERMELHO     = (215,  55,  55)
AMARELO      = (250, 205,  45)
EXPLOSAO     = (220,  55,  40)
AGUA         = ( 55, 125, 200)
VERMELHO_ESC = (120,  25,  25)
VERDE_CLARO  = ( 80, 220, 160)

CORES_AVIOES = [VERDE, LARANJA, ROXO]

# Direções possíveis: W=cima, S=baixo, A=esquerda, D=direita
DIRECOES = {
    "W": (-1,  0),
    "S": ( 1,  0),
    "A": ( 0, -1),
    "D": ( 0,  1),
}

# Setas visuais para cada direção
SETA = {"W": "^", "S": "v", "A": "<", "D": ">"}


# ==============================================================================
# FONTES (inicializadas quando o pygame já está rodando)
# ==============================================================================

fonte_titulo = fonte_grande = fonte_media = fonte_pequena = fonte_mini = None

def carregar_fontes():
    global fonte_titulo, fonte_grande, fonte_media, fonte_pequena, fonte_mini

    # Tenta Impact primeiro, senão usa a padrão do pygame
    for nome in ("impact", None):
        try:
            fonte_titulo = pygame.font.SysFont(nome, 56, bold=(nome is None))
            break
        except Exception:
            pass

    # Fontes monoespaçadas para o jogo
    for nome in ("consolas", "courier new", None):
        try:
            fonte_grande  = pygame.font.SysFont(nome, 30, bold=True)
            fonte_media   = pygame.font.SysFont(nome, 19, bold=True)
            fonte_pequena = pygame.font.SysFont(nome, 15)
            fonte_mini    = pygame.font.SysFont(nome, 12)
            break
        except Exception:
            pass


# ==============================================================================
# FUNÇÕES DE DESENHO GENÉRICAS
# ==============================================================================

def escrever(surf, texto, fonte, cor, x, y, ancora="center"):
    """Renderiza texto numa surface com âncora configurável."""
    s = fonte.render(str(texto), True, cor)
    r = s.get_rect()
    setattr(r, ancora, (x, y))
    surf.blit(s, r)
    return r

def desenhar_painel(surf, rect):
    """Painel escuro com borda azul."""
    pygame.draw.rect(surf, PAINEL, rect, border_radius=10)
    pygame.draw.rect(surf, GRADE,  rect, 2, border_radius=10)

def desenhar_botao(surf, rect, texto, destacado):
    """Botão clicável simples."""
    cor = BOTAO_HOVER if destacado else BOTAO
    pygame.draw.rect(surf, cor,   rect, border_radius=8)
    pygame.draw.rect(surf, CIANO, rect, 2, border_radius=8)
    escrever(surf, texto, fonte_media, BRANCO, rect.centerx, rect.centery)

def pos_celula(ox, oy, linha, col):
    """Retorna o pixel (x, y) do canto superior esquerdo de uma célula."""
    return ox + col * PASSO, oy + linha * PASSO

def pixel_para_celula(ox, oy, px, py):
    """Converte coordenada de pixel para (linha, coluna) no grid. Retorna None se fora."""
    rx, ry = px - ox, py - oy
    if rx < 0 or ry < 0:
        return None
    col, sobra_x = divmod(rx, PASSO)
    lin, sobra_y = divmod(ry, PASSO)
    if 0 <= lin < LINHAS and 0 <= col < COLUNAS and sobra_x < CELULA and sobra_y < CELULA:
        return lin, col
    return None


# ==============================================================================
# DESENHO DO AVIÃO
# ==============================================================================

def desenhar_aviao(surf, cx, cy, tamanho, cor, direcao="D"):
    """
    Desenha um avião apontando na direção do voo.
    O modelo base aponta para a direita; rotacionamos conforme a direção.
    """
    s = tamanho
    angulo = {"D": 0, "A": math.pi, "S": math.pi/2, "W": -math.pi/2}.get(direcao, 0)
    cos_a, sin_a = math.cos(angulo), math.sin(angulo)

    def girar(x, y):
        dx, dy = x - cx, y - cy
        return (cx + dx*cos_a - dy*sin_a,
                cy + dx*sin_a + dy*cos_a)

    # Corpo (linha horizontal)
    pygame.draw.line(surf, cor, girar(cx-s, cy), girar(cx+s*2, cy), 3)
    # Asas (triângulo acima e abaixo)
    pygame.draw.polygon(surf, cor, [girar(cx-s//2, cy), girar(cx+s//2, cy), girar(cx, cy-s)])
    pygame.draw.polygon(surf, cor, [girar(cx-s//2, cy), girar(cx+s//2, cy), girar(cx, cy+s)])
    # Cauda (dois traços na parte traseira)
    pygame.draw.line(surf, cor, girar(cx-s, cy), girar(cx-s-s//2, cy-s//2), 2)
    pygame.draw.line(surf, cor, girar(cx-s, cy), girar(cx-s-s//2, cy+s//2), 2)


# ==============================================================================
# DESENHO DO GRID
# ==============================================================================

def desenhar_grid(surf, ox, oy, lista_avioes, mostrar_avioes=True,
                  destaque=None, preview=None, cor_preview=VERDE,
                  ori_preview="H", dir_preview="D"):
    """
    Desenha um tabuleiro 10x10.
    - mostrar_avioes: False no grid inimigo (o jogador não pode ver)
    - destaque: célula (lin, col) que fica iluminada (hover do mouse)
    - preview: lista de células para mostrar antes de confirmar posição
    """
    # Células de fundo
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            x, y = pos_celula(ox, oy, lin, col)
            cor = OCEANO_HL if destaque == (lin, col) else OCEANO
            pygame.draw.rect(surf, cor,   (x, y, CELULA, CELULA), border_radius=3)
            pygame.draw.rect(surf, GRADE, (x, y, CELULA, CELULA), 1, border_radius=3)

    # Aviões reais (só aparece no tabuleiro do jogador)
    if mostrar_avioes:
        for av in lista_avioes:
            cor     = av["cor"]
            direcao = av["direcao"]
            casas   = av["casas"]

            # Pinta as 3 células do avião
            for (lin, col) in casas:
                x, y = pos_celula(ox, oy, lin, col)
                pygame.draw.rect(surf, cor,    (x, y, CELULA, CELULA), border_radius=3)
                pygame.draw.rect(surf, BRANCO, (x, y, CELULA, CELULA), 1, border_radius=3)

            # Ícone do avião no meio das 3 células
            lin_meio, col_meio = casas[1]
            cx_av = ox + col_meio * PASSO + CELULA // 2
            cy_av = oy + lin_meio * PASSO + CELULA // 2
            desenhar_aviao(surf, cx_av, cy_av, 9, BRANCO, direcao)

    # Preview de posicionamento
    if preview:
        for (lin, col) in preview:
            if 0 <= lin < LINHAS and 0 <= col < COLUNAS:
                x, y = pos_celula(ox, oy, lin, col)
                pygame.draw.rect(surf, cor_preview, (x, y, CELULA, CELULA), border_radius=3)
                pygame.draw.rect(surf, BRANCO,      (x, y, CELULA, CELULA), 2, border_radius=3)

        # Ícone do avião no preview
        if len(preview) >= 2:
            lin_m, col_m = preview[1]
            if 0 <= lin_m < LINHAS and 0 <= col_m < COLUNAS:
                cx_prev = ox + col_m * PASSO + CELULA // 2
                cy_prev = oy + lin_m * PASSO + CELULA // 2
                desenhar_aviao(surf, cx_prev, cy_prev, 9, BRANCO, dir_preview)

    # Letras das colunas (A-J) acima do grid
    for col in range(COLUNAS):
        x, _ = pos_celula(ox, oy, 0, col)
        escrever(surf, LETRAS_COLUNAS[col], fonte_mini, CINZA, x + CELULA//2, oy - 10)

    # Números das linhas (1-10) à esquerda do grid
    for lin in range(LINHAS):
        _, y = pos_celula(ox, oy, lin, 0)
        escrever(surf, str(lin+1), fonte_mini, CINZA, ox - 14, y + CELULA//2)


# ==============================================================================
# ANIMAÇÕES
# ==============================================================================

def anim_explosao(surf, clock, ox, oy, lin, col, redesenhar):
    """Círculo vermelho se expandindo — acerto."""
    cx = ox + col * PASSO + CELULA // 2
    cy = oy + lin * PASSO + CELULA // 2

    for frame in range(36):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        redesenhar()

        prog   = frame / 35
        raio   = int(prog * 62)
        alpha  = int(255 * (1 - prog))

        s = pygame.Surface((raio*2+4, raio*2+4), pygame.SRCALPHA)
        pygame.draw.circle(s, (*EXPLOSAO, alpha), (raio+2, raio+2), raio+2)
        pygame.draw.circle(s, (*AMARELO,  alpha), (raio+2, raio+2), max(1, raio-8))
        surf.blit(s, (cx-raio-2, cy-raio-2))

        pygame.display.flip()
        clock.tick(FPS)

def anim_agua(surf, clock, ox, oy, lin, col, redesenhar):
    """Círculo azul se expandindo — erro."""
    cx = ox + col * PASSO + CELULA // 2
    cy = oy + lin * PASSO + CELULA // 2

    for frame in range(24):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        redesenhar()

        prog  = frame / 23
        raio  = int(prog * 40)
        alpha = int(255 * (1 - prog))

        s = pygame.Surface((raio*2+4, raio*2+4), pygame.SRCALPHA)
        pygame.draw.circle(s, (*AGUA, alpha), (raio+2, raio+2), raio+2)
        surf.blit(s, (cx-raio-2, cy-raio-2))

        pygame.display.flip()
        clock.tick(FPS)

def anim_movimento(surf, clock, redesenhar, avioes_jogador, avioes_cpu):
    """
    Desliza os aviões do jogador visualmente antes de mover de verdade.
    A CPU é invisível, então só animamos o lado do jogador.
    """
    TOTAL_FRAMES = 32

    for frame in range(TOTAL_FRAMES):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # Curva ease-out: começa rápido, desacelera no final
        t = 1 - (1 - frame / (TOTAL_FRAMES - 1)) ** 3

        redesenhar()

        # Só mostra a animação dos aviões do jogador (inimigos são ocultos)
        for av in avioes_jogador:
            dr, dc  = DIRECOES[av["direcao"]]
            cor     = av["cor"]
            direcao = av["direcao"]
            casas   = av["casas"]

            for (lin, col) in casas:
                # Posição atual → posição destino
                x0 = GRID_P_X + col * PASSO
                y0 = GRID_Y   + lin * PASSO
                x1 = GRID_P_X + ((col + dc) % COLUNAS) * PASSO
                y1 = GRID_Y   + ((lin + dr) % LINHAS)  * PASSO

                xi = x0 + (x1 - x0) * t
                yi = y0 + (y1 - y0) * t

                pygame.draw.rect(surf, cor,    (xi, yi, CELULA, CELULA), border_radius=3)
                pygame.draw.rect(surf, BRANCO, (xi, yi, CELULA, CELULA), 1, border_radius=3)

            # Ícone no meio
            lin_m, col_m = casas[1]
            x0c = GRID_P_X + col_m * PASSO + CELULA // 2
            y0c = GRID_Y   + lin_m * PASSO + CELULA // 2
            x1c = GRID_P_X + ((col_m + dc) % COLUNAS) * PASSO + CELULA // 2
            y1c = GRID_Y   + ((lin_m + dr) % LINHAS)  * PASSO + CELULA // 2
            desenhar_aviao(surf, x0c + (x1c-x0c)*t, y0c + (y1c-y0c)*t, 9, BRANCO, direcao)

        escrever(surf, "Avioes se movendo...", fonte_media, VERDE_CLARO, LARGURA//2, ALTURA-30)
        pygame.display.flip()
        clock.tick(FPS)


# ==============================================================================
# BARRA DE TÍTULO
# ==============================================================================

def desenhar_titulo(surf, imagem_aviao):
    """Titulo 'BATALHA AEREA' com imagem opcional ao lado."""
    ts = fonte_titulo.render("BATALHA AEREA", True, CIANO)
    tw, th = ts.get_size()
    img_w  = imagem_aviao.get_width() if imagem_aviao else 0
    gap    = 12
    total  = img_w + (gap if imagem_aviao else 0) + tw
    sx, yc = LARGURA // 2 - total // 2, 38

    if imagem_aviao:
        surf.blit(imagem_aviao, (sx, yc - imagem_aviao.get_height() // 2))
        surf.blit(ts, (sx + img_w + gap, yc - th // 2))
    else:
        surf.blit(ts, (LARGURA // 2 - tw // 2, yc - th // 2))


# ==============================================================================
# LÓGICA DOS AVIÕES
# ==============================================================================

def criar_aviao(indice, casas, direcao, orientacao):
    """Cria um dicionário representando um avião."""
    return {
        "casas":      list(casas),
        "direcao":    direcao,
        "orientacao": orientacao,   # "H" ou "V"
        "nome":       f"Aviao {indice + 1}",
        "cor":        CORES_AVIOES[indice % 3],
    }

def direcoes_validas_para(orientacao):
    """
    Retorna só as direções que fazem sentido para a orientação do avião.
    Horizontal → só pode ir para esquerda (A) ou direita (D).
    Vertical   → só pode ir para cima (W) ou para baixo (S).
    Aviões não voam de lado!
    """
    if orientacao == "H":
        return ["A", "D"]
    else:
        return ["W", "S"]

def gerar_avioes_cpu(quantidade=3):
    """Cria aviões aleatórios para a CPU, sem sobreposição."""
    avioes = []
    ocupadas = set()

    for i in range(quantidade):
        while True:
            ori = random.choice(("H", "V"))
            lin0 = random.randint(0, 9)
            col0 = random.randint(0, 9)

            casas = []
            valido = True
            for j in range(3):
                nl = lin0 + (j if ori == "V" else 0)
                nc = col0 + (j if ori == "H" else 0)
                if not (0 <= nl < 10 and 0 <= nc < 10) or (nl, nc) in ocupadas:
                    valido = False
                    break
                casas.append((nl, nc))

            if valido:
                for c in casas:
                    ocupadas.add(c)
                # CPU também só voa em direções válidas para a orientação
                direcao = random.choice(direcoes_validas_para(ori))
                avioes.append(criar_aviao(i, casas, direcao, ori))
                break

    return avioes

def mover_avioes(lista):
    """Move todos os aviões uma casa na direção deles (wrap-around nas bordas)."""
    for av in lista:
        dr, dc = DIRECOES[av["direcao"]]
        av["casas"] = [((lin + dr) % 10, (col + dc) % 10) for lin, col in av["casas"]]

def verificar_acerto(lista, lin, col):
    """Retorna o índice do avião atingido em (lin, col), ou -1 se errou."""
    for i, av in enumerate(lista):
        if (lin, col) in av["casas"]:
            return i
    return -1

def casas_do_preview(lin0, col0, orientacao):
    """Retorna as 3 células que um avião ocuparia a partir de (lin0, col0)."""
    return [
        (lin0 + (j if orientacao == "V" else 0),
         col0 + (j if orientacao == "H" else 0))
        for j in range(3)
    ]

def preview_eh_valido(casas, ocupadas):
    """Checa se a posição do preview está dentro do grid e sem colisão."""
    return all(
        0 <= lin < 10 and 0 <= col < 10 and (lin, col) not in ocupadas
        for lin, col in casas
    )


# ==============================================================================
# BOTÕES DE DIREÇÃO (layout tipo WASD)
# ==============================================================================

def criar_botoes_direcao(cx, cy_topo):
    """
    Retorna um dict com os pygame.Rect dos 4 botões de direção,
    dispostos como as teclas WASD.
    """
    s, g = 52, 6   # tamanho e gap
    return {
        "W": pygame.Rect(cx - s//2,       cy_topo,           s, s),
        "A": pygame.Rect(cx - s - g - s//2, cy_topo + s + g, s, s),
        "S": pygame.Rect(cx - s//2,       cy_topo + s + g,   s, s),
        "D": pygame.Rect(cx + g + s//2,   cy_topo + s + g,   s, s),
    }

def desenhar_botoes_direcao(surf, botoes, atual, orientacao):
    """
    Desenha os 4 botões. Botões inválidos para a orientação ficam
    escurecidos (não podem ser clicados).
    """
    nomes = {"W": "Cima", "A": "Esq", "S": "Baixo", "D": "Dir"}
    validas = direcoes_validas_para(orientacao)
    mx, my = pygame.mouse.get_pos()

    for d, rect in botoes.items():
        disponivel = (d in validas)
        ativo      = (d == atual)
        hover      = rect.collidepoint(mx, my) and disponivel

        if not disponivel:
            # Acinzentado — não disponível para essa orientação
            cor_fundo  = (20, 30, 50)
            cor_borda  = (40, 50, 70)
            cor_texto  = (60, 70, 90)
        elif ativo:
            cor_fundo  = CIANO
            cor_borda  = BRANCO
            cor_texto  = AZUL_ESCURO
        elif hover:
            cor_fundo  = BOTAO_HOVER
            cor_borda  = CIANO
            cor_texto  = BRANCO
        else:
            cor_fundo  = BOTAO
            cor_borda  = CIANO
            cor_texto  = BRANCO

        pygame.draw.rect(surf, cor_fundo, rect, border_radius=6)
        pygame.draw.rect(surf, cor_borda, rect, 2, border_radius=6)
        escrever(surf, SETA[d],  fonte_media,   cor_texto, rect.centerx, rect.centery - 8)
        escrever(surf, nomes[d], fonte_mini,    cor_texto, rect.centerx, rect.centery + 14)


# ==============================================================================
# PAINEL DO GRID (fundo azul escuro em volta do tabuleiro)
# ==============================================================================

def fundo_grid(surf, ox):
    desenhar_painel(surf, pygame.Rect(
        ox - PAD_ESQUERDA - 8,
        GRID_Y - PAD_CIMA - 8,
        BOARD_W + PAD_ESQUERDA + 16,
        BOARD_H + PAD_CIMA + 16,
    ))


# ==============================================================================
# TELA DE POSICIONAMENTO DOS AVIÕES
# ==============================================================================

def posicionar_avioes(surf, clock, imagem_aviao):
    """
    Tela onde o jogador escolhe onde colocar seus 3 aviões.
    Retorna a lista de aviões confirmados.
    """
    avioes = []
    orientacao = "H"
    direcao    = "D"   # começa apontando para a direita
    idx = 0            # qual avião estamos posicionando

    # Botões de direção centralizados no painel direito
    botoes_dir = criar_botoes_direcao(CTRL_X, GRID_Y + 310)
    btn_girar  = pygame.Rect(CTRL_X - 100, GRID_Y + 255, 200, 38)

    while idx < 3:

        # --- Leitura de eventos ---
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_r, pygame.K_SPACE):
                    orientacao = "V" if orientacao == "H" else "H"
                    # Corrige a direção se não for válida para nova orientação
                    if direcao not in direcoes_validas_para(orientacao):
                        direcao = direcoes_validas_para(orientacao)[0]

                elif ev.key == pygame.K_w and "W" in direcoes_validas_para(orientacao):
                    direcao = "W"
                elif ev.key == pygame.K_s and "S" in direcoes_validas_para(orientacao):
                    direcao = "S"
                elif ev.key == pygame.K_a and "A" in direcoes_validas_para(orientacao):
                    direcao = "A"
                elif ev.key == pygame.K_d and "D" in direcoes_validas_para(orientacao):
                    direcao = "D"

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx_ev, my_ev = ev.pos

                # Clicou num botão de direção?
                for d, rect in botoes_dir.items():
                    if rect.collidepoint(mx_ev, my_ev):
                        if d in direcoes_validas_para(orientacao):
                            direcao = d

                # Clicou no botão de girar?
                if btn_girar.collidepoint(mx_ev, my_ev):
                    orientacao = "V" if orientacao == "H" else "H"
                    if direcao not in direcoes_validas_para(orientacao):
                        direcao = direcoes_validas_para(orientacao)[0]

                # Clicou no grid para confirmar posição?
                celula = pixel_para_celula(GRID_P_X, GRID_Y, mx_ev, my_ev)
                if celula:
                    lin0, col0 = celula
                    casas = casas_do_preview(lin0, col0, orientacao)
                    ocupadas = {c for av in avioes for c in av["casas"]}

                    if preview_eh_valido(casas, ocupadas):
                        avioes.append(criar_aviao(idx, casas, direcao, orientacao))
                        idx += 1

        # --- Preview do mouse ---
        mx, my = pygame.mouse.get_pos()
        celula_hover = pixel_para_celula(GRID_P_X, GRID_Y, mx, my)
        preview = []
        valido  = False

        if celula_hover:
            lin0, col0 = celula_hover
            preview = casas_do_preview(lin0, col0, orientacao)
            ocupadas = {c for av in avioes for c in av["casas"]}
            valido   = preview_eh_valido(preview, ocupadas)

        cor_preview = CORES_AVIOES[idx % 3] if valido else VERMELHO_ESC

        # --- Desenho ---
        surf.fill(AZUL_ESCURO)
        desenhar_titulo(surf, imagem_aviao)

        # Grid do jogador
        fundo_grid(surf, GRID_P_X)
        desenhar_grid(surf, GRID_P_X, GRID_Y, avioes, mostrar_avioes=True,
                      preview=preview if preview else None,
                      cor_preview=cor_preview,
                      ori_preview=orientacao,
                      dir_preview=direcao)
        escrever(surf, "TABULEIRO DO JOGADOR", fonte_media, CIANO,
                 GRID_P_X + BOARD_W // 2, GRID_Y - PAD_CIMA - 24)

        # --- Painel de controles à direita ---
        painel_rect = pygame.Rect(CTRL_X - 160, GRID_Y - PAD_CIMA - 8, 320, BOARD_H + PAD_CIMA + 16)
        desenhar_painel(surf, painel_rect)

        # Título do painel
        escrever(surf, f"Posicionando Aviao {idx+1} de 3",
                 fonte_media, BRANCO, CTRL_X, GRID_Y + 20)

        # Feedback de validade
        if valido:
            escrever(surf, "Posicao valida — clique para confirmar",
                     fonte_pequena, VERDE, CTRL_X, GRID_Y + 50)
        elif preview:
            escrever(surf, "Posicao invalida!",
                     fonte_pequena, VERMELHO, CTRL_X, GRID_Y + 50)
        else:
            escrever(surf, "Passe o mouse sobre o grid",
                     fonte_pequena, CINZA, CTRL_X, GRID_Y + 50)

        # Orientação atual
        ori_txt = "Horizontal  (—)" if orientacao == "H" else "Vertical  (|)"
        escrever(surf, f"Orientacao: {ori_txt}", fonte_pequena, LARANJA, CTRL_X, GRID_Y + 90)

        # Botão girar
        hover_girar = btn_girar.collidepoint(mx, my)
        destino_ori = "Vertical" if orientacao == "H" else "Horizontal"
        desenhar_botao(surf, btn_girar, f"[R] Girar -> {destino_ori}", hover_girar)

        # Botões de direção
        escrever(surf, "Direcao de voo:", fonte_media, CINZA, CTRL_X, GRID_Y + 298)
        desenhar_botoes_direcao(surf, botoes_dir, direcao, orientacao)

        nota = "Avioes horizontais: so esq/dir"  if orientacao == "H" else "Avioes verticais: so cima/baixo"
        escrever(surf, nota, fonte_mini, CINZA, CTRL_X, GRID_Y + 430)

        # Lista dos aviões já colocados
        if avioes:
            escrever(surf, "Ja posicionados:", fonte_pequena, CINZA, CTRL_X, GRID_Y + 460)
            for k, av in enumerate(avioes):
                ori_icone = "—" if av["orientacao"] == "H" else "|"
                linha_txt = f"Aviao {k+1}   {SETA[av['direcao']]}  {ori_icone}"
                escrever(surf, linha_txt, fonte_mini, av["cor"], CTRL_X, GRID_Y + 482 + k * 20)

        pygame.display.flip()
        clock.tick(FPS)

    return avioes


# ==============================================================================
# CENA DO JOGO (função que redesenha tudo durante a partida)
# ==============================================================================

def montar_cena(surf, imagem_aviao, avioes_jogador, avioes_cpu,
                rodada, mensagem, cor_msg, destaque_cpu=None):
    """
    Retorna uma função que redesenha a tela do jogo.
    Usada como callback pelas animações.
    """
    def redesenhar():
        surf.fill(AZUL_ESCURO)
        desenhar_titulo(surf, imagem_aviao)

        fundo_grid(surf, GRID_P_X)
        fundo_grid(surf, GRID_E_X)

        desenhar_grid(surf, GRID_P_X, GRID_Y, avioes_jogador, mostrar_avioes=True)
        desenhar_grid(surf, GRID_E_X, GRID_Y, avioes_cpu, mostrar_avioes=False,
                      destaque=destaque_cpu)

        escrever(surf, "SEUS AVIÕES",
                 fonte_media, CIANO, GRID_P_X + BOARD_W // 2, GRID_Y - PAD_CIMA - 24)
        escrever(surf, f"Restantes: {len(avioes_jogador)}",
                 fonte_mini, CINZA, GRID_P_X + BOARD_W // 2, GRID_Y + BOARD_H + 14)

        escrever(surf, "AVIÕES INIMIGOS",
                 fonte_media, CIANO, GRID_E_X + BOARD_W // 2, GRID_Y - PAD_CIMA - 24)
        escrever(surf, f"Restantes: {len(avioes_cpu)}",
                 fonte_mini, CINZA, GRID_E_X + BOARD_W // 2, GRID_Y + BOARD_H + 14)

        escrever(surf, f"Rodada {rodada}", fonte_mini, CINZA, LARGURA // 2, ALTURA - 44)
        escrever(surf, mensagem, fonte_pequena, cor_msg, LARGURA // 2, ALTURA - 26)

    return redesenhar


# ==============================================================================
# TELA DE RESULTADO FINAL
# ==============================================================================

def tela_fim(surf, clock, imagem_aviao, mensagem, cor):
    """Tela simples de fim de jogo com botão para voltar."""
    botao = pygame.Rect(LARGURA//2 - 130, ALTURA//2 + 80, 260, 48)

    while True:
        mx, my = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and botao.collidepoint(mx, my):
                return

        surf.fill(AZUL_ESCURO)
        desenhar_titulo(surf, imagem_aviao)
        escrever(surf, mensagem, fonte_grande, cor, LARGURA // 2, ALTURA // 2)
        desenhar_botao(surf, botao, "Voltar ao menu", botao.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(FPS)


# ==============================================================================
# FUNÇÃO PRINCIPAL — modo4()
# ==============================================================================

def modo4():
    """
    Abre a janela do jogo Batalha Aérea.
    Chamada pelo menu principal do batalha_naval.py.
    """
    if not pygame.get_init():
        pygame.init()

    surf  = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Batalha Aerea")
    clock = pygame.time.Clock()
    carregar_fontes()

    # Tenta carregar um ícone de avião (plane.png na mesma pasta)
    imagem_aviao = None
    try:
        caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plane.png")
        bruta = pygame.image.load(caminho).convert_alpha()
        escala = 50 / bruta.get_height()
        imagem_aviao = pygame.transform.smoothscale(
            bruta, (int(bruta.get_width() * escala), 50))
    except Exception:
        pass   # sem imagem, só o texto mesmo

    # Fase de posicionamento
    avioes_jogador = posicionar_avioes(surf, clock, imagem_aviao)
    avioes_cpu     = gerar_avioes_cpu(3)

    rodada  = 1
    msg     = "Sua vez! Clique no tabuleiro inimigo para atirar."
    cor_msg = BRANCO

    # Loop principal da partida
    while avioes_jogador and avioes_cpu:

        # ── Turno do jogador ─────────────────────────────────────────────────
        aguardando_clique = True
        while aguardando_clique:
            mx, my = pygame.mouse.get_pos()
            destaque = pixel_para_celula(GRID_E_X, GRID_Y, mx, my)

            redesenhar = montar_cena(surf, imagem_aviao, avioes_jogador, avioes_cpu,
                                     rodada, msg, cor_msg, destaque)
            redesenhar()
            pygame.display.flip()
            clock.tick(FPS)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and destaque:
                    lin, col = destaque
                    acerto = verificar_acerto(avioes_cpu, lin, col)

                    if acerto >= 0:
                        nome = avioes_cpu.pop(acerto)["nome"]
                        anim_explosao(surf, clock, GRID_E_X, GRID_Y, lin, col, redesenhar)
                        msg     = f"Você abateu o {nome} inimigo!"
                        cor_msg = EXPLOSAO
                    else:
                        anim_agua(surf, clock, GRID_E_X, GRID_Y, lin, col, redesenhar)
                        msg     = "Splash! O inimigo se moveu!"
                        cor_msg = AGUA

                    aguardando_clique = False

        if not avioes_cpu:
            break

        # ── Turno da CPU ─────────────────────────────────────────────────────
        pygame.time.wait(600)

        lin_cpu = random.randint(0, 9)
        col_cpu = random.randint(0, 9)

        msg_cpu = f"CPU atacou linha {lin_cpu+1}, coluna {LETRAS_COLUNAS[col_cpu]}..."
        redesenhar_cpu = montar_cena(surf, imagem_aviao, avioes_jogador, avioes_cpu,
                                     rodada, msg_cpu, LARANJA)
        redesenhar_cpu()
        pygame.display.flip()
        pygame.time.wait(700)

        acerto_cpu = verificar_acerto(avioes_jogador, lin_cpu, col_cpu)
        if acerto_cpu >= 0:
            nome = avioes_jogador.pop(acerto_cpu)["nome"]
            anim_explosao(surf, clock, GRID_P_X, GRID_Y, lin_cpu, col_cpu, redesenhar_cpu)
            msg     = f"CPU abateu seu {nome}!"
            cor_msg = VERMELHO
        else:
            anim_agua(surf, clock, GRID_P_X, GRID_Y, lin_cpu, col_cpu, redesenhar_cpu)
            msg     = f"CPU errou em {lin_cpu+1}{LETRAS_COLUNAS[col_cpu]}."
            cor_msg = AGUA

        if not avioes_jogador:
            break

        # ── Movimento ────────────────────────────────────────────────────────
        pygame.time.wait(300)

        redesenhar_base = montar_cena(surf, imagem_aviao, avioes_jogador, avioes_cpu,
                                      rodada, msg, cor_msg)
        # Anima primeiro, depois move de verdade
        anim_movimento(surf, clock, redesenhar_base, avioes_jogador, avioes_cpu)
        mover_avioes(avioes_cpu)
        mover_avioes(avioes_jogador)

        rodada += 1
        msg     = "Sua vez! Clique no tabuleiro inimigo para atirar."
        cor_msg = BRANCO

    # ── Resultado ────────────────────────────────────────────────────────────
    if not avioes_cpu and avioes_jogador:
        tela_fim(surf, clock, imagem_aviao, "Você venceu a Batalha Aérea!", VERDE)
    elif not avioes_jogador and avioes_cpu:
        tela_fim(surf, clock, imagem_aviao, "O computador venceu a Batalha Aérea...", VERMELHO)
    else:
        tela_fim(surf, clock, imagem_aviao, "Empate!", AMARELO)


# ==============================================================================
# RODAR DIRETO (para testar sem o menu principal)
# ==============================================================================

if __name__ == "__main__":
    pygame.init()
    modo4()
    pygame.quit()