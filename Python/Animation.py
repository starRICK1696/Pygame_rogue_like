import pygame

PG = pygame.sprite.Group()
PBG = pygame.sprite.Group()
EG = pygame.sprite.Group()
EBG = pygame.sprite.Group()
SA = pygame.sprite.Group()
class Player(pygame.sprite.Sprite):
    def __init__(self, columns, rows, x, y, speed, *args):
        self.freeze = 0
        super().__init__(PG)
        self.animation_num = 0
        self.damage = 1
        self.animations = []
        self.max_hp = 15
        self.HP = 15
        self.speed = speed
        for i in args:
            self.frames = []
            self.cut_sheet(i, columns, rows)
            self.animations.append(self.frames)
        self.cur_frame = 0
        self.image = self.animations[self.animation_num][self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.animations[self.animation_num][self.cur_frame]

class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self, columns, rows, x, y, damage, speed_x, speed_y, animation):
        self.speed_x = speed_x
        self.speed_y = speed_y
        super().__init__(PBG)
        self.frames = []
        self.cut_sheet(animation, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames    [self.cur_frame]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, columns, rows, x, y, HP, speed, time_to_move, attack_time, *args):
        super().__init__(EG)
        self.time_to_move = time_to_move
        self.vector_of_moving = None
        self.rest_time_to_move = self.time_to_move
        self.attack_time = attack_time
        self.rest_attack_time = attack_time
        self.animation_num = 0
        self.animations = []
        self.HP = HP
        self.speed = speed
        for i in args:
            self.frames = []
            self.cut_sheet(i, columns, rows)
            self.animations.append(self.frames)
        self.cur_frame = 0
        self.image = self.animations[self.animation_num][self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.animations[self.animation_num][self.cur_frame]

    def choose_way(self, level, char_x, char_y, M_x, M_y):
        enemy_pos = [(int(self.rect.y) + 120 - M_y) // 180, (int(self.rect.x) + 60 - M_x) // 180]
        end = [enemy_pos]
        level = list(map(list, level))
        level[enemy_pos[0]][enemy_pos[1]] = 0
        new_end = []
        rast = 0
        while level[char_y][char_x] in (['.'] + list(map(str, range(10)))):
            rast += 1
            for i in end:
                near_pos = [[i[0] + 1, i[1]], [i[0], i[1] + 1], [i[0] - 1, i[1]], [i[0], i[1] - 1]]
                for j in near_pos:
                    if j[0] >= 0 and j[0] < len(level) and j[1] < len(level[0]) and j[1] >= 0:
                        if level[j[0]][j[1]] in (['.'] + list(map(str, range(10)))):
                            level[j[0]][j[1]] = rast
                            new_end.append(j)
            end = new_end
            new_end = list()
        way = [[char_y, char_x]]
        while way[-1] != enemy_pos:
            i = way[-1]
            number_of_last_step = level[i[0]][i[1]]
            near_pos = [[i[0] + 1, i[1]], [i[0], i[1] + 1], [i[0] - 1, i[1]], [i[0], i[1] - 1]]
            for j in near_pos:
                if j[0] >= 0 and j[0] < len(level) and j[1] < len(level[0]) and j[1] >= 0:
                    if level[j[0]][j[1]] == number_of_last_step - 1:
                        number_of_last_step -= 1
                        way.append(j)
                        break
        if len(way) > 1:
            return way[-2]
            
        else:
            return way[0]


class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self, columns, rows, x, y, damage, speed_x, speed_y, animation):
        self.speed_x = speed_x
        self.speed_y = speed_y
        super().__init__(EBG)
        self.frames = []
        self.damage = damage
        self.cut_sheet(animation, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
                
    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

class Short_Animation(pygame.sprite.Sprite):
    def __init__(self, columns, rows, x, y, animation):
        super().__init__(SA)
        self.frames = []
        self.cut_sheet(animation, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1)
        if self.cur_frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[self.cur_frame]
        
