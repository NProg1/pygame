# Import pygame
import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

    
    def update(self, pressed_keys):
        if pressed_keys == K_LEFT:
            self.rect.move_ip(-5, 0)
        if pressed_keys == K_RIGHT:
            self.rect.move_ip(5, 0)
        if pressed_keys == K_UP:
            self.rect.move_ip(0, -5)
        if pressed_keys == K_DOWN:
            self.rect.move_ip(0, 5)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))

# Instantiate player
player = Player()

# Variable to keep the game loop running
running = True

# setup the clock for a decent framerate
clock = pygame.time.Clock()

# game loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # check for keydown press
        if event.type == KEYDOWN:
            player.update(event.key)
            if event.key == K_ESCAPE:
                running = False 

    # fill screen with the blank
    screen.fill((0, 0, 0))

    # draw the player on the screen
    screen.blit(player.surf, player.rect)

    # update the display
    pygame.display.flip()
    clock.tick(30)
