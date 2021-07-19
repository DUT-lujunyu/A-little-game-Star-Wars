import pygame
import random
from os import path

pygame.init()  
game_folder = path.dirname(path.abspath(__file__))  
img_dir = path.join(game_folder, 'img')
snd_dir = path.join(game_folder, 'snd')
WIDTH = 500 
HEIGHT = 600 
FPS = 50
POWERUP_TIME = 5000  
HIDE_TIME = 3000  
RESUME_TIME = 10000  

#RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()  
pygame.mixer.init()  
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Shump!")  
clock = pygame.time.Clock()  

font_name = pygame.font.match_font('arial')  
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)  
    text_surface = font.render(text, True, RED)  
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)  #
    surf.blit(text_surface, text_rect)
    
def newmob(): 
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)  
    
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 70:
        pygame.draw.rect(surf, GREEN, fill_rect)
    elif pct > 40:
        pygame.draw.rect(surf, YELLOW, fill_rect)
    else:
        pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_power_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Z/X keys fire", 22, WIDTH / 2, HEIGHT / 2 + 30)
    draw_text(screen, "C keys hide", 22, WIDTH / 2, HEIGHT / 2 + 60)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()  

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38)) 
        self.rect = self.image.get_rect()  
        self.radius = 35
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10        
        self.speedx = 0  
        self.speedy = 0
        self.shield = 100  
        self.power = 100  
        self.shoot_delay = 200  
        self.count = 1  
        self.lives = 3
        self.hidden = False  
        self.last_shot = pygame.time.get_ticks()  
        self.hide_timer = pygame.time.get_ticks() 
        self.power_timer = pygame.time.get_ticks()
        self.resume_timer = pygame.time.get_ticks() 
        
    def update(self):
        self.speedx = 0  
        self.speedy = 0 
        
        if pygame.time.get_ticks() - self.hide_timer > HIDE_TIME:
            self.hidden = False           
        
        if self.count > 1 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.count = 1
            
        if self.power < 100 and pygame.time.get_ticks() - self.resume_timer > RESUME_TIME:
            self.power += 10
            self.resume_timer = pygame.time.get_ticks()
            if self.power > 100:
                self.power = 100
        
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_z]:
            self.shoot_1()
        if keystate[pygame.K_x]:
            self.shoot_2()
        if keystate[pygame.K_c]:
            if self.power >= 20 and self.hidden == False:
                self.power -= 20
                self.hide()
        if keystate[pygame.K_LEFT]:  
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8   
        if keystate[pygame.K_UP]: 
            self.speedy = -8
        if keystate[pygame.K_DOWN]: 
            self.speedy = 8

        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT       
          
    def shoot_1(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.count == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top, 1)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if self.count > 1:
                bullet_1 = Bullet(self.rect.left, self.rect.top, 1)
                bullet_2 = Bullet(self.rect.right, self.rect.top, 1)
                all_sprites.add(bullet_1)
                all_sprites.add(bullet_2)
                bullets.add(bullet_1)
                bullets.add(bullet_2)                
            shoot_sound.play()              
  
    def shoot_2(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay and self.power >= 20:
            self.last_shot = now
            self.power -= 20
            bullet = Bullet(self.rect.centerx, self.rect.top, 2)
            all_sprites.add(bullet)
            bullets_2.add(bullet)
            shoot_sound.play()
   
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        s = Shield(player)
        all_sprites.add(s)
    
    def powerup(self):
        self.count += 1
        self.power_timer = pygame.time.get_ticks()
           
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = meteor_img  
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.85 / 2) 
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-20, 20) #
        self.last_update = pygame.time.get_ticks() #
        
    def update(self):  #
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx 
        if self.rect.top > HEIGHT + 10 or self.rect.left < -30 or self.rect.right > WIDTH + 30:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8) 
            #self.speedx = random.randrange(-3, 3)
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50: 
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)  
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
      
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, kind):
        pygame.sprite.Sprite.__init__(self)
        if kind == 1:
            self.image = bullet_img
        elif kind == 2:
            self.image = bullet2_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.kind = kind
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Shield(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = shield_img
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery
    
    def update(self):
        if player.hidden == True:
            self.rect.centerx = player.rect.centerx
            self.rect.centery = player.rect.centery
        if player.hidden == False:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = ex_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0  
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(ex_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = ex_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
 
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
    
background = pygame.image.load(path.join(img_dir, "starfield.png"))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png"))
player_mini_img = pygame.transform.scale(player_img, (25, 19))
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png"))
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png"))
bullet2_img = pygame.image.load(path.join(img_dir, "Blue.png"))
shield_img = pygame.image.load(path.join(img_dir, "shield.png"))
shield_img = pygame.transform.scale(shield_img, (80, 80))
powerup_images = {}  #
powerup_images['shield'] = pygame.image.load(path.join(img_dir, "shield_gold.png"))
powerup_images['gun'] = pygame.image.load(path.join(img_dir, "bolt_gold.png"))

ex_anim = {}  
ex_anim['big'] = []
ex_anim['small'] = []
ex_anim['player'] = []

for i in range(9):
    f_name = 'ex0{}.png'.format(i+1)
    img = pygame.image.load(path.join(img_dir, f_name)).convert()
    img.set_colorkey(BLACK)
    img_big = pygame.transform.scale(img, (80, 80))
    ex_anim['big'].append(img_big)
    img_small = pygame.transform.scale(img, (30, 30))
    ex_anim['small'].append(img_small)
    ex_anim['player'].append(img)    

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:  #
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
back_sound = pygame.mixer.music.load(path.join(snd_dir, 'background.mp3'))	
pygame.mixer.music.play(loops = -1)	 


running = True
game_over = True
while running:
    if game_over:  #
        show_go_screen()
        waiting = True
        while waiting and running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYUP:
                    waiting = False 
        
        if running == False:
            break
                    
        game_over = False
        all_sprites = pygame.sprite.Group()  
        mobs = pygame.sprite.Group()  
        bullets = pygame.sprite.Group()  
        bullets_2 = pygame.sprite.Group() #
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)  
        for i in range(20):
            newmob()
        score = 0
        
    clock.tick(FPS)  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False
                    
    all_sprites.update()  
    
    hits = pygame.sprite.spritecollide(player, mobs, True)  
    for hit in hits:
        random.choice(expl_sounds).play()  
        expl = Explosion(hit.rect.center, 'small')  
        all_sprites.add(expl)
        newmob()
        
        if player.hidden == False:
            player.shield -= 30
            if player.shield <= 0:
                death = Explosion(player.rect.center, 'player')
                all_sprites.add(death)
                player.hide() 
                player.lives -= 1           
                player.rect.centerx = WIDTH / 2
                player.rect.bottom = HEIGHT - 10
                player.shield = 100
                player.power = 100
        
    hits_1 = pygame.sprite.groupcollide(bullets, mobs, True, True)
    hits_2 = pygame.sprite.groupcollide(bullets_2, mobs, False, True)
    hits_1.update(hits_2)  
    for hit in hits_1: 
        score += 20
        random.choice(expl_sounds).play()  #
        expl = Explosion(hit.rect.center, 'big')
        all_sprites.add(expl)
        if random.random() > 0.95:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()
        
    hits = pygame.sprite.spritecollide(player, powerups, True)#
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10,30)
            if player.shield > 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
                
    if player.lives == 0 and not death.alive():
        game_over = True  
    
    screen.fill(BLACK)  
    screen.blit(background, background_rect)
    all_sprites.draw(screen) 
    draw_text(screen, "scores"+str(score), 25, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_power_bar(screen, 5, 20, player.power)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    while len(mobs) < 20:
        newmob()
    pygame.display.flip()  
    
pygame.quit()