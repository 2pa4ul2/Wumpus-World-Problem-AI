import sys
import pygame 

HEIGHT = 600
WIDTH = 800


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.clock = pygame.time.Clock()

        self.img = pygame.image.load("Assets/tile1.jpg") #TILES BACKGROUND
        self.img = pygame.transform.scale(self.img, (50, 50))


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)

            for i in range(0, HEIGHT, WIDTH):
                for j in range(0, HEIGHT, HEIGHT):
                    self.screen.blit(self.img, (i, j))   

            pygame.display.flip()


Game().run()