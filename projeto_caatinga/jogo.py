import pygame
import sys
import random
import math

pygame.init()

# Tela
LARGURA, ALTURA = 560, 640
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Cobra da Caatinga")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (200, 50, 30)
AMARELO = (255, 220, 50)
TERRA_ESC = (100, 60, 20)

# Configurações
CELULA = 40
VELOCIDADE = 4  # pixels por frame (deve dividir CELULA exatamente: 1,2,4,5,8,10,20,40)

# Mapa (1 = parede, 0 = vazio, 2 = sapinho)
MAPA = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,1,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,1,2,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,2,1,2,1,1,2,2,1],
    [1,2,2,2,2,1,2,1,2,2,2,2,2,1],
    [1,1,1,1,2,1,0,1,2,1,1,1,1,1],
    [1,1,1,1,2,1,0,1,2,1,1,1,1,1],
    [1,1,1,1,2,0,0,0,2,1,1,1,1,1],
    [0,0,0,0,2,0,0,0,2,0,0,0,0,0],
    [1,1,1,1,2,0,0,0,2,1,1,1,1,1],
    [1,1,1,1,2,1,0,1,2,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,1,2,2,1],
    [1,2,2,1,2,2,2,2,2,1,2,2,2,1],
]

LINHAS = len(MAPA)
COLUNAS = len(MAPA[0])

# Carregar imagens
cenario = pygame.image.load("imagens/cenario.png")
cenario = pygame.transform.scale(cenario, (LARGURA, ALTURA))

# Cobra
TAMANHO_COBRA = 60
cobra_aberta = pygame.image.load("imagens/cobra_aberta.png")
cobra_aberta = pygame.transform.scale(cobra_aberta, (TAMANHO_COBRA, TAMANHO_COBRA))

cobra_fechada = pygame.image.load("imagens/cobra_fechada.png")
cobra_fechada = pygame.transform.scale(cobra_fechada, (TAMANHO_COBRA, TAMANHO_COBRA))

# Gavião
TAMANHO_GAVIAO = 60
gaviao_img = pygame.image.load("imagens/gaviao.png")
gaviao_img = pygame.transform.scale(gaviao_img, (TAMANHO_GAVIAO, TAMANHO_GAVIAO))

# Sapo
TAMANHO_SAPO = 60
sapo_img = pygame.image.load("imagens/sapo.png")
sapo_img = pygame.transform.scale(sapo_img, (TAMANHO_SAPO, TAMANHO_SAPO))


def celula_valida(col, lin):
    if 0 <= lin < LINHAS and 0 <= col < COLUNAS:
        return MAPA[lin][col] != 1
    return False


class Cobra:
    def __init__(self):
        self.col = 6
        self.lin = 13
        self.x = float(self.col * CELULA + CELULA // 2)
        self.y = float(self.lin * CELULA + CELULA // 2)

        self.dx = 0
        self.dy = 0
        self.prox_dx = 0
        self.prox_dy = 0

        self.animacao = 0

    def definir_direcao(self, dx, dy):
        self.prox_dx = dx
        self.prox_dy = dy

    def _alinhada(self):
        cx = round(self.x - CELULA // 2)
        cy = round(self.y - CELULA // 2)
        return (cx % CELULA == 0) and (cy % CELULA == 0)

    def atualizar(self):
        if self._alinhada():
            col_atual = int(self.x) // CELULA
            lin_atual = int(self.y) // CELULA

            if self.prox_dx != 0 or self.prox_dy != 0:
                prox_col = col_atual + self.prox_dx
                prox_lin = lin_atual + self.prox_dy
                if celula_valida(prox_col, prox_lin):
                    self.dx = self.prox_dx
                    self.dy = self.prox_dy
                    self.prox_dx = 0
                    self.prox_dy = 0

            prox_col = col_atual + self.dx
            prox_lin = lin_atual + self.dy
            if not celula_valida(prox_col, prox_lin):
                self.x = float(col_atual * CELULA + CELULA // 2)
                self.y = float(lin_atual * CELULA + CELULA // 2)
                self.dx = 0
                self.dy = 0
                self.animacao += 1
                return

        self.x += self.dx * VELOCIDADE
        self.y += self.dy * VELOCIDADE
        self.animacao += 1

    def coletar(self, mapa):
        col = int(self.x) // CELULA
        lin = int(self.y) // CELULA
        if 0 <= lin < LINHAS and 0 <= col < COLUNAS:
            if mapa[lin][col] == 2:
                mapa[lin][col] = 0
                return True
        return False

    def desenhar(self, superficie):
        img = cobra_aberta if (self.animacao // 8) % 2 == 0 else cobra_fechada
        x = int(self.x) - img.get_width() // 2
        y = int(self.y) - img.get_height() // 2
        superficie.blit(img, (x, y))


class Gaviao:
    def __init__(self, col, lin):
        self.x = col * CELULA + CELULA // 2
        self.y = lin * CELULA + CELULA // 2
        self.dx = random.choice([-1, 1])
        self.dy = 0
        self.timer = random.randint(0, 30)

    def atualizar(self):
        self.timer += 1

        if self.timer >= 30:
            self.timer = 0
            direcoes = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(direcoes)
            for dx, dy in direcoes:
                novo_x = self.x + dx * 4
                novo_y = self.y + dy * 4
                col = int(novo_x) // CELULA
                lin = int(novo_y) // CELULA
                if celula_valida(col, lin):
                    self.dx, self.dy = dx, dy
                    break

        novo_x = self.x + self.dx * 2
        novo_y = self.y + self.dy * 2
        col = int(novo_x) // CELULA
        lin = int(novo_y) // CELULA
        if celula_valida(col, lin):
            self.x = novo_x
            self.y = novo_y

    def colide(self, cobra):
        distancia = math.hypot(self.x - cobra.x, self.y - cobra.y)
        return distancia < 30

    def desenhar(self, superficie):
        x = self.x - gaviao_img.get_width() // 2
        y = self.y - gaviao_img.get_height() // 2
        superficie.blit(gaviao_img, (x, y))


def desenhar_tudo(superficie, mapa, cobra, gavioes, pontuacao, vidas, game_over, vitoria):
    # 1. Limpa o buffer completamente antes de tudo — isso elimina o fantasma
    superficie.fill(PRETO)

    # 2. Cenário
    superficie.blit(cenario, (0, 0))

    # 3. Sapinhos
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if mapa[lin][col] == 2:
                x = col * CELULA + (CELULA - TAMANHO_SAPO) // 2
                y = lin * CELULA + (CELULA - TAMANHO_SAPO) // 2
                superficie.blit(sapo_img, (x, y))

    # 4. Gaviões
    for g in gavioes:
        g.desenhar(superficie)

    # 5. Cobra
    cobra.desenhar(superficie)

    # 6. Barra inferior
    pygame.draw.rect(superficie, TERRA_ESC, (0, ALTURA - 42, LARGURA, 42))
    fonte = pygame.font.SysFont("Arial", 22, bold=True)
    txt_p = fonte.render(f"Sapinhos: {pontuacao}", True, AMARELO)
    txt_v = fonte.render(f"Vidas: {vidas}", True, AMARELO)
    superficie.blit(txt_p, (10, ALTURA - 32))
    superficie.blit(txt_v, (400, ALTURA - 32))

    # 7. Game over / vitória
    if game_over or vitoria:
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        superficie.blit(overlay, (0, 0))
        fonte_g = pygame.font.SysFont("Arial", 44, bold=True)
        if game_over:
            txt = fonte_g.render("A cobra foi pega!", True, VERMELHO)
        else:
            txt = fonte_g.render("Cobra sobreviveu!", True, AMARELO)
        superficie.blit(txt, (LARGURA // 2 - txt.get_width() // 2, ALTURA // 2 - 50))
        txt2 = fonte.render("Pressione R para recomeçar", True, BRANCO)
        superficie.blit(txt2, (LARGURA // 2 - txt2.get_width() // 2, ALTURA // 2 + 10))


def resetar(cobra, gavioes):
    cobra.col = 6
    cobra.lin = 13
    cobra.x = float(6 * CELULA + CELULA // 2)
    cobra.y = float(13 * CELULA + CELULA // 2)
    cobra.dx = 0
    cobra.dy = 0
    cobra.prox_dx = 0
    cobra.prox_dy = 0
    cobra.animacao = 0

    posicoes = [(5, 9), (6, 9), (7, 9), (8, 9)]
    for i, (col, lin) in enumerate(posicoes):
        gavioes[i].x = col * CELULA + CELULA // 2
        gavioes[i].y = lin * CELULA + CELULA // 2
        gavioes[i].dx = 1
        gavioes[i].dy = 0
        gavioes[i].timer = random.randint(0, 30)


def main():
    clock = pygame.time.Clock()

    mapa = [linha[:] for linha in MAPA]
    cobra = Cobra()
    gavioes = [Gaviao(5, 9), Gaviao(6, 9), Gaviao(7, 9), Gaviao(8, 9)]

    pontuacao = 0
    vidas = 3
    game_over = False
    vitoria = False
    invencivel = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if not game_over and not vitoria:
                    if evento.key == pygame.K_RIGHT:
                        cobra.definir_direcao(1, 0)
                    elif evento.key == pygame.K_LEFT:
                        cobra.definir_direcao(-1, 0)
                    elif evento.key == pygame.K_UP:
                        cobra.definir_direcao(0, -1)
                    elif evento.key == pygame.K_DOWN:
                        cobra.definir_direcao(0, 1)

                if (game_over or vitoria) and evento.key == pygame.K_r:
                    main()
                    return

        if not game_over and not vitoria:
            cobra.atualizar()
            for g in gavioes:
                g.atualizar()

            if cobra.coletar(mapa):
                pontuacao += 10

            total_sapos = sum(linha.count(2) for linha in mapa)
            if total_sapos == 0:
                vitoria = True

            if invencivel > 0:
                invencivel -= 1
            else:
                for g in gavioes:
                    if g.colide(cobra):
                        vidas -= 1
                        invencivel = 90
                        resetar(cobra, gavioes)
                        if vidas <= 0:
                            game_over = True
                        break

        desenhar_tudo(tela, mapa, cobra, gavioes, pontuacao, vidas, game_over, vitoria)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
