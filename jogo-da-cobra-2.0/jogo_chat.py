import pygame
from pygame.locals import *
import random

WINDOW_SIZE = (600, 600)
PIXEL_SIZE = 10

def collision(pos1, pos2):
    return pos1 == pos2

def off_limits(pos):
    if 0 <= pos[0] < WINDOW_SIZE[0] and 0 <= pos[1] < WINDOW_SIZE[1]:
        return False
    else:
        return True

def random_on_grid():
    x = random.randint(0, (WINDOW_SIZE[0] - PIXEL_SIZE) // PIXEL_SIZE) * PIXEL_SIZE
    y = random.randint(0, (WINDOW_SIZE[1] - PIXEL_SIZE) // PIXEL_SIZE) * PIXEL_SIZE
    return x, y

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE))
pygame.display.set_caption("Snake")

snake_pos = [(258, 58), (268, 58), (278, 58)]
snake_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
snake_surface.fill((255, 255, 255))
snake_direction = K_LEFT

apple_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
apple_surface.fill((255, 0, 0))
apple_pos = random_on_grid()

# Variável para controlar o tamanho da cobra
snake_growth = False

while True:
    pygame.time.Clock().tick(15)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                snake_direction = event.key

    screen.blit(apple_surface, apple_pos)

    if collision(apple_pos, snake_pos[0]):
        # Colisão com a maçã, a cobra cresce
        snake_growth = True
        # Atualiza a posição da maçã até que ela não colida com a cobra
        while True:
            apple_pos = random_on_grid()
            if not any(collision(apple_pos, pos) for pos in snake_pos):
                break

    if snake_growth:
        # Adiciona um novo segmento à cobra na direção oposta
        tail = snake_pos[-1]
        if snake_direction == K_UP:
            snake_pos.append((tail[0], tail[1] + PIXEL_SIZE))
        elif snake_direction == K_DOWN:
            snake_pos.append((tail[0], tail[1] - PIXEL_SIZE))
        elif snake_direction == K_LEFT:
            snake_pos.append((tail[0] + PIXEL_SIZE, tail[1]))
        elif snake_direction == K_RIGHT:
            snake_pos.append((tail[0] - PIXEL_SIZE, tail[1]))
        snake_growth = False

    for pos in snake_pos:
        screen.blit(snake_surface, pos)

    for i in range(len(snake_pos) - 1, 0, -1):
        if collision(snake_pos[0], snake_pos[i]):
            pygame.quit()
            quit()
        snake_pos[i] = snake_pos[i - 1]

        if off_limits(snake_pos[0]):
            pygame.quit()
            quit()

    if snake_direction == K_UP:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] - PIXEL_SIZE)
    elif snake_direction == K_DOWN:
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] + PIXEL_SIZE)
    elif snake_direction == K_LEFT:
        snake_pos[0] = (snake_pos[0][0] - PIXEL_SIZE, snake_pos[0][1])
    elif snake_direction == K_RIGHT:
        snake_pos[0] = (snake_pos[0][0] + PIXEL_SIZE, snake_pos[0][1])

    pygame.display.update()
