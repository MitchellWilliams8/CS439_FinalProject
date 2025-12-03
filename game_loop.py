import pygame

from camera import Camera
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from level import create_level
from player import Player
from ui import HealthBar, AmmoDisplay, FrogDisplay, ScoreDisplay

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
        self.game_started = False
        self.game_over = False
        self.game_won = False

        self.platforms, self.saws, self.heart_items, self.enemies, self.ammo_items = \
            create_level()

        self.player = Player(200, 300)
        self.player.set_game_loop(self)
        self.camera = Camera()

        self.background = pygame.image.load(background_path).convert()
        self.damage_background = pygame.image.load(damage_background_path).convert()

        self.damage_background = pygame.transform.scale(
            self.damage_background, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.health_bar = HealthBar()
        self.ammo_display = AmmoDisplay()
        self.frog_display = FrogDisplay()
        self.score_display = ScoreDisplay()

        self.flash_background_timer = 0
        self.flash_background_duration = 10
        self.flash_interval = 10

        self.load_background_music("Assets/background_music.mp3")

        self.font_large = pygame.font.Font("Assets/ShinyEyes-prr1.ttf", 72)
        self.font_small = pygame.font.Font("Assets/ShinyEyes-prr1.ttf", 36)

    def load_background_music(self, path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def trigger_background_flash(self):
        self.flash_background_timer = self.flash_background_duration

    def trigger_score_event(self):
        self.frog_display.trigger_rotation()

    def trigger_victory(self):
        self.game_won = True

    def restart_game(self):
        self.game_over = False
        self.game_won = False
        self.platforms, self.saws, self.heart_items, self.enemies, self.ammo_items = \
            create_level()
        self.player = Player(200, 300)
        self.player.set_game_loop(self)
        self.camera = Camera()
        self.frog_display.reset()

    def draw_start_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        title_text = self.font_large.render("Wizard Frog", True, (100, 255, 30))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(title_text, title_rect)

        start_text = self.font_small.render("Press SPACE to Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(start_text, start_rect)

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font_large.render("GAME OVER", True, (255, 50, 50))
        game_over_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)
        )
        self.screen.blit(game_over_text, game_over_rect)

        score_text = self.font_small.render(f"Final Score: {self.player.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
        )
        self.screen.blit(score_text, score_rect)

        restart_text = self.font_small.render("Press R to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
        )
        self.screen.blit(restart_text, restart_rect)

        quit_text = self.font_small.render("Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)
        )
        self.screen.blit(quit_text, quit_rect)

    def draw_victory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        victory_text = self.font_large.render("VICTORY!", True, (100, 255, 30))
        victory_rect = victory_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)
        )
        self.screen.blit(victory_text, victory_rect)

        score_text = self.font_small.render(f"Final Score: {self.player.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
        )
        self.screen.blit(score_text, score_rect)

        restart_text = self.font_small.render("Press R to Restart", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
        )
        self.screen.blit(restart_text, restart_rect)

        quit_text = self.font_small.render("Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)
        )
        self.screen.blit(quit_text, quit_rect)

    def draw(self):
        if self.flash_background_timer > 0:
            if (self.flash_background_timer // self.flash_interval) % 2 == 1:
                self.screen.blit(self.damage_background, (0, 0))
        else:
            bg_width = self.background.get_width()
            bg_height = self.background.get_height()

            tiles_x = (SCREEN_WIDTH // bg_width) + 1
            tiles_y = (SCREEN_HEIGHT // bg_height) + 1

            for x in range(tiles_x):
                for y in range(tiles_y):
                    tile_x = x * bg_width
                    tile_y = y * bg_height
                    self.screen.blit(self.background, (tile_x, tile_y))

        if not self.game_started:
            self.draw_start_screen()
            pygame.display.flip()
            return

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
        self.frog_display.draw(self.screen)
        self.score_display.draw(self.screen, self.player.score)

        if self.game_over:
            self.draw_game_over()
        elif self.game_won:
            self.draw_victory()

        pygame.display.flip()

    def update(self):
        if self.game_over or self.game_won or not self.game_started:
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
                    if not self.game_started:
                        if event.key == pygame.K_SPACE:
                            self.game_started = True
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False
                    if self.game_over or self.game_won:
                        if event.key == pygame.K_r:
                            self.restart_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False

            self.clock.tick(FPS)
            self.update()
            self.draw()

        pygame.mixer.music.stop()
        pygame.quit()