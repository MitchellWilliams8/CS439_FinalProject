import pygame

from camera import Camera
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from level import create_level
from player import Player
from ui import HealthBar, AmmoDisplay

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(64)

class GameLoop:
    def __init__(self, background_path="Assets/Background.png",
                 damage_background_path="Assets/Background2.png"):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

        self.platforms, self.saws, self.heart_items, self.enemies, self.ammo_items = \
            create_level()

        self.player = Player(200, 300)
        self.player.set_game_loop(self)
        self.camera = Camera()

        self.background = None
        self.damage_background = None

        self.health_bar = HealthBar()
        self.ammo_display = AmmoDisplay()

        self.load_background(background_path)
        self.load_damage_background(damage_background_path)

        self.flash_background_timer = 0
        self.flash_background_duration = 10
        self.flash_interval = 10

        self.load_background_music("Assets/background_music.mp3")

        self.font_large = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 36)

    def load_background_music(self, path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Could not load background music: {path}, Error: {e}")

    def load_damage_background(self, path):
        try:
            self.damage_background = pygame.image.load(path).convert()
            self.damage_background = pygame.transform.scale(
                self.damage_background, (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
        except Exception as e:
            print(f"Could not load damage background: {path}, Error: {e}")
            self.damage_background = None

    def trigger_background_flash(self):
        self.flash_background_timer = self.flash_background_duration

    def load_background(self, path):
        try:
            self.background = pygame.image.load(path).convert()
        except Exception as e:
            print(f"Could not load background: {path}, Error: {e}")
            self.background = None

    def restart_game(self):
        self.game_over = False
        self.platforms, self.saws, self.heart_items, self.enemies, self.ammo_items = \
            create_level()
        self.player = Player(200, 300)
        self.player.set_game_loop(self)
        self.camera = Camera()

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font_large.render("GAME OVER", True, (255, 50, 50))
        game_over_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        )
        self.screen.blit(game_over_text, game_over_rect)

        restart_text = self.font_small.render("Press R to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        )
        self.screen.blit(restart_text, restart_rect)

        quit_text = self.font_small.render("Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
        )
        self.screen.blit(quit_text, quit_rect)

    def draw(self):
        if self.flash_background_timer > 0 and self.damage_background:
            if (self.flash_background_timer // self.flash_interval) % 2 == 1:
                self.screen.blit(self.damage_background, (0, 0))
        else:
            if self.background:
                bg_width = self.background.get_width()
                bg_height = self.background.get_height()

                tiles_x = (SCREEN_WIDTH // bg_width) + 1
                tiles_y = (SCREEN_HEIGHT // bg_height) + 1

                for x in range(tiles_x):
                    for y in range(tiles_y):
                        tile_x = x * bg_width
                        tile_y = y * bg_height
                        self.screen.blit(self.background, (tile_x, tile_y))

        for platform in self.platforms:
            platform.draw(self.screen, self.camera)

        self.player.draw(self.screen, self.camera)

        for saw in self.saws:
            saw.draw(self.screen, self.camera)

        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera)

        for heart_item in self.heart_items:
            heart_item.draw(self.screen, self.camera)

        for ammo_item in self.ammo_items:
            ammo_item.draw(self.screen, self.camera)

        self.health_bar.draw(self.screen, self.player.health)
        self.ammo_display.draw(self.screen, self.player.ammo)

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def update(self):
        if self.game_over:
            return

        if self.flash_background_timer > 0:
            self.flash_background_timer -= 1

        keys = pygame.key.get_pressed()

        for platform in self.platforms:
            platform.update()
        for saw in self.saws:
            saw.update()
        for enemy in self.enemies:
            enemy.update()

        self.player.handle_input(keys)
        self.player.update(self.platforms)
        self.player.check_saw_collision(self.saws)
        self.player.check_enemy_collision(self.enemies)
        self.player.check_heart_item_collision(self.heart_items)
        self.player.check_projectile_collisions(self.enemies)
        self.player.check_ammo_item_collision(self.ammo_items)

        for projectile in self.player.projectiles[:]:
            projectile.update()
            if projectile.is_off_screen(self.camera):
                self.player.projectiles.remove(projectile)

        self.camera.update(self.player)

        if self.player.player_dead:
            self.game_over = True

    def run(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.restart_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False

            self.clock.tick(FPS)
            self.update()
            self.draw()

        pygame.mixer.music.stop()
        pygame.quit()