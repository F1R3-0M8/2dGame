import pygame

#C:\DEV\python\2dGame
#https://docs.repl.it/tutorials/14-2d-platform-game

WIDTH = 400
HEIGHT = 300
BACKGROUND = (0, 0, 0)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("p1_front.png", startx, starty)
        self.stand_image = self.image
        
        self.walk_cycle = [pygame.image.load(f"p1_walk{i:0>2}.png") for i in range(1,12)]
        
        self.jump_image = pygame.image.load("p1_jump.png")
        
        self.animation_index = 0
        self.facing_left = False
        
        self.speed = 6
        self.jumpspeed = 20
        self.vsp = 0 # vertical speed
        
        self.gravity = 1
    
    def update(self, boxes):
        hsp = 0 # horizontal speed
        onground = pygame.sprite.spritecollideany(self, boxes)
        
    # check keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_q]:
            self.facing_left = True
            self.walk_animation()
            # self.move(-self.speed,0)
            hsp = -self.speed
        elif key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.facing_left = False
            self.walk_animation()
            # self.move(self.speed,0)
            hsp = self.speed
        else:
            self.image = self.stand_image
        
        if key[pygame.K_UP] or key[pygame.K_z]:
            if onground: #adding this to prevent jump when it's already in air
                # self.move(0,-self.jumpspeed)
                self.vsp = -self.jumpspeed
        
        #Gravity
        if self.vsp < 10 and not onground:
            self.jump_animation()# 9.8 rounded up
            self.vsp += self.gravity
        
        #Stop falling when the ground is reached
        if self.vsp > 0 and onground:
            self.vsp = 0
            
        #Mouvement
        self.move(hsp, self.vsp)
        
    def move(self, x, y):
        self.rect.move_ip([x,y])
        
    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
        
        if self.animation_index < len(self.walk_cycle)-1:
            self.animation_index += 1
        else:
            self.animation_index = 0
    
    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
        
class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("boxAlt.png", startx, starty)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(100, 200)

    boxes = pygame.sprite.Group()
    for bx in range(0,400,70):
        boxes.add(Box(bx,300))

    while True:
        pygame.event.pump()
        player.update(boxes)

        # Draw loop
        screen.fill(BACKGROUND)
        player.draw(screen)
        boxes.draw(screen)
        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()