
import pygame
import random
from pygame.locals import *
from sys import exit

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 32, 2, 4096)

font_name = pygame.font.get_default_font()

game_font = pygame.font.SysFont(font_name, 72)

screen = pygame.display.set_mode((396, 548), 0, 32)

background_filename = 'pista.png'
background = pygame.image.load(background_filename).convert()

carro = {
    'surface': pygame.image.load('carro.png').convert_alpha(),
    'position': [(240), (348)],
    'speed': {
        'x': 0,
        'y': 0
    }
}

explosion_sound = pygame.mixer.Sound('boom.wav')
explosion_played = False
pygame.display.set_caption('Crash Escape')

clock = pygame.time.Clock()

def create_rival():
    return {
        'surface': pygame.image.load('rival.png').convert_alpha(),
        'position': [random.randrange(10, 240, 229), -100],
        'speed':(10)
    }

ticks_to_rival = 90
rivals = []


def move_rivals():
    for rival in rivals:
        rival['position'][1] += rival ['speed']


def remove_used_rivals():
    for rival in rivals:
        if rival ['position'][1] > 550:
            rivals.remove(rival)


def get_rect(obj):
    return Rect(obj['position'][0],
                obj['position'][1],
                obj['surface'].get_width(),
                obj['surface'].get_height())


def carro_collided():
    carro_rect = get_rect(carro)
    for rival in rivals:
        if carro_rect.colliderect(get_rect(rival)):
            return True
    return False

collided = False

while True:

    if not ticks_to_rival:
        ticks_to_rival = 40
        rivals.append(create_rival())
    else:
        ticks_to_rival -=1

    carro['speed'] = {
        'x': 0,
        'y': 0
    }
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_LEFT]:
        carro['position'] = [(10), (348)]
    elif pressed_keys[K_RIGHT]:
        carro['position'] = [(240), (348)]

    screen.blit(background, (0, 0))

    move_rivals()

    for rival in rivals:
        screen.blit(rival['surface'], rival ['position'])

    if not collided:
        collided = carro_collided()
        carro['position'][0] += carro['speed'] ['x']
        carro['position'][1] += carro['speed'] ['y']

        screen.blit(carro['surface'], carro['position'])
    else:
        if not explosion_played:
            explosion_played = True
            explosion_sound.play()
            carro['position'][0] += carro ['speed']['x']
            carro['position'][1] += carro ['speed']['y']

            screen.blit(carro['surface'], carro ['position'])
        else:
            text = game_font.render('GAME OVER', 1, (255, 0, 0))
            screen.blit(text, (40, 250))

    pygame.display.update()
    time_passed = clock.tick(30)

    remove_used_rivals()
