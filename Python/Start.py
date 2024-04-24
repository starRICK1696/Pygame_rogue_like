import pygame
from ImageUtils import load_image
import main
import Level_gen
from Level_gen import *
from ImageUtils import load_image
from Animation import *
import Animation
from main import *


def Button(m_x, m_y, left_top, side):
    return (
        m_x > left_top[0] and
        m_x < (left_top[0] + side) and
        m_y > left_top[1] and
        m_y < (left_top[1] + side))

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
pygame.display.set_caption('EtD')
pygame.mouse.set_visible(False)
running = True
fon = load_image('Meny.png')
mouse = load_image('Курсор.png')
mouse_x, mouse_y = 0, 0
while running:
    screen.blit(fon, (150, 100))
    screen.blit(mouse, (mouse_x, mouse_y))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos[0], event.pos[1]
        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if Button(mouse_x, mouse_y, (1162, 725), 250):
                        if level(generate_level(load_level('Levels\Level1.txt')), {'0': [['p', (500, 500)]], '1': [['p', (500, 800)]]}, screen):
                            if level(generate_level(load_level('Levels\Level2.txt')), {'0': [['p', (900, 800)], ['s', (1000, 1000)]], '1': [['s', (2500, 750)], ['s', (2500, 800)]]}, screen):
                                if level(generate_level(load_level('Levels\Level3.txt')),
                                         {'0': [['p', (900, 806)], ['s', (1000, 1060)], ['p', (900, 840)], ['s', (1000, 1015)]],
                                          '1': [['s', (2500, 750)], ['s', (2500, 800)], ['s', (2500, 750)], ['s', (2500, 800)]],
                                          '2': [['s', (2500, 715)], ['s', (2500, 810)], ['s', (2500, 740)], ['s', (2500, 811)], ['s', (2500, 753)], ['s', (2500, 804)]]}, screen):
                                    molodec = True
