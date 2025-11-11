import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 48
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen):

        pygame.draw.rect(screen, (100, 100, 200), self.rect)

class GameLoop:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("")
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(200, 300)

    def draw(self):
        self.player.draw(self.screen)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.clock.tick(FPS)
            self.draw()
            pygame.display.flip()

        pygame.quit()

game = GameLoop()
game.run()