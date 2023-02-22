from typing import Tuple
import pygame, sys
'''
Variables
'''
pygame.init()
worldx = 960
worldy = 720
FPS = 30
animat = 4
clock = pygame.time.Clock()
world = pygame.display.set_mode([worldx, worldy])

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)
'''
Objects
'''


class Player(pygame.sprite.Sprite):
  """
  Spawn a player
  """

  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.movex = 0  # move along X
    self.movey = 0  # move along Y
    self.frame = 0  # count frames
    self.health = 10
    self.images = []
    for i in range(0, 5):
      img = pygame.image.load('images/hero' + str(i) + '.png').convert()
      img.convert_alpha()  # optimise alpha
      img.set_colorkey(ALPHA)  # set alpha

      self.images.append(img)
      self.image = self.images[0]
      self.rect = self.image.get_rect()

  def control(self, x, y):
    '''
    control player movement
    '''
    
    self.movex += x
    self.movey += y

  def update(self):
    """
    Update sprite position
    """
    self.rect.x = self.rect.x + self.movex
    self.rect.y = self.rect.y + self.movey

    # moving left
    if self.movex < 0:
        self.frame += 1
        if self.frame > 3 * animat:
            self.frame = 0
        self.image = pygame.transform.flip(
            self.images[self.frame // animat], True, False)

    # moving right
    if self.movex > 0:
        self.frame += 1
        if self.frame > 3 * animat:
            self.frame = 0
        self.image = self.images[self.frame // animat]
    hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
    for enemy in hit_list:
      self.health -= 1
      print(self.health)


class Enemy(pygame.sprite.Sprite):
  '''
  Enemy spawn
  '''

  def __init__(self,x,y,img):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('images/'+ img)
    self.image.convert_alpha()
    self.image.set_colorkey(ALPHA)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.counter = 0
  def move(self):
    '''
    enemy movement
    '''
    distant = 25
    speed = 1.25

    if self.counter >= 0 and self.counter <= distant:
      self.rect.x += speed
    
    elif self.counter >= distant and self.counter <= distant*2:
      self.rect.x  -= speed
    else:
      self.counter = 0
    self.counter += 1
class Level():
  
  def bad(lvl, eloc):
    
    if lvl == 1:
      enemy = Enemy(eloc[0],eloc[1], 'enemy.png')
      enemy_list = pygame.sprite.Group()
      enemy_list.add(enemy)
    if lvl == 2:
      print('Level' + str(lvl))
    return enemy_list
    
    

'''
Setup
'''

backdrop = pygame.image.load(('images/Background.png'))
clock = pygame.time.Clock()
pygame.init()
backdropbox = world.get_rect()
main = True
player = Player()  # spawn player
player.rect.x = 0  # go to x
player.rect.y = 0  # go to y
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 2.5
eloc = []
eloc = [300,10]
enemy_list = Level.bad(1, eloc)
Enemy = Enemy(300,10, 'enemy.png') # spawn enemy
enemy_list = pygame.sprite.Group() # create enemy group
enemy_list.add(Enemy) 

'''
Main loop
'''

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            main = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.control(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('jump')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                main = False

    world.blit(backdrop, backdropbox)
    
    
    player.update()
    player_list.draw(world)
    enemy_list.draw(world)
    enemy_list.draw(world)
    for e in enemy_list:
      e.move()
    pygame.display.flip()
    clock.tick(FPS)
