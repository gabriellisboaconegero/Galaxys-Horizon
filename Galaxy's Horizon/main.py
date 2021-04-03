import os, sys
dirpath = os.getcwd()
sys.path.append(dirpath)
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
####

import pygame
import math
import random


pygame.init()
tela = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# cores
branco = (255, 255, 255)
preto = (0, 0, 0)
verde = (0, 255, 0)
vermelho = (255, 0, 0)
amarelo = (255, 255, 0)
azul = (0, 0, 255)

# loads

bullet_sound = pygame.mixer.Sound('data/tiro.wav')
bullet_sound.set_volume(0.4)
explosion_sound = pygame.mixer.Sound('data/explosion.wav')
explosion_sound.set_volume(0.4)
dano_sound = pygame.mixer.Sound('data/dano.wav')
plus_nivel_sound = pygame.mixer.Sound('data/+nivel.wav')
power_sound = pygame.mixer.Sound('data/poder.wav')
game_over_sound = pygame.mixer.Sound('data/game_over.wav')
moving_sound = pygame.mixer.Sound('data/moving.wav')
moving_sound.set_volume(0.3)
back_sound = pygame.mixer.music.load('data/back_music.wav')

instructions_img = pygame.image.load('data/instructions.png')

back = pygame.image.load('data/background.png')

explosion_img = pygame.image.load('data/explosão.png')
explosion_img.set_colorkey((255, 255, 255))

img1 = pygame.image.load('data/seta.png').convert()
img1.set_colorkey(branco)

ennimie_img = pygame.image.load('data/player.png')

bala_img = pygame.image.load('data/bala.png')

img_vida = pygame.image.load('data/vida.png')

more_life = pygame.image.load('data/+vida.png')
more_speed = pygame.image.load('data/+speed.png')

full_m = pygame.image.load('data/nivel_main_full.png')
full_m = pygame.transform.scale(full_m, (37, 43))

empt_m = pygame.image.load('data/nivel_main_empt.png')
empt_m = pygame.transform.scale(empt_m, (37, 43))

ye_m = pygame.image.load('data/nivel_main_ye.png')
ye_m = pygame.transform.scale(ye_m, (37, 43))

full_s = pygame.image.load('data/nivel_sec_full.png')
full_s = pygame.transform.scale(full_s, (34, 22))

empt_s = pygame.image.load('data/nivel_sec_empt.png')
empt_s = pygame.transform.scale(empt_s, (34, 22))

ye_s = pygame.image.load('data/nivel_sec_ye.png')
ye_s = pygame.transform.scale(ye_s, (34, 22))

# classes
class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = img1
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.rot = 0
        self.speed = 5

    def update(self, *args):
        mx, my = pygame.mouse.get_pos()
        if not self.rect.contains(pygame.Rect(mx, my, 1, 1)):
            self.rot = -math.atan2((my - self.rect.centery), (mx - self.rect.centerx))
            self.image = pygame.transform.rotate(img1, math.degrees(self.rot))
            x = self.rect.centerx
            y = self.rect.centery
            if move_state:
                movex = math.cos(self.rot)
                movey = math.sin(self.rot)
                self.rect.centerx += movex * self.speed
                self.rect.centery -= movey * self.speed
            else:
                self.rect = self.image.get_rect()
                self.rect.centerx = x
                self.rect.centery = y


class Bala(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.rot = seta1.rot
        self.image = pygame.transform.scale(bala_img, (8, 8))
        self.image = pygame.transform.rotate(self.image, math.degrees(self.rot))
        self.rect = self.image.get_rect()

    def update(self, *args):
        movex = math.cos(self.rot)
        movey = math.sin(self.rot)
        self.rect.centerx += movex * 12
        self.rect.centery -= movey * 12
        if not pygame.Rect(0, 0, 800, 600).contains(self.rect):
            self.kill()


class Ennimies(pygame.sprite.Sprite):
    def __init__(self, *groups):
        dentro = True
        while dentro:
            dentro = False
            x = random.randrange(-200, 1000, 100)
            y = random.randrange(-200, 800, 100)
            if 0 <= x <= 800 and 0 <= y <= 600:
                dentro = True
        super().__init__(*groups)
        self.verificar_entrada = True
        self.verificar_saida = False
        self.dentro = False
        self.speed = math.trunc(random.uniform(0.15, 0.2) * 100) / 10
        self.escala = random.randint(40, 100)
        self.image = ennimie_img
        self.img_escalada = pygame.transform.scale(ennimie_img, (self.escala, self.escala - 20))
        self.rect = self.img_escalada.get_rect()
        self.rect.center = (x, y)

    def update(self, *args):
        if self.verificar_entrada:
            if pygame.Rect(0, 0, 800, 600).contains(self.rect):
                self.dentro = True
                self.verificar_entrada = False
                self.verificar_saida = True
        if self.verificar_saida:
            if not pygame.Rect(0, 0, 800, 600).contains(self.rect):
                self.kill()
        self.rot = -math.atan2(seta1.rect.centery - self.rect.centery, seta1.rect.centerx - self.rect.centerx)
        self.image = pygame.transform.rotate(self.img_escalada, math.floor(math.degrees(self.rot)))
        movex = (math.cos(self.rot) * self.speed)
        movey = (math.sin(self.rot) * self.speed)
        self.rect.centerx += movex
        self.rect.centery -= movey


class Poderes(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = random.choice([more_life, more_speed])
        if self.image == more_speed:
            self.poder = 'speed'
        else:
            self.poder = 'vida'
        self.image = pygame.transform.scale(self.image, (52, 31))
        self.rect = self.image.get_rect()

    def update(self, *args):
        pass


class Explosion(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(explosion_img, (explo_scale, explo_scale))
        self.rect = self.image.get_rect()
        self.rect.center = index
        self.timer = 0

    def update(self, *args):
        self.timer += 1
        if self.timer == 30:
            self.kill()


# funções
def palette_swap(surf, old, new):
    copy = pygame.Surface(img1.get_size())
    copy.fill(new)
    surf.set_colorkey(old)
    copy.blit(surf, (0, 0))
    return copy


def new_skin(when_change, n_cores):
    global img1
    if score == when_change:
        for c in n_cores:
            img1 = palette_swap(img1, c[0], c[1])
        img1.set_colorkey(branco)


def draw_nivel():
    x = 742
    y = 86
    for c in range(nivel):
        tela.blit(full_m, (x, y))
        y += 15


def shoot_bar():
    pygame.draw.circle(tela, (255, 255, 0), (750, 50), int(timer_tiro * scale_shoot))
    pygame.draw.circle(tela, (0, 0, 0), (750, 50), 3)
    pygame.draw.circle(tela, (0, 0, 0), (750, 50), 33, 3)


def quant_vidas(x1):
    barra = []
    for c in range(x1):
        vida = img_vida
        vida = pygame.transform.scale(vida, (32, 32))
        barra.append(vida)
    return barra


def vida(surf, list, x, y=300):
    for vida in list:
        surf.blit(vida, (x, y))
        x += 42
    x = x


def vida_bar(surf, list):
    global vidas
    x = seta1.rect.centerx - (len(vidas) * 32 + (len(vidas) - 1) * 10) / 2
    y = seta1.rect.centery + 32
    vida(surf, list, x, y)


def xp_plus(list):
    if exp > 1:
        if exp % 1 == 0:
            list[int(math.ceil(exp)) - 1] = full_s
        else:
            list[int(math.ceil(exp)) - 1] = ye_s
    else:
        if exp % 1 == 0:
            list[int(math.ceil(exp)) - 1] = full_m
        else:
            list[int(math.ceil(exp)) - 1] = ye_m


def restar_nivel(n_nivel):
    exp = 0
    nivel = []
    nivel.append(empt_m)
    for n in range(n_nivel * 2):
        nivel.append(empt_s)
    return nivel, exp


def niveis(list, x):
    tela.blit(list[0], (x, 550))
    x += 40
    for n, c in enumerate(list):
        if n != 0:
            tela.blit(c, (x, 561))
            x += 34
    x = x


def nivel_plus(list):
    global nivel
    if list[-1] == full_s:
        nivel += 1
        restar_nivel(nivel)


def pause_game():
    global pause
    if pause:
        fonte = pygame.font.Font('data/letras.ttf', 40)
        txt = txt = fonte.render('PAUSE', False, azul)
        txt.set_alpha(150)
        rect = txt.get_rect()
        txt.set_colorkey(branco)
        tela.blit(txt, (400 - int(rect.w / 2), 50 - int(rect.h / 2)))
        pygame.display.update()
    if end:
        fonte = pygame.font.Font('data/letras.ttf', 30)
        txt_vict = fonte.render(f'PARABENS VOCE VENCEU', True, vermelho)
        rect = txt_vict.get_rect()
        tela.blit(txt_vict, (400 - int(rect.w / 2), 100 - int(rect.h / 2)))
        pygame.display.update()
    while pause or end:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pause = not pause


def menuAba():
    global menu
    timer_bot = 0
    pisc = True
    while not menu:
        tela.blit(back, (0, 0))
        player.draw(tela)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                menu = not menu

        if timer_bot == 30:
            timer_bot = 0
            pisc = not pisc
        if not pisc:
            font = pygame.font.Font('data/letras.ttf', 20)
            txt1 = font.render(f'PRESS ANY BUTTON', False, preto)
            rec = txt1.get_rect()
            tela.blit(txt1, (400 - int(rec.w / 2), 560 - int(rec.h / 2)))

        font = pygame.font.Font('data/letras.ttf', 20)
        txt1 = font.render(f'MOVER NAVE', False, preto)
        tela.blit(txt1, (200, 485))
        txt1 = font.render(f'PAUSE', False, preto)
        tela.blit(txt1, (475, 360))
        font = pygame.font.Font('data/letras.ttf', 70)
        txt1 = font.render(f'GALAXY\'S HORIZON', False, preto)
        rec = txt1.get_rect()
        tela.blit(txt1, (400 - int(rec.w / 2), 150 - int(rec.h / 2)))
        rec = instructions_img.get_rect()
        tela.blit(instructions_img, (400 - int(rec.w / 2), 430 - int(rec.h / 2)))
        pygame.display.update()
        timer_bot += 1
        clock.tick(60)


# grupos
explosions = pygame.sprite.Group()
poderes = pygame.sprite.Group()
player = pygame.sprite.Group()
balas = pygame.sprite.Group()
inimigos = pygame.sprite.Group()

# player
seta1 = Player(player)
seta1.rect.center = (400, 300)
main_skin = seta1.image.copy()


# constantes
scale_shoot = 2
reload = 15
vidas = quant_vidas(5)
timer_tiro = 15
ennimie_timer = score = timer_picar = poder_state = timer_power = 0
cronometro = 60
move_state = piscando = pause = end = menu = False
nivel = 1
bar_nivel, exp = restar_nivel(1)
duração_power = 120

pygame.mixer.music.play(-1)

# jogo em si
while 1:
    pause_game()

    # fundo
    tela.blit(back, (0, 0))

    # score
    fonte = pygame.font.Font('data/letras.ttf', 400)
    txt = fonte.render(f'{score}', False, azul)
    txt.set_alpha(150)
    rect = txt.get_rect()
    txt.set_colorkey(branco)
    tela.blit(txt, (400 - int(rect.w / 2), 300 - int(rect.h / 2)))

    # draw sprites
    draw_nivel()
    explosions.draw(tela)
    poderes.draw(tela)
    inimigos.draw(tela)
    balas.draw(tela)
    if not piscando:
        player.draw(tela)
    else:
        if timer_picar % 10 == 0:
            player.draw(tela)

    # captar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if not move_state:
                    moving_sound.play(-1)
                else:
                    moving_sound.stop()
                move_state = not move_state
            if evento.key == pygame.K_p:
                pause = not pause

    #menu
    menuAba()

    # atirar
    clique = pygame.mouse.get_pressed()

    if clique[0]:
        if timer_tiro == reload:
            bullet_sound.play()
            bala = Bala(balas)
            bala.rect.center = seta1.rect.center
            timer_tiro = 0
        timer_tiro += 1

    # adicionar inimigo
    if ennimie_timer == cronometro:
        if random.random() > 0:
            inimigo = Ennimies(inimigos)
        ennimie_timer = 0

    # kill ennimie
    collision = pygame.sprite.groupcollide(balas, inimigos, True, True)
    if collision:
        explosion_sound.play()
        for c in collision.keys():
            index = collision[c][0].rect.center
            explo_scale = collision[c][0].escala
        score += 1
        explosion = Explosion(explosions)
        if score % 2 == 0:
            exp += 0.5
            xp_plus(bar_nivel)
        if score > 120:
            if random.random() > 0.95:
                poder = Poderes(poderes)
                poder.rect.center = index
        if score > 250:
            duração_power = 240

    # levar dano
    collision = pygame.sprite.groupcollide(inimigos, player, True, False)
    if not piscando:
        if collision:
            dano_sound.play()
            vidas.pop()
            piscando = True
            timer_picar = 0
    else:
        if timer_picar % 180 == 0:
            piscando = False

    # pegar poder
    collision = pygame.sprite.groupcollide(player, poderes, False, True)
    for c in collision.keys():
        poder_state = collision[c][0].poder
    if collision:
        power_sound.play()
        if poder_state == 'vida':
            vida_ = pygame.transform.scale(img_vida, (32, 32))
            vidas.append(vida_)
        else:
            timer_tiro = 0
            reload = 7
            scale_shoot = 4

    # barras de tiro, vida, nivel
    shoot_bar()
    vida_bar(tela, vidas)
    niveis(bar_nivel, 10)

    # niveis
    if bar_nivel[-1] == full_s:
        plus_nivel_sound.play()
        nivel += 1
        bar_nivel, exp = restar_nivel(nivel)
        cronometro -= 5
        ennimie_timer = 0

    #nova skin
    new_skin(100, [[(83, 143, 248), (255, 89, 0)]])
    new_skin(200, [[(255, 242, 0), (255, 16, 215)]])
    new_skin(250, [[(236, 28, 36), (255, 243, 0)]])
    new_skin(350, [[(35, 35, 35), preto], [(60, 60, 60), (12, 77, 9)], [(88, 88, 88), (8, 90, 4)], [(161, 161, 161), (20, 179, 12)]])

    # game over
    if not vidas:
        moving_sound.stop()
        game_over_sound.play()
        menu = not menu
        vidas = quant_vidas(5)
        timer_tiro = 15
        ennimie_timer = score = 0
        cronometro = 60
        move_state = piscando = False
        nivel = 1
        bar_nivel, exp = restar_nivel(1)
        seta1.rect.center = (400, 300)
        inimigos.empty()
        poderes.empty()

    # atualizar grupos
    explosions.update()
    player.update()
    balas.update()
    inimigos.update()
    pygame.display.update()

    # end game
    if nivel == 11:
        cronometro = 0
        if inimigos.sprites() == []:
            end = True
            pause_game()

    ####
    if poder_state != 0:
        timer_power += 1
        if timer_power >= duração_power:
            timer_power = 0
            reload = 15
            poder_state = 0
            scale_shoot = 2
    ennimie_timer += 1
    timer_picar += 1
    clock.tick(60)
