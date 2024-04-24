from ImageUtils import *

def generate_level(levl):
    level = pygame.Surface((len(levl[0]) * 180, len(levl) * 180))
    for y in range(len(levl)):
        for x in range(len(levl[y])):
            if levl[y][x] in (['.'] + list(map(str, range(10)))):
                level.blit(load_image('Level_pict\Пол.png'), (x * 180, y * 180))
            elif levl[y][x] == '_':
                level.blit(load_image('Level_pict\Верх.png'), (x * 180, y * 180))
            elif levl[y][x] == 'T':
                level.blit(load_image('Level_pict\ЛевоВерх.png'), (x * 180, y * 180))
            elif levl[y][x] == 'Z':
                level.blit(load_image('Level_pict\ПравоВерх.png'), (x * 180, y * 180))
            elif levl[y][x] == '(':
                level.blit(load_image('Level_pict\Лево.png'), (x * 180, y * 180))
            elif levl[y][x] == ')':
                level.blit(load_image('Level_pict\Право.png'), (x * 180, y * 180))
            elif levl[y][x] == 'L':
                level.blit(load_image('Level_pict\ЛевоНиз.png'), (x * 180, y * 180))
            elif levl[y][x] == 'J':
                level.blit(load_image('Level_pict\ПравоНиз.png'), (x * 180, y * 180))
            elif levl[y][x] == 'x':
                level.blit(load_image('Level_pict\Колонна.png'), (x * 180, y * 180))
            elif levl[y][x] == 'K':
                level.blit(load_image('Level_pict\УголПравый.png'), (x * 180, y * 180))
            elif levl[y][x] == 'X':
                level.blit(load_image('Level_pict\УголЛевый.png'), (x * 180, y * 180))
            elif levl[y][x] == '-':
                level.blit(load_image('Level_pict\Низ.png'), (x * 180, y * 180))
            elif levl[y][x] == '*':
                level.fill((21, 28, 31), (x * 180, y * 180, 180, 180))

    return level, levl
    
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину    
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')    
    return list(map(lambda x: x.ljust(max_width, '*'), level_map))
