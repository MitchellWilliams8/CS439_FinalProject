import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
GRAVITY = 0.8
FALL_SPEED = 15

class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 48
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.on_ground = False

    def draw(self, screen):

        pygame.draw.rect(screen, (100, 100, 200), self.rect)

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed

    def update(self):
        self.x += self.vel_x
        self.rect.x = self.x

        self.y += self.vel_y
        self.rect.y = self.y

        if not self.on_ground:
            self.vel_y = min(self.vel_y + GRAVITY, FALL_SPEED)

class GameLoop:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("")
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(200, 300)

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.player.draw(self.screen)
        pygame.display.flip()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.clock.tick(FPS)
            self.update()
            self.draw()

        pygame.quit()

game = GameLoop()
game.run()