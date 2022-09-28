from turtle import width
import pygame
from pygame import mixer
import random
import math

# initialize pygame
pygame.init()

# set up the drawing window
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# Background
background = pygame.image.load("assets/img/backgroundMoon.jpeg")
background = pygame.transform.scale(background, (width, height))
b = 0

# Background Sound
mixer.music.load("assets/sounds/background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Gekke vlieger")
icon = pygame.image.load("assets/img/spaceship.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("assets/img/spaceship.png")
playerRotate = pygame.transform.rotate(playerImg, -90)
playerX = 80
playerY = 280
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyRotate = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("assets/img/alien.png"))
    enemyRotate.append(pygame.transform.rotate(enemyImg[i], -90))
    enemyX.append(random.randint(500, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(-20)
    enemyY_change.append(0.5)

# bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load("assets/img/bullet.png")
bulletRotate = pygame.transform.rotate(bulletImg, -90)
bulletX = 50
bulletY = 0
bulletX_change = 5
bulletY_change = 0
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("assets/fonts/Roboto-Bold.ttf", 32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font("assets/fonts/Roboto-Bold.ttf", 64)


def show_score(x, y):
    score = font.render("Score = " + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (220, 260))


def player(x, y):
    screen.blit(playerRotate, (x, y))


def enemy(x, y, i):
    screen.blit(enemyRotate[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletRotate, (x, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(
        (math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2))
    )
    if distance < 27:
        return True
    else:
        return False


# Run until the user asks to quit
running = True

while running:

    # Background color
    screen.fill((130, 40, 150))

    # Background image
    screen.blit(background, (b, 0))
    screen.blit(background, (width + b, 0))

    # Background movement
    if b == -width:
        screen.blit(background, (width + b, 0))
        b = 0

    if i == -width:
        screen.blit(background, (width + b, 0))
        b = 0
    b -= 1

    # Quit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -1
            if event.key == pygame.K_DOWN:
                playerY_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("assets/sounds/laser.wav")
                    bullet_sound.play()
                    # Get the current x cordinate of the spaceship
                    bulletY = playerY
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerY += playerY_change

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyX[i] < 140:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 0:
            enemyY_change[i] = 0.5
            enemyX[i] += enemyX_change[i]
        elif enemyY[i] >= 536:
            enemyY_change[i] = -0.5
            enemyX[i] += enemyX_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("assets/sounds/explosion.wav")
            explosion_Sound.play()
            bulletY = 0
            bulletX = 50
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(500, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletX += bulletX_change

    # Reset bullet
    if bulletX >= 800:
        bullet_state = "ready"
        bulletY = 480

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
