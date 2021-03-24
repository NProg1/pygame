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
    K_SPACE,
)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((5, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.color = (60,60,60)
        self.speed = -10

    def update(self):
        """Move the bullet up"""
        self.rect.y += self.speed
        # kill the bullet once off screen
        if self.rect.bottom < 0:
            self.kill()

    


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT-150))

    
    def update(self, pressed_keys):
        if pressed_keys == K_LEFT:
            self.rect.move_ip(-5, 0)
        if pressed_keys == K_RIGHT:
            self.rect.move_ip(5, 0)
        if pressed_keys == K_UP:
            self.rect.move_ip(0, -5)
        if pressed_keys == K_DOWN:
            self.rect.move_ip(0, 5)
          # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom == SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        # all_sprites.add(bullets)
        # bullets.add(bullet)
        return bullet

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
bullets = pygame.sprite.Group()
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
            if event.key == K_SPACE:
                new_bullet = player.shoot()
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
    
    # check to see if a bullet hit a enemy
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    # replace killed enemy with new enemy
    for hit in hits:
        m = Enemy()
        all_sprites.add(m)
        enemies.add(m)

    # Update enemy position
    enemies.update()
    bullets.update()


    # fill screen with the blank
    screen.fill((0, 0, 0))
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False


    # draw the player on the screen
    screen.blit(player.surf, player.rect)

    # update the display
    pygame.display.flip()
    clock.tick(30)
