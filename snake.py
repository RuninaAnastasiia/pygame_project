import pygame
from random import randrange

# задаем размер рабочего поля и единичного отрезка змейки, а также размер печеньки
RES = 600
SIZE = 50


def load_image(name, colorkey=None):
    fullname = name
    # если файл не существует, то выходим
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Error", name)
        raise SystemError(message)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# функция отвечающая за закрытие окна
def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


# функция отвечающая за вывод на экран предупреждения об окончании игры
def ended():
    flags = pygame.DOUBLEBUF | pygame.RESIZABLE
    window = pygame.display.set_mode([RES, RES])
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", True, (147, 112, 219))
    text_x = 640 // 2 - text.get_width() // 2
    text_y = 490 // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    window.blit(text, (text_x - 10, text_y))
    pygame.draw.rect(window, (147, 112, 219), (text_x - 20, text_y - 10,
                                               text_w + 20, text_h + 20), 1)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYDOWN:
                if event.key == 32:
                    run = False
                    start()
        pygame.display.flip()


# функция в который храниться основной код игры
def start():
    pygame.display.set_caption('Snake for Python')

    # фоновая музыка
    pygame.init()
    pygame.mixer.music.load('game.mp3')
    pygame.mixer.music.play()

    # начальное положение змейки
    x, y = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
    # начальное положение яблока
    sprite = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
    # длинна змейки
    length = 1
    # сама змейка
    snake = [(x, y)]
    # направления движения змейки
    dx, dy = 0, 0
    # скорость змейки
    fps = 30
    dirs = {'UP': True, 'DOWN': True, 'LEFT': True, 'RIGHT': True, }
    # счетчик
    score = 0
    speed_count, snake_speed = 0, 10

    # создание игрового поля
    pygame.init()
    screen = pygame.display.set_mode([RES, RES])
    clock = pygame.time.Clock()
    font_score = pygame.font.SysFont('Arial', 26, bold=True)
    font_end = pygame.font.SysFont('Arial', 66, bold=True)
    img = pygame.image.load('fon.jpg').convert()
    im = load_image("Cookie.png", -1)
    im = pygame.transform.scale(im, (70, 70))
    # игровой цикл
    while True:
        screen.blit(img, (0, 0))
        # создание головы змейки
        [pygame.draw.rect(screen, pygame.Color(147, 112, 219), (i, j, SIZE - 1, SIZE - 1)) for i, j in snake]
        # создание печеньки
        pygame.draw.rect(screen, pygame.Color('red'), (*sprite, SIZE, SIZE))
        screen.blit(im, (int(sprite[0]) - 10, int(sprite[1]) - 10))
        # вывод счета на экран
        render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color(255, 105, 180))
        screen.blit(render_score, (5, 5))
        speed_count += 1
        # движение змейки
        if not speed_count % snake_speed:
            x += dx * SIZE
            y += dy * SIZE
            # добавление шагов змейки в ее список координат
            snake.append((x, y))
            # срез координат змейки, чтобы она не была бесконечной
            snake = snake[-length:]
        # описание поедания печеньки
        if snake[-1] == sprite:
            sprite = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
            length += 1
            score += 1
            snake_speed -= 1
            snake_speed = max(snake_speed, 4)
        # описание завершения игры если мы врезались в стенку или змейка укусила себя
        if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
            ended()

        pygame.display.flip()
        clock.tick(fps)
        close_game()

        # получение информации о всех нажатых клавишах
        key = pygame.key.get_pressed()
        # если нажата стрелка вверх, то и змейка движентся вверх
        if key[pygame.K_UP]:
            if dirs['UP']:
                dx, dy = 0, -1
                # проверка на нажатие
                dirs = {'UP': True, 'DOWN': False, 'LEFT': True, 'RIGHT': True, }
        # если нажата стрелка вниз, то и змейка движентся вниз
        elif key[pygame.K_DOWN]:
            if dirs['DOWN']:
                dx, dy = 0, 1
                # проверка на нажатие
                dirs = {'UP': False, 'DOWN': True, 'LEFT': True, 'RIGHT': True, }
        # если нажата стрелка  налево, то и змейка движентся влево
        elif key[pygame.K_LEFT]:
            if dirs['LEFT']:
                dx, dy = -1, 0
                # проверка на нажатие
                dirs = {'UP': True, 'DOWN': True, 'LEFT': True, 'RIGHT': False, }
        # если нажата стрелка  направо, то и змейка движентся вправо
        elif key[pygame.K_RIGHT]:
            if dirs['RIGHT']:
                dx, dy = 1, 0
                # проверка на нажатие
                dirs = {'UP': True, 'DOWN': True, 'LEFT': False, 'RIGHT': True, }


start()
