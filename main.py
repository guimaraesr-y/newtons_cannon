import pygame, sys, math
from env import *
pygame.init()
pygame.mixer.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.mixer.music.load('./src/explosion.wav')
pygame.display.set_caption("Newton's Cannon")
running = True
FPS = 120
shoot_force = 8.0

class Earth(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./src/earth.png').convert_alpha()
        img_w, img_h = self.image.get_size()
        self.image = pygame.transform.smoothscale(self.image, (int(img_w*0.21),int(img_h*0.21)))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.mass = 10**3
    
    def update(self):
        collided = self.check_collision()
        if collided:
            for i in collided: i.kill()
            pygame.mixer.music.play()
    
    def check_collision(self):
        return pygame.sprite.spritecollide(self, bullets, False, collided=pygame.sprite.collide_mask)

class Cannon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('./src/cannon.png').convert_alpha()
        img_w, img_h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(img_w*0.009), int(img_h*0.009)))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y+14

class Ammo(pygame.sprite.Sprite):
    def __init__(self, vx, mass):
        super().__init__()
        self.radius = 5
        self.image = pygame.Surface((2*self.radius, 2*self.radius))
        pygame.draw.circle(self.image,(255,0,0),(self.radius,self.radius),self.radius,0)

        self.rect = self.image.get_rect()
        self.rect.center = (cannon.rect.centerx+16, cannon.rect.centery-5)

        self.vx = vx
        self.vy = 0
        self.mass = mass

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.gravity(earth)

        if self.rect.left>SCREEN_WIDTH+500 or self.rect.right<-500 or self.rect.bottom<-500 or self.rect.top>SCREEN_HEIGHT+500:
            self.kill()
    
    def gravity(self, earth):
        dx = self.rect.centerx - earth.rect.centerx
        dy = self.rect.centery - earth.rect.centery
        d = math.sqrt((dx*dx+dy*dy))

        G = 12
        F = (G*self.mass * earth.mass) / d**2

        self.vx += -(dx/d) * (F/self.mass)
        self.vy += -(dy/d) * (F/self.mass)

class Button:
    def __init__(self, button_src, text, pos, callback):
        self.image = pygame.image.load('./src/grey_button01.png').convert_alpha()
        fontsys=pygame.font.SysFont('Monospace', 20)
        self.text = fontsys.render(text, 1, (0,0,0))
        self.image.blit(self.text, 
            (self.image.get_width()/2-self.text.get_width()/2, 
            self.image.get_height()/2-self.text.get_height()/2)
        )
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.callback = callback
    
    def render(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def check_click(self, x, y):
        if self.rect.collidepoint(x, y):
            self.callback()

def shoot():
    bullets.add(Ammo(shoot_force, 100))

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

earth = Earth()
cannon = Cannon(earth.rect.centerx, earth.rect.top)

all_sprites.add(earth)
all_sprites.add(cannon)

shoot()
launch_button = Button('./src/grey_button01.png', 'Fire!', (SCREEN_WIDTH-150, SCREEN_HEIGHT-50), shoot)

def move_scene(direction):
    if direction == 0:
        for sprite in all_sprites.sprites():
            sprite.rect.x -= 50
        for sprite in bullets.sprites():
            sprite.rect.x -= 50
    if direction == 1:
        for sprite in all_sprites.sprites():
            sprite.rect.x += 50
        for sprite in bullets.sprites():
            sprite.rect.x += 50
    if direction == 2:
        for sprite in all_sprites.sprites():
            sprite.rect.y -= 50
        for sprite in bullets.sprites():
            sprite.rect.y -= 50
    if direction == 3:
        for sprite in all_sprites.sprites():
            sprite.rect.y += 50
        for sprite in bullets.sprites():
            sprite.rect.y += 50

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                shoot_force -= 0.1
            if event.key == pygame.K_RIGHT:
                shoot_force += 0.1
            if event.key == pygame.K_SPACE:
                shoot()
            if event.key == pygame.K_a: move_scene(1)
            if event.key == pygame.K_d: move_scene(0)
            if event.key == pygame.K_w: move_scene(3)
            if event.key == pygame.K_s: move_scene(2)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            launch_button.check_click(mouse_x, mouse_y)
    screen.fill((0,0,10))

    fontsys = pygame.font.SysFont('Monospace', 20)
    shoot_text = fontsys.render('Force: '+str(shoot_force*100), 1, (255,255,255))
    screen.blit(shoot_text, (10, 10))

    all_sprites.update()
    all_sprites.draw(screen)
    bullets.update()
    bullets.draw(screen)

    launch_button.render()

    pygame.display.flip()
    clock.tick(FPS)
