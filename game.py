import sys
import pygame 

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1500

BOARD_HEIGHT = 600
BOARD_WIDTH = 1200


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        self.clock = pygame.time.Clock()

        self.tile = pygame.image.load("Assets/tile1.jpg") #TILES BACKGROUND
        self.speed = 10

       # self.front = pygame.image.load("assets/character1-01.png") #CHARACTER
       # self.back = pygame.image.load("assets/character1-02.png") #CHARACTER
       # self.left = pygame.image.load("assets/character1-03.png") #CHARACTER
       # self.right = pygame.image.load("assets/character1-04.png") #CHARACTER
        
        self.front = pygame.image.load("assets/CH2-01.png") #CHARACTER
        self.back = pygame.image.load("assets/CH2-02.png") #CHARACTER
        self.left = pygame.image.load("assets/CH2-03.png") #CHARACTER
        self.right = pygame.image.load("assets/CH2-04.png") #CHARACTER


        self.tile_width = BOARD_WIDTH // 15
        self.tile_height = BOARD_HEIGHT // 8
        self.tile = pygame.transform.scale(self.tile, (self.tile_width, self.tile_height))
        self.front = pygame.transform.scale(self.front, (70, 70))
        self.back = pygame.transform.scale(self.back, (70, 70))
        self.left = pygame.transform.scale(self.left, (70, 70))
        self.right = pygame.transform.scale(self.right, (70, 70))
        
        self.movement = [False, False, False, False] #UP, DOWN, LEFT, RIGHT
        self.img_pos = [0, 0]



    def run(self):
        while True:                      # Get the size of the image
            img_width, img_height = self.tile.get_size()
            
            for i in range(0, BOARD_WIDTH, img_width):
                for j in range(0, BOARD_HEIGHT, img_height):
                    self.screen.blit(self.tile, (i, j)) 

            self.img_pos[1] += (self.movement[1] - self.movement[0]) * self.speed
            self.img_pos[0] += (self.movement[3] - self.movement[2]) * self.speed
            
            
            if self.movement[0]:  # Up
                self.screen.blit(self.back, self.img_pos)
            elif self.movement[1]:  # Down
                self.screen.blit(self.front, self.img_pos)
            elif self.movement[2]:  # Left
                self.screen.blit(self.left, self.img_pos)
            elif self.movement[3]:  # Right
                self.screen.blit(self.right, self.img_pos)
            else:  # No movement
                self.screen.blit(self.front, self.img_pos)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True  
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True  
                    if event.key == pygame.K_LEFT:
                        self.movement[2] = True  
                    if event.key == pygame.K_RIGHT:
                        self.movement[3] = True  
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False  
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[2] = False  
                    if event.key == pygame.K_RIGHT:
                        self.movement[3] = False  
            
            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(60)


Game().run()




#WUMPUS RULES
#stench = wumpus nearby
#breeze = pit nearby
#glitter = gold nearby

#CONTROLS FOR SELF
#UP, DOWN, LEFT, RIGHT
#KILL = X
#GET GOLD = Z
#
#
#
#
#