import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure of the Girl")

# Загрузка изображения для фонового изображения и увеличение его размера
background_image = pygame.image.load("forest.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_rect = background_image.get_rect()

# Размещение фонового изображения на экране
background_rect.topleft = (0, 0)

# Загрузка изображения для главного героя (девочки) и уменьшение его размера
girl_image = pygame.image.load("girls.png")  # Путь к изображению главного героя
girl_image = pygame.transform.scale(girl_image, (130, 110))

girl_rect = girl_image.get_rect()
girl_rect.bottomleft = (0, SCREEN_HEIGHT // 2)  # Установка начальных координат в левый нижний угол

# Загрузка изображения для монстра и уменьшение его размера
monster_image = pygame.image.load("monster.png")
monster_image = pygame.transform.scale(monster_image, (100, 100))

# Загрузка изображения начального экрана
start_screen_image = pygame.image.load("start.jpg")
start_screen_image = pygame.transform.scale(start_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_screen_rect = start_screen_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Загрузка изображения экрана победы
win_screen_image = pygame.image.load("win.jpg")
win_screen_image = pygame.transform.scale(win_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
win_screen_rect = win_screen_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Загрузка аудиофайла для фоновой музыки
pygame.mixer.music.load("спасение.mp3")  # Путь к аудиофайлу фоновой музыки
pygame.mixer.music.set_volume(0.5)  # Установка громкости

# Загрузка аудиофайла для начальной музыки
start_music = pygame.mixer.Sound("начало .mp3")  # Путь к аудиофайлу начальной музыки
start_music.set_volume(0.5)  # Установка громкости

# Список монстров
monsters = []

# Переменная для отслеживания количества избежанных монстров
escaped_monsters = 0

# Переменная для определения целевого количества избежанных монстров
target_escaped_monsters = 10

# Шрифт для отображения счетчика
font = pygame.font.Font(None, 36)

# Функция для создания нового монстра
def create_monster():
    monster = {
        "rect": monster_image.get_rect(),
        "speed": random.randint(1, 3),  # Скорость монстра
    }
    monster["rect"].right = SCREEN_WIDTH
    monster["rect"].top = random.randint(0, SCREEN_HEIGHT - monster["rect"].height)
    return monster

# Функция для отрисовки монстров на экране
def draw_monsters():
    for monster in monsters:
        screen.blit(monster_image, monster["rect"])

# Функция для обновления положения монстров
def update_monsters():
    global escaped_monsters
    for monster in monsters:
        monster["rect"].x -= monster["speed"]
        if monster["rect"].right < 0:  # Если монстр вышел за пределы экрана
            monsters.remove(monster)
            escaped_monsters += 1

# Функция для проверки столкновения главного героя с монстрами
def check_collision():
    for monster in monsters:
        if girl_rect.colliderect(monster["rect"]):
            return True
    return False

# Функция для отображения изображения "Game Over"
def show_game_over():
    game_over_image = pygame.image.load("game.png")  # Загрузка изображения с надписью "Game Over"
    game_over_image = pygame.transform.scale(game_over_image, (800, 600))  # Изменение размера изображения
    image_rect = game_over_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Определение положения изображения
    screen.blit(game_over_image, image_rect)  # Отображение изображения на экране

# Функция для отображения изображения "Win"
def show_win_screen():
    screen.blit(win_screen_image, win_screen_rect)
    pygame.display.flip()
    wait_for_keypress()

# Скорость перемещения главного героя (девочки)
speed = 3

# Таймер для создания новых монстров
CREATE_MONSTER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_MONSTER_EVENT, 1400)  # Уменьшение интервала появления монстров

# Функция для отображения начального экрана
def show_start_screen():
    screen.blit(start_screen_image, start_screen_rect)
    pygame.display.flip()
    start_music.play()  # Проигрывание начальной музыки
    wait_for_keypress()
    start_music.stop()  # Остановить начальную музыку после нажатия клавиши

# Функция ожидания нажатия клавиши
def wait_for_keypress():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

# Основной игровой цикл
running = True
game_over = False
game_won = False
start_screen_displayed = False

while running:
    if not start_screen_displayed:
        show_start_screen()
        start_screen_displayed = True
        pygame.mixer.music.play(-1)  # Начинаем воспроизведение фоновой музыки

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == CREATE_MONSTER_EVENT:
            if not game_over and not game_won:  # Добавляем проверку, чтобы монстры не создавались после завершения игры
                monsters.append(create_monster())

    if not game_over and not game_won:
        # Управление главным героем (девочкой)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and girl_rect.top > 0:
            girl_rect.y -= speed
        if keys[pygame.K_DOWN] and girl_rect.bottom < SCREEN_HEIGHT:
            girl_rect.y += speed

        # Очистка экрана
        screen.fill(WHITE)

        # Отрисовка фонового изображения
        screen.blit(background_image, background_rect)

        # Отрисовка главного героя (девочки)
        screen.blit(girl_image, girl_rect)

        # Обновление и отрисовка монстров
        update_monsters()
        draw_monsters()

        # Проверка столкновения с монстрами
        if check_collision():
            game_over = True
            pygame.mixer.music.stop()  # Останавливаем музыку при завершении игры

        # Проверка достижения цели (избежать 10 монстров)
        if escaped_monsters >= target_escaped_monsters:
            game_won = True
            pygame.mixer.music.stop()  # Останавливаем музыку при достижении цели
            show_win_screen()

        # Отображение счетчика избежанных монстров
        score_text = font.render(f"Escaped Monsters: {escaped_monsters}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Если game_over, показываем надпись "Game Over"
        if game_over:
            show_game_over()

        # Обновление экрана
        pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
sys.exit()
