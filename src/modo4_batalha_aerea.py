import pygame
import random
import sys
import os
import math

LARGURA, ALTURA = 1200, 820
CELULA   = 46
ESPACO   = 3
PASSO    = CELULA + ESPACO
LINHAS = COLUNAS = 10
FPS = 60

LETRAS_COLUNAS = list("ABCDEFGHIJ")

BOARD_W      = COLUNAS * PASSO - ESPACO
BOARD_H      = LINHAS  * PASSO - ESPACO
MARGEM_X     = 73
PAD_ESQUERDA = 28
PAD_CIMA     = 18

GRID_P_X = MARGEM_X + PAD_ESQUERDA
GRID_E_X = MARGEM_X + BOARD_W + 80 + PAD_ESQUERDA
GRID_Y   = 130 + PAD_CIMA
CTRL_X   = GRID_P_X + BOARD_W + (LARGURA - GRID_P_X - BOARD_W) // 2

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

CORES_AVIOES = [VERDE, LARANJA, ROXO]

DIRECOES = {"W": (-1, 0), "S": (1, 0), "A": (0, -1), "D": (0, 1)}
SETA     = {"W": "^", "S": "v", "A": "<", "D": ">"}

fonte_titulo = fonte_grande = fonte_media = fonte_pequena = fonte_mini = None

def carregar_fontes():
    global fonte_titulo, fonte_grande, fonte_media, fonte_pequena, fonte_mini
    for nome in ("impact", None):
        try:
            fonte_titulo = pygame.font.SysFont(nome, 56, bold=(nome is None))
            break
        except Exception:
            pass
    for nome in ("consolas", "courier new", None):
        try:
            fonte_grande  = pygame.font.SysFont(nome, 30, bold=True)
            fonte_media   = pygame.font.SysFont(nome, 19, bold=True)
            fonte_pequena = pygame.font.SysFont(nome, 15)
            fonte_mini    = pygame.font.SysFont(nome, 12)
            break
        except Exception:
            pass

def escrever(surf, texto, fonte, cor, x, y, ancora="center"):
    s = fonte.render(str(texto), True, cor)
    r = s.get_rect()
    setattr(r, ancora, (x, y))
    surf.blit(s, r)
    return r

def desenhar_painel(surf, rect):
    pygame.draw.rect(surf, PAINEL, rect, border_radius=10)
    pygame.draw.rect(surf, GRADE,  rect, 2, border_radius=10)

def desenhar_botao(surf, rect, texto, destacado):
    cor = BOTAO_HOVER if destacado else BOTAO
    pygame.draw.rect(surf, cor,   rect, border_radius=8)
    pygame.draw.rect(surf, CIANO, rect, 2, border_radius=8)
    escrever(surf, texto, fonte_media, BRANCO, rect.centerx, rect.centery)

def pos_celula(ox, oy, linha, col):
    return ox + col * PASSO, oy + linha * PASSO

def pixel_para_celula(ox, oy, px, py):
    rx, ry = px - ox, py - oy
    if rx < 0 or ry < 0:
        return None
    col, sobra_x = divmod(rx, PASSO)
    lin, sobra_y = divmod(ry, PASSO)
    if 0 <= lin < LINHAS and 0 <= col < COLUNAS and sobra_x < CELULA and sobra_y < CELULA:
        return lin, col
    return None

def desenhar_aviao(surf, cx, cy, tamanho, cor, direcao="D"):
    s = tamanho
    angulo = {"D": 0, "A": math.pi, "S": math.pi/2, "W": -math.pi/2}.get(direcao, 0)
    cos_a, sin_a = math.cos(angulo), math.sin(angulo)

    def girar(x, y):
        dx, dy = x - cx, y - cy
        return (cx + dx*cos_a - dy*sin_a, cy + dx*sin_a + dy*cos_a)

    pygame.draw.line(surf, cor, girar(cx-s, cy), girar(cx+s*2, cy), 3)
    pygame.draw.polygon(surf, cor, [girar(cx-s//2, cy), girar(cx+s//2, cy), girar(cx, cy-s)])
    pygame.draw.polygon(surf, cor, [girar(cx-s//2, cy), girar(cx+s//2, cy), girar(cx, cy+s)])
    pygame.draw.line(surf, cor, girar(cx-s, cy), girar(cx-s-s//2, cy-s//2), 2)
    pygame.draw.line(surf, cor, girar(cx-s, cy), girar(cx-s-s//2, cy+s//2), 2)

def desenhar_grid(surf, ox, oy, lista_avioes, mostrar_avioes=True,
                  destaque=None, preview=None, cor_preview=VERDE,
                  ori_preview="H", dir_preview="D"):
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            x, y = pos_celula(ox, oy, lin, col)
            cor = OCEANO_HL if destaque == (lin, col) else OCEANO
            pygame.draw.rect(surf, cor,   (x, y, CELULA, CELULA), border_radius=3)
            pygame.draw.rect(surf, GRADE, (x, y, CELULA, CELULA), 1, border_radius=3)

    if mostrar_avioes:
        for av in lista_avioes:
            for (lin, col) in av["casas"]:
                x, y = pos_celula(ox, oy, lin, col)
                pygame.draw.rect(surf, av["cor"], (x, y, CELULA, CELULA), border_radius=3)
                pygame.draw.rect(surf, BRANCO,    (x, y, CELULA, CELULA), 1, border_radius=3)
            lin_meio, col_meio = av["casas"][1]
            desenhar_aviao(surf,
                           ox + col_meio * PASSO + CELULA // 2,
                           oy + lin_meio * PASSO + CELULA // 2,
                           9, BRANCO, av["direcao"])

    if preview:
        for (lin, col) in preview:
            if 0 <= lin < LINHAS and 0 <= col < COLUNAS:
                x, y = pos_celula(ox, oy, lin, col)
                pygame.draw.rect(surf, cor_preview, (x, y, CELULA, CELULA), border_radius=3)
                pygame.draw.rect(surf, BRANCO,      (x, y, CELULA, CELULA), 2, border_radius=3)
        if len(preview) >= 2:
            lin_m, col_m = preview[1]
            if 0 <= lin_m < LINHAS and 0 <= col_m < COLUNAS:
                desenhar_aviao(surf,
                               ox + col_m * PASSO + CELULA // 2,
                               oy + lin_m * PASSO + CELULA // 2,
                               9, BRANCO, dir_preview)

    for col in range(COLUNAS):
        x, _ = pos_celula(ox, oy, 0, col)
        escrever(surf, LETRAS_COLUNAS[col], fonte_mini, CINZA, x + CELULA//2, oy - 10)
    for lin in range(LINHAS):
        _, y = pos_celula(ox, oy, lin, 0)
        escrever(surf, str(lin+1), fonte_mini, CINZA, ox - 14, y + CELULA//2)

def anim_explosao(surf, clock, ox, oy, lin, col, redesenhar, som=None):
    cx = ox + col * PASSO + CELULA // 2
    cy = oy + lin * PASSO + CELULA // 2
    if som:
        som.play()
    for frame in range(36):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        redesenhar()
        prog  = frame / 35
        raio  = int(prog * 62)
        alpha = int(255 * (1 - prog))
        s = pygame.Surface((raio*2+4, raio*2+4), pygame.SRCALPHA)
        pygame.draw.circle(s, (*EXPLOSAO, alpha), (raio+2, raio+2), raio+2)
        pygame.draw.circle(s, (*AMARELO,  alpha), (raio+2, raio+2), max(1, raio-8))
        surf.blit(s, (cx-raio-2, cy-raio-2))
        pygame.display.flip()
        clock.tick(FPS)

def anim_agua(surf, clock, ox, oy, lin, col, redesenhar, som=None):
    cx = ox + col * PASSO + CELULA // 2
    cy = oy + lin * PASSO + CELULA // 2
    if som:
        som.play()
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

def desenhar_titulo(surf, imagem_aviao):
    ts = fonte_titulo.render("BATALHA AEREA", True, CIANO)
    tw, th = ts.get_size()
    img_w = imagem_aviao.get_width() if imagem_aviao else 0
    gap   = 12
    total = img_w + (gap if imagem_aviao else 0) + tw
    sx, yc = LARGURA // 2 - total // 2, 38
    if imagem_aviao:
        surf.blit(imagem_aviao, (sx, yc - imagem_aviao.get_height() // 2))
        surf.blit(ts, (sx + img_w + gap, yc - th // 2))
    else:
        surf.blit(ts, (LARGURA // 2 - tw // 2, yc - th // 2))

def criar_aviao(indice, casas, direcao, orientacao):
    return {
        "casas":      list(casas),
        "direcao":    direcao,
        "orientacao": orientacao,
        "nome":       f"Aviao {indice + 1}",
        "cor":        CORES_AVIOES[indice % 3],
    }

def direcoes_validas_para(orientacao):
    return ["A", "D"] if orientacao == "H" else ["W", "S"]

def gerar_avioes_cpu(quantidade=3):
    avioes = []
    ocupadas = set()
    for i in range(quantidade):
        while True:
            ori  = random.choice(("H", "V"))
            lin0 = random.randint(0, 9)
            col0 = random.randint(0, 9)
            casas, valido = [], True
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
                avioes.append(criar_aviao(i, casas, random.choice(direcoes_validas_para(ori)), ori))
                break
    return avioes

def mover_avioes(lista):
    for av in lista:
        dr, dc = DIRECOES[av["direcao"]]
        av["casas"] = [((lin + dr) % 10, (col + dc) % 10) for lin, col in av["casas"]]

def verificar_acerto(lista, lin, col):
    for i, av in enumerate(lista):
        if (lin, col) in av["casas"]:
            return i
    return -1

def casas_do_preview(lin0, col0, orientacao):
    return [(lin0 + (j if orientacao == "V" else 0), col0 + (j if orientacao == "H" else 0))
            for j in range(3)]

def preview_eh_valido(casas, ocupadas):
    return all(0 <= lin < 10 and 0 <= col < 10 and (lin, col) not in ocupadas
               for lin, col in casas)

def criar_botoes_direcao(cx, cy_topo):
    s, g = 52, 6
    return {
        "W": pygame.Rect(cx - s//2,         cy_topo,         s, s),
        "A": pygame.Rect(cx - s - g - s//2, cy_topo + s + g, s, s),
        "S": pygame.Rect(cx - s//2,         cy_topo + s + g, s, s),
        "D": pygame.Rect(cx + g + s//2,     cy_topo + s + g, s, s),
    }

def desenhar_botoes_direcao(surf, botoes, atual, orientacao):
    nomes   = {"W": "Cima", "A": "Esq", "S": "Baixo", "D": "Dir"}
    validas = direcoes_validas_para(orientacao)
    mx, my  = pygame.mouse.get_pos()
    for d, rect in botoes.items():
        disponivel = (d in validas)
        ativo      = (d == atual)
        hover      = rect.collidepoint(mx, my) and disponivel
        if not disponivel:
            cor_fundo, cor_borda, cor_texto = (20, 30, 50), (40, 50, 70), (60, 70, 90)
        elif ativo:
            cor_fundo, cor_borda, cor_texto = CIANO, BRANCO, AZUL_ESCURO
        elif hover:
            cor_fundo, cor_borda, cor_texto = BOTAO_HOVER, CIANO, BRANCO
        else:
            cor_fundo, cor_borda, cor_texto = BOTAO, CIANO, BRANCO
        pygame.draw.rect(surf, cor_fundo, rect, border_radius=6)
        pygame.draw.rect(surf, cor_borda, rect, 2, border_radius=6)
        escrever(surf, SETA[d],  fonte_media, cor_texto, rect.centerx, rect.centery - 8)
        escrever(surf, nomes[d], fonte_mini,  cor_texto, rect.centerx, rect.centery + 14)

def fundo_grid(surf, ox):
    desenhar_painel(surf, pygame.Rect(
        ox - PAD_ESQUERDA - 8, GRID_Y - PAD_CIMA - 8,
        BOARD_W + PAD_ESQUERDA + 16, BOARD_H + PAD_CIMA + 16,
    ))

def posicionar_avioes(surf, clock, imagem_aviao):
    avioes     = []
    orientacao = "H"
    direcao    = "D"
    idx        = 0

    botoes_dir = criar_botoes_direcao(CTRL_X, GRID_Y + 310)
    btn_girar  = pygame.Rect(CTRL_X - 100, GRID_Y + 255, 200, 38)

    while idx < 3:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_r, pygame.K_SPACE):
                    orientacao = "V" if orientacao == "H" else "H"
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
                for d, rect in botoes_dir.items():
                    if rect.collidepoint(mx_ev, my_ev) and d in direcoes_validas_para(orientacao):
                        direcao = d
                if btn_girar.collidepoint(mx_ev, my_ev):
                    orientacao = "V" if orientacao == "H" else "H"
                    if direcao not in direcoes_validas_para(orientacao):
                        direcao = direcoes_validas_para(orientacao)[0]
                celula = pixel_para_celula(GRID_P_X, GRID_Y, mx_ev, my_ev)
                if celula:
                    lin0, col0 = celula
                    casas    = casas_do_preview(lin0, col0, orientacao)
                    ocupadas = {c for av in avioes for c in av["casas"]}
                    if preview_eh_valido(casas, ocupadas):
                        avioes.append(criar_aviao(idx, casas, direcao, orientacao))
                        idx += 1

        mx, my       = pygame.mouse.get_pos()
        celula_hover = pixel_para_celula(GRID_P_X, GRID_Y, mx, my)
        preview      = []
        valido       = False

        if celula_hover:
            lin0, col0 = celula_hover
            preview  = casas_do_preview(lin0, col0, orientacao)
            ocupadas = {c for av in avioes for c in av["casas"]}
            valido   = preview_eh_valido(preview, ocupadas)

        cor_preview = CORES_AVIOES[idx % 3] if valido else VERMELHO_ESC

        surf.fill(AZUL_ESCURO)
        desenhar_titulo(surf, imagem_aviao)

        fundo_grid(surf, GRID_P_X)
        desenhar_grid(surf, GRID_P_X, GRID_Y, avioes, mostrar_avioes=True,
                      preview=preview if preview else None,
                      cor_preview=cor_preview, ori_preview=orientacao, dir_preview=direcao)
        escrever(surf, "SEU TABULEIRO", fonte_media, CIANO,
                 GRID_P_X + BOARD_W // 2, GRID_Y - PAD_CIMA - 24)

        desenhar_painel(surf, pygame.Rect(CTRL_X - 160, GRID_Y - PAD_CIMA - 8, 320, BOARD_H + PAD_CIMA + 16))

        escrever(surf, f"Posicionando Aviao {idx+1} de 3", fonte_media, BRANCO, CTRL_X, GRID_Y + 20)

        if valido:
            escrever(surf, "Posicao valida — clique para confirmar", fonte_pequena, VERDE,    CTRL_X, GRID_Y + 50)
        elif preview:
            escrever(surf, "Posicao invalida!",                      fonte_pequena, VERMELHO, CTRL_X, GRID_Y + 50)
        else:
            escrever(surf, "Passe o mouse sobre o grid",             fonte_pequena, CINZA,    CTRL_X, GRID_Y + 50)

        ori_txt = "Horizontal  (—)" if orientacao == "H" else "Vertical  (|)"
        escrever(surf, f"Orientacao: {ori_txt}", fonte_pequena, LARANJA, CTRL_X, GRID_Y + 90)

        destino_ori = "Vertical" if orientacao == "H" else "Horizontal"
        desenhar_botao(surf, btn_girar, f"[R] Girar -> {destino_ori}", btn_girar.collidepoint(mx, my))

        escrever(surf, "Direcao de voo:", fonte_media, CINZA, CTRL_X, GRID_Y + 298)
        desenhar_botoes_direcao(surf, botoes_dir, direcao, orientacao)

        nota = "Horizontais: so esq/dir" if orientacao == "H" else "Verticais: so cima/baixo"
        escrever(surf, nota, fonte_mini, CINZA, CTRL_X, GRID_Y + 430)

        if avioes:
            escrever(surf, "Ja posicionados:", fonte_pequena, CINZA, CTRL_X, GRID_Y + 460)
            for k, av in enumerate(avioes):
                ori_icone = "—" if av["orientacao"] == "H" else "|"
                escrever(surf, f"Aviao {k+1}   {SETA[av['direcao']]}  {ori_icone}",
                         fonte_mini, av["cor"], CTRL_X, GRID_Y + 482 + k * 20)

        pygame.display.flip()
        clock.tick(FPS)

    return avioes

def montar_cena(surf, imagem_aviao, avioes_jogador, avioes_cpu, rodada, mensagem, cor_msg, destaque_cpu=None, hack=False):
    def redesenhar():
        surf.fill(AZUL_ESCURO)
        desenhar_titulo(surf, imagem_aviao)
        fundo_grid(surf, GRID_P_X)
        fundo_grid(surf, GRID_E_X)
        desenhar_grid(surf, GRID_P_X, GRID_Y, avioes_jogador, mostrar_avioes=True)
        desenhar_grid(surf, GRID_E_X, GRID_Y, avioes_cpu, mostrar_avioes=hack, destaque=destaque_cpu)
        escrever(surf, "SEUS AVIOES",     fonte_media, CIANO, GRID_P_X + BOARD_W // 2, GRID_Y - PAD_CIMA - 24)
        escrever(surf, f"Restantes: {len(avioes_jogador)}", fonte_mini, CINZA, GRID_P_X + BOARD_W // 2, GRID_Y + BOARD_H + 14)
        escrever(surf, "AVIOES INIMIGOS", fonte_media, CIANO, GRID_E_X + BOARD_W // 2, GRID_Y - PAD_CIMA - 24)
        escrever(surf, f"Restantes: {len(avioes_cpu)}",    fonte_mini, CINZA, GRID_E_X + BOARD_W // 2, GRID_Y + BOARD_H + 14)
        escrever(surf, f"Rodada {rodada}", fonte_mini,    CINZA,   LARGURA // 2, ALTURA - 44)
        escrever(surf, mensagem,           fonte_pequena, cor_msg, LARGURA // 2, ALTURA - 26)
    return redesenhar

def tela_fim(surf, clock, imagem_aviao, mensagem, cor):
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

def modo4(hack=False, som_explosao=None, som_splash=None):
    if not pygame.get_init():
        pygame.init()

    surf  = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Batalha Aerea")
    clock = pygame.time.Clock()
    carregar_fontes()

    imagem_aviao = None
    try:
        caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plane.png")
        bruta   = pygame.image.load(caminho).convert_alpha()
        escala  = 50 / bruta.get_height()
        imagem_aviao = pygame.transform.smoothscale(bruta, (int(bruta.get_width() * escala), 50))
    except Exception:
        pass

    avioes_jogador = posicionar_avioes(surf, clock, imagem_aviao)
    avioes_cpu     = gerar_avioes_cpu(3)

    rodada  = 1
    msg     = "Sua vez — clique no tabuleiro inimigo para atirar."
    cor_msg = BRANCO

    while avioes_jogador and avioes_cpu:

        # Turno do jogador
        aguardando_clique = True
        while aguardando_clique:
            mx, my   = pygame.mouse.get_pos()
            destaque = pixel_para_celula(GRID_E_X, GRID_Y, mx, my)
            redesenhar = montar_cena(surf, imagem_aviao, avioes_jogador, avioes_cpu,
                                     rodada, msg, cor_msg, destaque, hack)
            redesenhar()
            pygame.display.flip()
            clock.tick(FPS)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and destaque:
                    lin, col = destaque
                    acerto   = verificar_acerto(avioes_cpu, lin, col)
                    if acerto >= 0:
                        nome    = avioes_cpu.pop(acerto)["nome"]
                        anim_explosao(surf, clock, GRID_E_X, GRID_Y, lin, col, redesenhar, som_explosao)
                        msg     = f"Voce abateu o {nome} inimigo!"
                        cor_msg = EXPLOSAO
                    else:
                        anim_agua(surf, clock, GRID_E_X, GRID_Y, lin, col, redesenhar, som_splash)
                        msg     = "Tiro no vazio — o inimigo se moveu!"
                        cor_msg = AGUA
                    aguardando_clique = False

        if not avioes_cpu:
            break

        # Turno da CPU
        pygame.time.wait(600)
        lin_cpu = random.randint(0, 9)
        col_cpu = random.randint(0, 9)

        redesenhar_cpu = montar_cena(surf, imagem_aviao, avioes_jogador, avioes_cpu,
                                     rodada, f"CPU atacou linha {lin_cpu+1}, coluna {LETRAS_COLUNAS[col_cpu]}...", LARANJA, hack=hack)
        redesenhar_cpu()
        pygame.display.flip()
        pygame.time.wait(700)

        acerto_cpu = verificar_acerto(avioes_jogador, lin_cpu, col_cpu)
        if acerto_cpu >= 0:
            nome    = avioes_jogador.pop(acerto_cpu)["nome"]
            anim_explosao(surf, clock, GRID_P_X, GRID_Y, lin_cpu, col_cpu, redesenhar_cpu, som_explosao)
            msg     = f"CPU abateu seu {nome}!"
            cor_msg = VERMELHO
        else:
            anim_agua(surf, clock, GRID_P_X, GRID_Y, lin_cpu, col_cpu, redesenhar_cpu, som_splash)
            msg     = f"CPU errou em {lin_cpu+1}{LETRAS_COLUNAS[col_cpu]}."
            cor_msg = AGUA

        if not avioes_jogador:
            break

        # Aviões se movem
        pygame.time.wait(300)
        mover_avioes(avioes_cpu)
        mover_avioes(avioes_jogador)

        rodada += 1
        msg     = "Sua vez — clique no tabuleiro inimigo para atirar."
        cor_msg = BRANCO

    if not avioes_cpu and avioes_jogador:
        tela_fim(surf, clock, imagem_aviao, "Voce venceu a Batalha Aerea!", VERDE)
    elif not avioes_jogador and avioes_cpu:
        tela_fim(surf, clock, imagem_aviao, "A CPU venceu a Batalha Aerea...", VERMELHO)
    else:
        tela_fim(surf, clock, imagem_aviao, "Empate!", AMARELO)


if __name__ == "__main__":
    pygame.init()
    modo4()
    pygame.quit()