"""
modo4_batalha_aerea.py  –  Batalha Aérea em janela Pygame
Requer: pip install pygame

Regras:
  • Cada avião ocupa 3 casas consecutivas (H ou V).
  • Ao posicionar, o jogador escolhe a direção de voo (W/A/S/D).
  • Após cada rodada completa, todos os aviões se movem 1 casa (wrap-around).
  • Acertar qualquer parte de um avião o destrói por completo.
  • Não há registro de água/explosão — o tabuleiro se move a cada turno.
  • Cada lado tem 3 aviões.

Compatibilidade: basta manter este arquivo na mesma pasta do main.py.
    from modo4_batalha_aerea import modo4
"""

import pygame
import random
import sys
import math
import time

# ─── Constantes visuais ───────────────────────────────────────────────────────

W, H       = 1100, 740
CELL       = 44
GAP        = 3
CELL_FULL  = CELL + GAP
ROWS       = 10
COLS       = 10
FPS        = 60
COLUNAS    = list("ABCDEFGHIJ")

# Paleta
C_BG        = ( 8,  16,  36)
C_OCEAN     = (14,  44,  86)
C_OCEAN_HL  = (20,  64, 118)
C_GRID      = (28,  64, 120)
C_WHITE     = (225, 238, 255)
C_GRAY      = (110, 130, 165)
C_TITLE     = ( 80, 195, 255)
C_PANEL     = (12,  24,  56)
C_BTN       = (28,  76, 155)
C_BTN_H     = (46, 114, 200)
C_BTN_PRESS = (18,  48, 105)
C_GREEN     = ( 50, 195,  90)
C_ORANGE    = (235, 135,  25)
C_PURPLE    = (155,  75, 215)
C_RED       = (215,  55,  55)
C_YELLOW    = (250, 205,  45)
C_HIT       = (220,  55,  40)
C_MISS      = ( 55, 125, 200)
C_DARK_RED  = (140,  30,  30)

PLANE_COLORS = [C_GREEN, C_ORANGE, C_PURPLE]

DIRECOES = {
    "W": (-1,  0),
    "S": ( 1,  0),
    "A": ( 0, -1),
    "D": ( 0,  1),
}
DIR_LABELS = {"W": "↑ Cima", "S": "↓ Baixo", "A": "← Esquerda", "D": "→ Direita"}

# ─── Helpers de desenho ───────────────────────────────────────────────────────

def _init_fonts():
    global FONT_TITLE, FONT_BIG, FONT_MED, FONT_SMALL, FONT_TINY
    try:
        FONT_TITLE = pygame.font.SysFont("impact",    60)
        FONT_BIG   = pygame.font.SysFont("consolas",  32, bold=True)
        FONT_MED   = pygame.font.SysFont("consolas",  20, bold=True)
        FONT_SMALL = pygame.font.SysFont("consolas",  15)
        FONT_TINY  = pygame.font.SysFont("consolas",  12)
    except Exception:
        FONT_TITLE = pygame.font.SysFont(None, 64)
        FONT_BIG   = pygame.font.SysFont(None, 36)
        FONT_MED   = pygame.font.SysFont(None, 24)
        FONT_SMALL = pygame.font.SysFont(None, 18)
        FONT_TINY  = pygame.font.SysFont(None, 14)

def txt(surf, text, font, color, x, y, anchor="center"):
    s = font.render(str(text), True, color)
    r = s.get_rect()
    setattr(r, anchor, (x, y))
    surf.blit(s, r)
    return r

def panel(surf, rect, border=C_GRID):
    pygame.draw.rect(surf, C_PANEL, rect, border_radius=10)
    pygame.draw.rect(surf, border, rect, 2, border_radius=10)

def button(surf, rect, label, hovered, pressed=False):
    col = C_BTN_PRESS if pressed else (C_BTN_H if hovered else C_BTN)
    pygame.draw.rect(surf, col, rect, border_radius=8)
    pygame.draw.rect(surf, C_TITLE, rect, 2, border_radius=8)
    txt(surf, label, FONT_MED, C_WHITE, rect.centerx, rect.centery)

def cell_px(ox, oy, r, c):
    """Pixel top-left da célula (r, c)."""
    return ox + c * CELL_FULL, oy + r * CELL_FULL

def px_to_cell(ox, oy, px, py):
    """Célula (r, c) a partir de pixel; None se fora."""
    c  = (px - ox) // CELL_FULL
    r  = (py - oy) // CELL_FULL
    rx = (px - ox) % CELL_FULL
    ry = (py - oy) % CELL_FULL
    if 0 <= r < ROWS and 0 <= c < COLS and rx < CELL and ry < CELL:
        return r, c
    return None

def draw_grid(surf, ox, oy, avioes, show_planes=True,
              highlight=None, preview=None, preview_color=C_GREEN):
    """Desenha tabuleiro aéreo 10×10."""
    # células
    for r in range(ROWS):
        for c in range(COLS):
            x, y = cell_px(ox, oy, r, c)
            rc   = pygame.Rect(x, y, CELL, CELL)
            color = C_OCEAN_HL if highlight == (r, c) else C_OCEAN
            pygame.draw.rect(surf, color, rc, border_radius=3)
            pygame.draw.rect(surf, C_GRID, rc, 1, border_radius=3)

    # aviões
    if show_planes:
        for i, av in enumerate(avioes):
            col = av.get("color", PLANE_COLORS[i % 3])
            for (r, c) in av["casas"]:
                x, y = cell_px(ox, oy, r, c)
                rc   = pygame.Rect(x, y, CELL, CELL)
                pygame.draw.rect(surf, col, rc, border_radius=3)
                pygame.draw.rect(surf, C_WHITE, rc, 1, border_radius=3)
                txt(surf, "✈", FONT_SMALL, C_WHITE, x + CELL//2, y + CELL//2)

    # preview de posicionamento
    if preview:
        for (r, c) in preview:
            if 0 <= r < ROWS and 0 <= c < COLS:
                x, y = cell_px(ox, oy, r, c)
                rc   = pygame.Rect(x, y, CELL, CELL)
                pygame.draw.rect(surf, preview_color, rc, border_radius=3)
                pygame.draw.rect(surf, C_WHITE, rc, 2, border_radius=3)
                txt(surf, "✈", FONT_SMALL, C_WHITE, x + CELL//2, y + CELL//2)

    # marcadores de acerto/erro (explosões salvas no dict do avião já removido;
    # aqui salvamos na lista hit_marks externa se precisar — veja abaixo)

    # rótulos
    for c in range(COLS):
        x, y = cell_px(ox, oy, 0, c)
        txt(surf, COLUNAS[c], FONT_TINY, C_GRAY, x + CELL//2, y - 9)
    for r in range(ROWS):
        x, y = cell_px(ox, oy, r, 0)
        txt(surf, str(r + 1), FONT_TINY, C_GRAY, x - 13, y + CELL//2)

# ─── Animações ────────────────────────────────────────────────────────────────

def anim_abate(surf, clock, ox, oy, r, c, draw_bg_fn):
    """Explosão expandindo na célula (r, c)."""
    cx, cy = cell_px(ox, oy, r, c)
    cx += CELL // 2
    cy += CELL // 2
    for frame in range(30):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        draw_bg_fn()
        prog  = frame / 29
        radius = int(prog * 55)
        alpha  = int(255 * (1 - prog))
        s = pygame.Surface((radius*2+4, radius*2+4), pygame.SRCALPHA)
        pygame.draw.circle(s, (*C_HIT, alpha),   (radius+2, radius+2), radius+2)
        pygame.draw.circle(s, (*C_YELLOW, alpha), (radius+2, radius+2), max(1, radius-6))
        surf.blit(s, (cx - radius - 2, cy - radius - 2))
        pygame.display.flip()
        clock.tick(FPS)

def anim_erro(surf, clock, ox, oy, r, c, draw_bg_fn):
    """Splash de água na célula (r, c)."""
    cx, cy = cell_px(ox, oy, r, c)
    cx += CELL // 2
    cy += CELL // 2
    for frame in range(24):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        draw_bg_fn()
        prog   = frame / 23
        radius = int(prog * 40)
        alpha  = int(255 * (1 - prog))
        s = pygame.Surface((radius*2+4, radius*2+4), pygame.SRCALPHA)
        pygame.draw.circle(s, (*C_MISS, alpha), (radius+2, radius+2), radius+2)
        surf.blit(s, (cx - radius - 2, cy - radius - 2))
        pygame.display.flip()
        clock.tick(FPS)

# ─── Tela de resultado ────────────────────────────────────────────────────────

def tela_resultado(surf, clock, msg, color):
    btn = pygame.Rect(W//2 - 130, H//2 + 60, 260, 48)
    while True:
        mx, my = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(mx, my):
                return
        surf.fill(C_BG)
        txt(surf, msg, FONT_BIG, color, W//2, H//2 - 20)
        button(surf, btn, "Voltar ao menu", btn.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(FPS)

# ─── Lógica de aviões ─────────────────────────────────────────────────────────

def make_aviao(idx, casas, direcao):
    return {
        "casas":   list(casas),
        "direcao": direcao,
        "nome":    f"Avião {idx + 1}",
        "color":   PLANE_COLORS[idx % 3],
    }

def cpu_gerar_avioes(n=3):
    result   = []
    ocupadas = set()
    for i in range(n):
        while True:
            ori  = random.choice(("H", "V"))
            r0   = random.randint(0, 9)
            c0   = random.randint(0, 9)
            cells = []
            ok   = True
            for j in range(3):
                nr = r0 + (j if ori == "V" else 0)
                nc = c0 + (j if ori == "H" else 0)
                if not (0 <= nr < 10 and 0 <= nc < 10) or (nr, nc) in ocupadas:
                    ok = False; break
                cells.append((nr, nc))
            if ok:
                for cl in cells:
                    ocupadas.add(cl)
                result.append(make_aviao(i, cells, random.choice(list(DIRECOES.keys()))))
                break
    return result

def mover_avioes(lista):
    for av in lista:
        dr, dc = DIRECOES[av["direcao"]]
        av["casas"] = [((r + dr) % 10, (c + dc) % 10) for r, c in av["casas"]]

def check_hit(lista, r, c):
    """Retorna índice do avião atingido ou -1."""
    for i, av in enumerate(lista):
        if (r, c) in av["casas"]:
            return i
    return -1

def preview_casas(r0, c0, ori):
    cells = []
    for j in range(3):
        nr = r0 + (j if ori == "V" else 0)
        nc = c0 + (j if ori == "H" else 0)
        cells.append((nr, nc))
    return cells

def preview_valido(cells, ocupadas):
    return all(0 <= r < 10 and 0 <= c < 10 and (r, c) not in ocupadas
               for r, c in cells)

# ─── Fase de posicionamento ───────────────────────────────────────────────────

def fase_posicionamento(surf, clock):
    avioes_p = []
    ori      = "H"
    direcao  = "D"
    OX, OY   = 85, 95

    for idx in range(3):
        placed = False
        while not placed:
            mx, my = pygame.mouse.get_pos()
            cell   = px_to_cell(OX, OY, mx, my)

            prev   = preview_casas(cell[0], cell[1], ori) if cell else []
            ocup   = {c for av in avioes_p for c in av["casas"]}
            valid  = preview_valido(prev, ocup) if prev else False
            prev_col = PLANE_COLORS[idx] if valid else C_DARK_RED

            # ── eventos ──
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    k = ev.key
                    if k == pygame.K_r or k == pygame.K_SPACE:
                        ori = "V" if ori == "H" else "H"
                    elif k == pygame.K_w: direcao = "W"
                    elif k == pygame.K_s: direcao = "S"
                    elif k == pygame.K_a: direcao = "A"
                    elif k == pygame.K_d: direcao = "D"
                if ev.type == pygame.MOUSEBUTTONDOWN and valid:
                    avioes_p.append(make_aviao(idx, prev, direcao))
                    placed = True

            # ── desenho ──
            surf.fill(C_BG)

            # painel esquerdo — grid
            panel(surf, pygame.Rect(20, 20, 560, 700))
            draw_grid(surf, OX, OY, avioes_p, show_planes=True,
                      preview=prev, preview_color=prev_col)
            txt(surf, "SEU TABULEIRO", FONT_MED, C_TITLE, OX + 218, 60)

            # painel direito — instruções
            info_x = 630
            panel(surf, pygame.Rect(610, 20, 470, 700))
            txt(surf, "BATALHA AÉREA", FONT_TITLE, C_TITLE, info_x + 215, 80)

            lines = [
                ("Posicione seus 3 aviões",          C_WHITE, FONT_MED,  160),
                (f"Avião {idx+1}/3",                 PLANE_COLORS[idx], FONT_BIG, 220),
                ("",                                  C_WHITE, FONT_SMALL, 260),
                ("[R] ou [Espaço]  →  girar",        C_GRAY,  FONT_SMALL, 295),
                (f"Orientação atual:  {'Horizontal' if ori=='H' else 'Vertical'}",
                                                      C_WHITE, FONT_SMALL, 325),
                ("",                                  C_WHITE, FONT_SMALL, 355),
                ("Direção de voo  [W/A/S/D]:",       C_GRAY,  FONT_SMALL, 385),
                (DIR_LABELS[direcao],                C_YELLOW, FONT_MED,  420),
                ("",                                  C_WHITE, FONT_SMALL, 455),
                ("Clique no grid para confirmar",     C_GRAY,  FONT_SMALL, 490),
            ]
            for (t, col, font, y) in lines:
                if t:
                    txt(surf, t, font, col, info_x + 215, y)

            # legenda de aviões já posicionados
            if avioes_p:
                txt(surf, "Já posicionados:", FONT_SMALL, C_GRAY, info_x + 215, 550)
                for k, av in enumerate(avioes_p):
                    txt(surf, f"  {av['nome']}  {DIR_LABELS[av['direcao']]}",
                        FONT_SMALL, av["color"], info_x + 215, 575 + k * 22)

            pygame.display.flip()
            clock.tick(FPS)

    return avioes_p

# ─── Loop principal do modo ───────────────────────────────────────────────────

def modo4():
    # Garantir pygame inicializado (o main.py já chama pygame.init(),
    # mas chamamos novamente para o caso de uso standalone)
    if not pygame.get_init():
        pygame.init()

    surf  = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Batalha Aérea ✈")
    clock = pygame.time.Clock()

    _init_fonts()

    # ── posicionamento ──
    avioes_p   = fase_posicionamento(surf, clock)
    avioes_cpu = cpu_gerar_avioes(3)

    rodada  = 1
    msg     = "Sua vez — clique no tabuleiro inimigo para atirar."
    msg_col = C_WHITE

    OX_P,  OY_P  = 30,  95    # grid do jogador
    OX_E,  OY_E  = 600, 95    # grid inimigo

    while avioes_p and avioes_cpu:

        # ── turno do jogador ──
        player_done = False
        while not player_done:
            mx, my = pygame.mouse.get_pos()
            cell_e = px_to_cell(OX_E, OY_E, mx, my)

            def draw_scene():
                surf.fill(C_BG)

                # painéis
                panel(surf, pygame.Rect(15,  15, 555, 710))
                panel(surf, pygame.Rect(585, 15, 510, 710))

                # grids
                draw_grid(surf, OX_P, OY_P, avioes_p,   show_planes=True)
                draw_grid(surf, OX_E, OY_E, avioes_cpu, show_planes=False,
                          highlight=cell_e)

                # rótulos
                txt(surf, "SEUS AVIÕES",      FONT_MED, C_TITLE, OX_P + 218,  60)
                txt(surf, f"Restantes: {len(avioes_p)}",
                    FONT_SMALL, C_GRAY, OX_P + 218, 660)
                txt(surf, "AVIÕES INIMIGOS", FONT_MED, C_TITLE, OX_E + 218,  60)
                txt(surf, f"Restantes: {len(avioes_cpu)}",
                    FONT_SMALL, C_GRAY, OX_E + 218, 660)
                txt(surf, f"Rodada {rodada}", FONT_SMALL, C_GRAY, W//2, 690)
                txt(surf, msg, FONT_SMALL, msg_col, W//2, 715)

            draw_scene()
            pygame.display.flip()
            clock.tick(FPS)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and cell_e:
                    r, c = cell_e
                    idx  = check_hit(avioes_cpu, r, c)
                    if idx >= 0:
                        nome = avioes_cpu.pop(idx)["nome"]
                        anim_abate(surf, clock, OX_E, OY_E, r, c, draw_scene)
                        msg     = f"💥 Você abateu o {nome} inimigo!"
                        msg_col = C_HIT
                    else:
                        anim_erro(surf, clock, OX_E, OY_E, r, c, draw_scene)
                        msg     = "Tiro no vazio — inimigo em outro lugar!"
                        msg_col = C_MISS
                    player_done = True

        if not avioes_cpu:
            break

        # ── turno da CPU ──
        pygame.time.wait(700)
        r_cpu = random.randint(0, 9)
        c_cpu = random.randint(0, 9)

        def draw_cpu_turn():
            surf.fill(C_BG)
            panel(surf, pygame.Rect(15,  15, 555, 710))
            panel(surf, pygame.Rect(585, 15, 510, 710))
            draw_grid(surf, OX_P, OY_P, avioes_p,   show_planes=True)
            draw_grid(surf, OX_E, OY_E, avioes_cpu, show_planes=False)
            txt(surf, "SEUS AVIÕES",     FONT_MED, C_TITLE, OX_P+218, 60)
            txt(surf, f"Restantes: {len(avioes_p)}", FONT_SMALL, C_GRAY, OX_P+218, 660)
            txt(surf, "AVIÕES INIMIGOS", FONT_MED, C_TITLE, OX_E+218, 60)
            txt(surf, f"Restantes: {len(avioes_cpu)}", FONT_SMALL, C_GRAY, OX_E+218, 660)
            txt(surf, f"CPU atacou  {r_cpu+1}{COLUNAS[c_cpu]}  …",
                FONT_MED, C_ORANGE, W//2, 715)

        draw_cpu_turn()
        pygame.display.flip()
        pygame.time.wait(600)

        idx_j = check_hit(avioes_p, r_cpu, c_cpu)
        if idx_j >= 0:
            nome = avioes_p.pop(idx_j)["nome"]
            anim_abate(surf, clock, OX_P, OY_P, r_cpu, c_cpu, draw_cpu_turn)
            msg     = f"CPU abateu seu {nome}!"
            msg_col = C_RED
        else:
            anim_erro(surf, clock, OX_P, OY_P, r_cpu, c_cpu, draw_cpu_turn)
            msg     = f"CPU errou em {r_cpu+1}{COLUNAS[c_cpu]}."
            msg_col = C_MISS

        if not avioes_p:
            break

        # ── mover aviões ──
        pygame.time.wait(500)
        mover_avioes(avioes_cpu)
        mover_avioes(avioes_p)

        # flash de movimento
        surf.fill(C_BG)
        panel(surf, pygame.Rect(15,  15, 555, 710))
        panel(surf, pygame.Rect(585, 15, 510, 710))
        draw_grid(surf, OX_P, OY_P, avioes_p,   show_planes=True)
        draw_grid(surf, OX_E, OY_E, avioes_cpu, show_planes=False)
        txt(surf, "SEUS AVIÕES",     FONT_MED, C_TITLE, OX_P+218, 60)
        txt(surf, "AVIÕES INIMIGOS", FONT_MED, C_TITLE, OX_E+218, 60)
        txt(surf, "✈  Os aviões se moveram!  ✈", FONT_MED, C_YELLOW, W//2, 715)
        pygame.display.flip()
        pygame.time.wait(900)

        rodada += 1
        msg     = "Sua vez — clique no tabuleiro inimigo para atirar."
        msg_col = C_WHITE

    # ── resultado ──
    if not avioes_cpu and avioes_p:
        tela_resultado(surf, clock, "🎉 Você venceu a Batalha Aérea!", C_GREEN)
    elif not avioes_p and avioes_cpu:
        tela_resultado(surf, clock, "😞 A CPU venceu a Batalha Aérea...", C_RED)
    else:
        tela_resultado(surf, clock, "🤝 Empate!", C_YELLOW)


# ─── Execução standalone (opcional) ──────────────────────────────────────────
if __name__ == "__main__":
    pygame.init()
    modo4()
    pygame.quit()
