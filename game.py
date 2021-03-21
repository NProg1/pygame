# Import pygame
import pygame
import random

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

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((5, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(SCREEN_HEIGHT-700, SCREEN_HEIGHT-450),
            )
        )
        self.speed = random.randint(5, 10)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(0,self.speed)
        if self.rect.right < 0:
            self.kill()

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))

# Instantiate player
player = Player()

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)


# Create groups to hold enemy sprites and all sprites
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

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
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Update enemy position
    #enemies.update()

    # fill screen with the blank
    screen.fill((0, 0, 0))
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)


    # draw the player on the screen
    screen.blit(player.surf, player.rect)

    # update the display
    pygame.display.flip()
    clock.tick(30)
