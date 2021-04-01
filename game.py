import pygame
import random
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
)


# constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

# background
bg = pygame.image.load("assets/bg.png")
bg = pygame.transform.scale(bg,(500,600))
bgX = 0
bgX2 = bg.get_height()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("assets/Spaceship.png").convert()
        self.surf = pygame.transform.scale(self.surf,(40,60))
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-150))

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
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        return bullet


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("assets/meteor.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(SCREEN_HEIGHT - 700, SCREEN_HEIGHT - 450),
            )
        )
        self.speed = random.randint(2, 7)

    # Move the sprite based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top < 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    """A class that manages bullets fired by spaceships"""

    def __init__(self, x, y):
        """Create a bullet object where the ship is located"""
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((5, 5))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        # The location of the bullet is represented by a decimal
        self.color = (60, 60, 60)
        self.speed = -10

    def update(self):
        """Move the bullet up"""
        # Update the decimal value that represents the bullet position
        self.rect.y += self.speed
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# initialization
pygame.init()

# create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((0, 0, 0))

def draw_background():
    # first image
    screen.blit(bg, (0, bgX))
    #seond image
    screen.blit(bg, (0, bgX2))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# instantiate the player
player = Player()

# Create groups to hold enemy sprites and all sprites
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# setup the clock for framerate
clock = pygame.time.Clock()

# gameloop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            player.update(event.key)
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_SPACE:
                bullet = player.shoot()
                bullets.add(bullet)
                all_sprites.add(bullet)

        elif event.type == QUIT:
            running = False
        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
  
    draw_background()
    bgX -= 1
    bgX2 -= 1
    
    if bgX < bg.get_height() * -1:
        bgX = bg.get_height()

    if bgX2 < bg.get_height() * -1:
        bgX2 = bg.get_height()


    # draw the player to the screen
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        m = Enemy()
        all_sprites.add(m)
        enemies.add(m)

    # update the display
    enemies.update()
    bullets.update()
    pygame.display.flip()
    clock.tick(30)
