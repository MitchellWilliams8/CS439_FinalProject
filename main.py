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
        self.jump_power = -15

    def draw(self, screen):

        pygame.draw.rect(screen, (100, 100, 200), self.rect)

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_power

    def check_collision_x(self, platforms):
        for platform in platforms:
            if not self.rect.colliderect(platform.rect):
                continue
            if self.rect.bottom <= platform.rect.top + 15:
                continue
            if self.vel_x > 0:
                self.rect.right = platform.rect.left
            elif self.vel_x < 0:
                self.rect.left = platform.rect.right
            self.x = self.rect.x
            self.vel_x = 0

    def check_collision_y(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if not self.rect.colliderect(platform.rect):
                continue
            if self.rect.bottom <= platform.rect.top + 10 and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.y = self.rect.y
                self.vel_y = 0
                self.on_ground = True

            elif self.vel_y < 0:
                self.rect.top = platform.rect.bottom
                self.y = self.rect.y
                self.vel_y = 0

    def update(self, platforms):
        self.x += self.vel_x
        self.rect.x = self.x
        self.check_collision_x(platforms)

        self.y += self.vel_y
        self.rect.y = self.y
        self.check_collision_y(platforms)

        if not self.on_ground:
            self.vel_y = min(self.vel_y + GRAVITY, FALL_SPEED)

class Platform:

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 200), self.rect)

class GameLoop:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("")
        self.clock = pygame.time.Clock()
        self.running = True
        self.platforms = self.create_level()
        self.player = Player(200, 300)

    def create_level(self):
        platforms = []

        platforms.append(Platform(50, 400, 300, 40))
        platforms.append(Platform(500, 400, 300, 40))
        return platforms

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.player.draw(self.screen)
        for platform in self.platforms:
            platform.draw(self.screen)
        pygame.display.flip()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update(self.platforms)

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