import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Sounds
bullet_sound = pygame.mixer.Sound("alienshoot1.wav")
background_music = pygame.mixer.Sound("background_music.ogg")
bullet_sounds = []
bullet_sound.set_volume(1)
background_music.set_volume(1)

# Screen dimensions
screen_width = 570
screen_height = 1000

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Starship Game")

# Load background image
starry_background = pygame.image.load("starry_background.jpg")
background_rect = starry_background.get_rect()
background_y1 = 0
background_y2 = -background_rect.height

# Load the starship image
starship_image = pygame.image.load("starship.png")

# New dimensions for the starship
new_width = 100
new_height = 100

# Resize the starship image
starship_image = pygame.transform.scale(starship_image, (new_width, new_height))
starship_rect = starship_image.get_rect()

# Starship's initial position
starship_x = screen_width // 2 - starship_rect.width // 2
starship_y = screen_height - starship_rect.height - 10

# Initialize bullets
bullets = []
bullet_speed = 2
last_bullet_time = 0
bullet_cooldown = 300

# Initialize enemy ships
enemy_ships = []
small_ship_w = 100
small_ship_h = 100


class EnemyShip:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (small_ship_w, small_ship_h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Create enemy ships
for _ in range(3):
    x = random.randint(0, screen_width - small_ship_w)
    y = random.randint(0, screen_height // 2)
    enemy_ship = EnemyShip("small_enemy_ship.png", x, y)
    enemy_ships.append(enemy_ship)

# Game state flags
game_started = False
game_over = False

while not game_over:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.quit()
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    for key in keys:
        if key:
            game_started = True

    if keys[pygame.K_LEFT] and starship_x > 0:
        starship_x -= 1
    if keys[pygame.K_RIGHT] and starship_x < screen_width - starship_rect.width:
        starship_x += 1

    if game_started:
        background_y1 += 0.41
        background_y2 += 0.41

        for enemy_ship in enemy_ships:
            enemy_ship.rect.y += 0.41

        if background_y1 > background_rect.height:
            background_y1 = 0

        if background_y2 > 0:
            background_y2 = -background_rect.height

        if enemy_ship.rect.y > screen_height:
            enemy_ship.rect.y = 0
            enemy_ship.rect.x = random.randint(1, 500)

        if keys[pygame.K_UP] and current_time - last_bullet_time > bullet_cooldown:
            new_bullet_sound = pygame.mixer.Sound("alienshoot1.wav")
            new_bullet_sound.set_volume(1)
            new_bullet_sound.play()
            bullet_sounds.append([new_bullet_sound, current_time])

            bullet_x = starship_x + starship_rect.width // 10
            bullet_x2 = starship_x + starship_rect.width // 2
            bullet_y = starship_y
            bullets.append([bullet_x, bullet_y])
            bullets.append([bullet_x2, bullet_y])
            last_bullet_time = current_time

    screen.blit(starry_background, (0, background_y1))
    screen.blit(starry_background, (0, background_y2))

    screen.blit(starship_image, (starship_x, starship_y))

    for enemy_ship in enemy_ships:
        screen.blit(enemy_ship.image, (enemy_ship.rect.x, enemy_ship.rect.y))

    for bullet in bullets:
        bullet[1] -= bullet_speed
        pygame.draw.rect(screen, (255, 0, 0), (bullet[0], bullet[1], 5, 10))

    for bullet_sound, start_time in bullet_sounds:
        elapsed_time = current_time - start_time
        if elapsed_time >= bullet_sound.get_length() * 1000:
            bullet_sounds.remove([bullet_sound, start_time])

    for bullet in bullets:
        for enemy_ship in enemy_ships:
            if (bullet[1] < enemy_ship.rect.y + enemy_ship.rect.height and
                    bullet[1] + 10 > enemy_ship.rect.y and
                    bullet[0] < enemy_ship.rect.x + enemy_ship.rect.width and
                    bullet[0] + 5 > enemy_ship.rect.x):
                bullets.remove(bullet)
                enemy_ships.remove(enemy_ship)

    bullets = [bullet for bullet in bullets if bullet[1] > -10]

    pygame.display.update()
