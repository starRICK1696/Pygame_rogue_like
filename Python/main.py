import pygame
from pygame import Rect
import os
import sys
from ImageUtils import load_image
from Animation import *
import Animation
import random
from Level_gen import *
import Level_gen
FPS = 100
def level(level, spawns, screen):
    level, level_map = level
    def generate_pistol(x, y):
        nonlocal Enemy_sprites_pistol
        enemy = Enemy(7, 1, x, y, 7, 170, 140, 70,
                    load_image("Sprites\Enemies\Хотьба_Вправо.png"),
                    load_image("Sprites\Enemies\Хотьба_Влево.png"),
                    load_image("Sprites\Enemies\Вправо_стрельба.png"),
                    load_image("Sprites\Enemies\Влево_стрельба.png"))
        Enemy_sprites_pistol.add(enemy)

    def generate_shotgun(x, y):
        nonlocal Enemy_sprites_shotgun
        enemy = Enemy(5, 2, x, y, 15, 170, 140, 100,
                    load_image("Sprites\Enemies\Ведро_идет_вправо.png"),
                    load_image("Sprites\Enemies\Ведро_идет_влево.png"),
                    load_image("Sprites\Enemies\Ведро_вправо_стрельба.png"),
                    load_image("Sprites\Enemies\Ведро_влево_стрельба.png"))
        Enemy_sprites_shotgun.add(enemy)
    
    def Button(m_x, m_y, left_top, side):
        return (
            m_x > left_top[0] and
            m_x < (left_top[0] + side) and
            m_y > left_top[1] and
            m_y < (left_top[1] + side))

    def Pause(mouse_x, mouse_y):
        running = True
        nonlocal mov_x, mov_y
        fon = load_image('Pause.png')
        mouse = load_image('Курсор.png')
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos[0], event.pos[1]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if Button(mouse_x, mouse_y, (630, 380), 200):
                            return 'end'
                        elif Button(mouse_x, mouse_y, (850, 380), 200):
                            return True
                        elif Button(mouse_x, mouse_y, (1070, 380), 200):
                            return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        mov_y -= 1
                    if event.key == pygame.K_s:
                        mov_y += 1
                    if event.key == pygame.K_a: 
                        mov_x -= 1
                    if event.key == pygame.K_d:
                        mov_x += 1
                    if event.key == pygame.K_ESCAPE:
                        running = Pause(mouse_x, mouse_y)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        mov_y += 1
                    if event.key == pygame.K_s:
                        mov_y -= 1
                    if event.key == pygame.K_a:
                        mov_x += 1
                    if event.key == pygame.K_d:
                            mov_x -= 1
            screen.blit(fon, (150, 100))
            screen.blit(mouse, (mouse_x, mouse_y))
            pygame.display.flip()
            

    pygame.display.set_caption('EtD')
    pygame.mouse.set_visible(False)
    cursor = load_image("Прицел.png")
    death = load_image('Death.png')
    winner = load_image('Winning.png')
    pygame.display.flip()
    running = True
    mouse_x, mouse_y = 0, 0
    mov_x, mov_y = 0, 0
    moving_x, moving_y = 0, 0
    clock = pygame.time.Clock()
    player = Player(8, 1, 920, 490, 3, 
                            load_image("Sprites\MainCharacter\Стоит.png"),
                            load_image("Sprites\MainCharacter\Вверх.png"),
                            load_image("Sprites\MainCharacter\Вниз.png"),
                            load_image("Sprites\MainCharacter\Вправо.png"),
                            load_image("Sprites\MainCharacter\Влево.png"),
                            )
    char_sprite = pygame.sprite.Group()
    char_sprite.add(player)
    HP_bar = load_image("HP_bar.png")
    print('\n'.join(level_map))
    count = 0
    M_x, M_y = 0, 0
    pygame.display.flip()
    P_x, P_y = 920, 490
    Enemy_sprites_pistol = pygame.sprite.Group()
    Enemy_sprites_shotgun = pygame.sprite.Group()
    Player_Bullet_Group = pygame.sprite.Group()
    Enemy_Bullet_Group = pygame.sprite.Group()
    ShortAnimations = pygame.sprite.Group()
    while running:
        mov_x, mov_y = max(-1, min(1, mov_x)), max(-1, min(1, mov_y))
        if player.HP <= 0:
            screen.blit(death, (150, 100))
            pygame.display.flip()
            clock.tick(0.3)
            return False
        elif not (bool(spawns) or bool(Enemy_sprites_shotgun) or bool(Enemy_sprites_pistol)):
            screen.blit(winner, (150, 100))
            pygame.display.flip()
            clock.tick(0.3)
            return True
        clock.tick(FPS)
        player.freeze -= 1
        screen.fill((21, 28, 31))
        count += 1
        if count == 10:
            count = 0
            player.update()
            for i in Player_Bullet_Group:
                i.update()
            for i in Enemy_sprites_pistol:
                i.update()
            for i in Enemy_sprites_shotgun:
                i.update()
            for i in ShortAnimations:
                i.update()
        if level_map[(int(P_y) + 74) // 180][(int(P_x) + 39) // 180] in spawns:
            for i in spawns[level_map[(int(P_y) + 74) // 180][(int(P_x) + 39) // 180]]:
                print(1)
                if i[0] == 'p':
                    generate_pistol(i[1][0] + M_x, i[1][1] + M_y)
                else:
                    generate_shotgun(i[1][0] + M_x, i[1][1] + M_y)
            del spawns[level_map[(int(P_y) + 74) // 180][(int(P_x) + 39) // 180]]
        if (
            level_map[(int(P_y) + 66) // 180][(int(P_x) + 3) // 180] not in (['.'] + list(map(str, range(10)))) or
            level_map[(int(P_y) + 83) // 180][(int(P_x) + 76) // 180] not in (['.'] + list(map(str, range(10)))) or
            level_map[(int(P_y) + 83) // 180][(int(P_x) + 3) // 180] not in (['.'] + list(map(str, range(10)))) or
            level_map[(int(P_y) + 66) // 180][(int(P_x) + 76) // 180] not in (['.'] + list(map(str, range(10))))
            ):
            M_x, M_y, P_x, P_y = Last
        else:
            for i in Player_Bullet_Group:
                i.rect.x -= moving_x
                i.rect.y -= moving_y
            for i in Enemy_sprites_pistol:
                i.rect.x -= moving_x
                i.rect.y -= moving_y
            for i in Enemy_sprites_shotgun:
                i.rect.x -= moving_x
                i.rect.y -= moving_y
            for i in Enemy_Bullet_Group:
                i.rect.x -= moving_x
                i.rect.y -= moving_y
            for i in ShortAnimations:
                i.rect.x -= moving_x
                i.rect.y -= moving_y
        screen.blit(level, (M_x, M_y))   
        Player_Bullet_Group.draw(screen)
        Enemy_sprites_pistol.draw(screen)
        Enemy_sprites_shotgun.draw(screen)
        Enemy_Bullet_Group.draw(screen)
        char_sprite.draw(screen)
        ShortAnimations.draw(screen)
        screen.blit(HP_bar, (200, 120))
        screen.fill((130, 0, 0), Rect(320, 145, int(225 * (player.HP / player.max_hp)), 65))
        screen.blit(cursor, (mouse_x - 17, mouse_y - 17))
        pygame.display.flip()
        #pistol zombie
        for i in Enemy_sprites_pistol:
            k = pygame.sprite.spritecollide(i, Player_Bullet_Group, True)
            i.HP -= player.damage * len(k)
            if k:
                blood = Short_Animation(5, 3, i.rect.x, i.rect.y + 60, load_image('Effects/blood.png'))
                ShortAnimations = Animation.SA
            if i.HP <= 0:
                i.kill()

            if i.rest_time_to_move >= 0:
                if i.rest_time_to_move == i.time_to_move:
                    i.rest_attack_time = i.attack_time
                    i.rest_time_to_move -= 1
                    point_to_go = list(map(lambda x: (x * 180), i.choose_way(level_map, ((int(P_x) + 40) // 180), ((int(P_y) + 78) // 180), M_x, M_y)))
                    i.vector_of_moving = [(i.rect.y + 80 - M_y - point_to_go[0]) // i.speed, (i.rect.x + 40 - M_x - point_to_go[1]) // i.speed]
                    if i.vector_of_moving[1] > 0:
                        i.animation_num = 1
                    else:
                        i.animation_num = 0
                else:
                    i.rest_time_to_move -= 1
                    i.rect.x -= i.vector_of_moving[1]
                    i.rect.y -= i.vector_of_moving[0]
                
            else:
                if i.rest_attack_time <= 0:
                    i.rest_time_to_move = i.time_to_move
                elif i.rest_attack_time == i.attack_time:
                    if i.rect.x + 60 > 960:
                        i.animation_num = 3
                    else:
                        i.animation_num = 2
                    i.cur_frame = 0
                    i.rest_attack_time -= 1
                else:
                    if i.rest_attack_time == 65:
                        bullet_speed = ((((i.rect.x + 40 - 920) ** 2) + ((i.rect.y + 80 - 500) ** 2)) ** 0.5) // 6
                        if i.animation_num == 3:
                            bullet = Enemy_Bullet(1, 1, i.rect.x, i.rect.y + 30, 3,
                                                   (i.rect.x - 920) // bullet_speed,
                                                   (i.rect.y - 500) // bullet_speed,
                                                   load_image("Sprites\Enemies\Bullet.png"))
                        else:
                            bullet = Enemy_Bullet(1, 1, i.rect.x + 50, i.rect.y + 40, 3,
                                                   (i.rect.x - 920) // bullet_speed,
                                                   (i.rect.y - 500) // bullet_speed,
                                                   load_image("Sprites\Enemies\Bullet.png"))
                        Enemy_Bullet_Group = Animation.EBG
                    i.rest_attack_time -= 1

        #shotgun zombie
        for i in Enemy_sprites_shotgun:
            k = pygame.sprite.spritecollide(i, Player_Bullet_Group, True)
            i.HP -= player.damage * len(k)
            if k:
                blood = Short_Animation(5, 3, i.rect.x, i.rect.y + 60, load_image('Effects/blood.png'))
                ShortAnimations = Animation.SA
            if i.HP <= 0:
                i.kill()

            if i.rest_time_to_move >= 0:
                if i.rest_time_to_move == i.time_to_move:
                    i.rest_attack_time = i.attack_time
                    i.rest_time_to_move -= 1
                    point_to_go = list(map(lambda x: (x * 180), i.choose_way(level_map, ((int(P_x) + 40) // 180), ((int(P_y) + 78) // 180), M_x, M_y)))
                    i.vector_of_moving = [(i.rect.y + 80 - M_y - point_to_go[0]) // i.speed, (i.rect.x + 40 - M_x - point_to_go[1]) // i.speed]
                    if i.vector_of_moving[1] > 0:
                        i.animation_num = 1
                    else:
                        i.animation_num = 0
                else:
                    i.rest_time_to_move -= 1
                    i.rect.x -= i.vector_of_moving[1]
                    i.rect.y -= i.vector_of_moving[0]
                
            else:
                if i.rest_attack_time <= 0:
                    i.rest_time_to_move = i.time_to_move
                elif i.rest_attack_time == i.attack_time:
                    if i.rect.x + 60 > 960:
                        i.animation_num = 3
                    else:
                        i.animation_num = 2
                    i.cur_frame = 0
                    i.rest_attack_time -= 1
                else:
                    if i.rest_attack_time == 85:
                        bullet_speed = ((((i.rect.x + 40 - 920) ** 2) + ((i.rect.y + 80 - 500) ** 2)) ** 0.5) // 6
                        if i.animation_num == 3:
                            for j in range(5):
                                bullet = Enemy_Bullet(1, 1, i.rect.x, i.rect.y + 30, 1,
                                                   (i.rect.x - 920 + int((random.random() - 0.5) * 300)) // bullet_speed,
                                                   (i.rect.y - 450 + int((random.random() - 0.5) * 300)) // bullet_speed,
                                                   load_image("Sprites\Enemies\Bullet.png"))
                        else:
                            for j in range(5):
                                bullet = Enemy_Bullet(1, 1, i.rect.x + 50, i.rect.y + 40, 1,
                                                   (i.rect.x - 920 + int((random.random() - 0.5) * 300)) // bullet_speed,
                                                   (i.rect.y - 450 + int((random.random() - 0.5) * 300)) // bullet_speed,
                                                   load_image("Sprites\Enemies\Bullet.png"))
                        Enemy_Bullet_Group = Animation.EBG
                    i.rest_attack_time -= 1
         

        k = pygame.sprite.spritecollide(player, Enemy_Bullet_Group, True)
        for i in k:
            player.HP -= i.damage
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos[0], event.pos[1]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    mov_y -= 1
                if event.key == pygame.K_s:
                    mov_y += 1
                if event.key == pygame.K_a: 
                    mov_x -= 1
                if event.key == pygame.K_d:
                    mov_x += 1
                if event.key == pygame.K_ESCAPE:
                    k = Pause(mouse_x, mouse_y)
                    if k == 'end':
                        return False
                    else:
                        running = k
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    mov_y += 1
                if event.key == pygame.K_s:
                    mov_y -= 1
                if event.key == pygame.K_a:
                    mov_x += 1
                if event.key == pygame.K_d:
                        mov_x -= 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player.freeze <= 0:
                        bullet_speed = ((((event.pos[0] - 960) ** 2) + ((event.pos[1] - 540) ** 2)) ** 0.5) // 6
                        bullet = Player_Bullet(2, 2, 960, 510, 10,
                                               (960 - event.pos[0]) // bullet_speed,
                                               (510 - event.pos[1]) // bullet_speed,
                                               load_image("Sprites\Fireball\Fireball.png"))
                        Player_Bullet_Group = Animation.PBG
                        player.freeze = 25
                if event.button == 3:
                    generate_shotgun(event.pos[0], event.pos[1])
        if mov_x == 0 and mov_y == 0:
            player.animation_num = 0
        elif mov_x > 0:
            player.animation_num = 3
        elif mov_x < 0:
            player.animation_num = 4
        elif mov_y < 0:
            player.animation_num = 1
        else:
            player.animation_num = 2
        Last = [M_x, M_y, P_x, P_y]
        moving_x = mov_x * player.speed
        moving_y = mov_y * player.speed
        M_x -= moving_x
        M_y -= moving_y
        P_x += moving_x
        P_y += moving_y
        for i in Player_Bullet_Group:
            if level_map[(i.rect.y - M_y + 40) // 180][(i.rect.x - M_x + 20) // 180] not in (['.'] + list(map(str, range(10)))):
                i.kill()
            i.rect.x -= i.speed_x
            i.rect.y -= i.speed_y
        for i in Enemy_Bullet_Group:
            if level_map[(i.rect.y - M_y) // 180][(i.rect.x - M_x) // 180] not in (['.'] + list(map(str, range(10)))):
                i.kill()
            i.rect.x -= i.speed_x
            i.rect.y -= i.speed_y
    screen.blit(death, (150, 100))
    pygame.quit()
