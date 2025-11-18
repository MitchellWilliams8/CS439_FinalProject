import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
GRAVITY = 0.8
FALL_SPEED = 15

class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0

    def apply(self, rect):
        return pygame.Rect(rect.x - self.offset_x, rect.y - self.offset_y, rect.width, rect.height)

    def update(self, target):
        self.offset_x = target.rect.centerx - SCREEN_WIDTH // 2
        self.offset_y = target.rect.centery - SCREEN_HEIGHT // 2

class Player:

    def __init__(self, x, y, sprite_sheet_path="Assets/Player.png"):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.hitbox_width = 35
        self.hitbox_height = 55
        self.rect = pygame.Rect(x, y, self.hitbox_width, self.hitbox_height)

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.on_ground = False
        self.jump_power = -15
        self.on_moving_platform = None
        self.health = 100
        self.player_dead = False
        self.facing_right = True

        self.damage_cooldown = 0
        self.damage_cooldown_max = 60
        self.invincible = False
        self.game_loop = None
        self.sprite_sheet = None
        self.animations = {'idle': [],'walk_right': [],'walk_left': [],'jump': [],'fall': []}
        self.current_animation = 'idle'
        self.current_frame = 0
        self.frame_counter = 0

        self.animation_speeds = {'idle': 15,'walk_right': 8,'walk_left': 8,'jump': 12,'fall': 12}

        self.load_sprite_sheet(sprite_sheet_path)

    def set_game_loop(self, game_loop_instance):
        self.game_loop = game_loop_instance

    def load_sprite_sheet(self, path, frame_width=32, frame_height=32, idle_frames=2, walk_frames=3, jump_frames=2):
        try:
            self.sprite_sheet = pygame.image.load(path).convert_alpha()

            frame_index = 0

            for i in range(idle_frames):
                frame_x = frame_index * frame_width
                frame = self.sprite_sheet.subsurface(pygame.Rect(frame_x, 0, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (self.width, self.height))
                self.animations['idle'].append(frame)
                frame_index += 1

            for i in range(walk_frames):
                frame_x = frame_index * frame_width
                frame = self.sprite_sheet.subsurface(pygame.Rect(frame_x, 0, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (self.width, self.height))
                self.animations['walk_right'].append(frame)
                frame_index += 1

            for frame in self.animations['walk_right']:
                flipped = pygame.transform.flip(frame, True, False)
                self.animations['walk_left'].append(flipped)

            for i in range(jump_frames):
                frame_x = frame_index * frame_width
                frame = self.sprite_sheet.subsurface(pygame.Rect(frame_x, 0, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (self.width, self.height))
                self.animations['jump'].append(frame)
                frame_index += 1

            if self.animations['jump']:
                self.animations['fall'] = [self.animations['jump'][-1]]

        except Exception as e:
            print(f"Could not load sprite sheet: {path}, Error: {e}")
            self.sprite_sheet = None

    def update_animation(self):
        new_animation = 'idle'

        is_grounded = self.on_ground or abs(self.vel_y) < 1

        if not is_grounded:
            new_animation = 'jump'
        elif abs(self.vel_x) > 0.1:
            if self.vel_x > 0:
                new_animation = 'walk_right'
                self.facing_right = True
            else:
                new_animation = 'walk_left'
                self.facing_right = False

        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.current_frame = 0
            self.frame_counter = 0

        if self.animations[self.current_animation]:
            frames = self.animations[self.current_animation]
            current_speed = self.animation_speeds.get(self.current_animation, 15)
            self.frame_counter += 1

            if self.frame_counter >= current_speed:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(frames)

    def draw(self, screen, camera):
        sprite_rect = pygame.Rect(
            self.rect.x - (self.width - self.hitbox_width) // 2,
            self.rect.y - (self.height - self.hitbox_height) // 2,
            self.width,
            self.height
        )
        draw_rect = camera.apply(sprite_rect)

        if self.animations[self.current_animation] and len(self.animations[self.current_animation]) > 0:
            frames = self.animations[self.current_animation]

            if self.current_frame >= len(frames):
                self.current_frame = 0

            current_surface = frames[self.current_frame]

            screen.blit(current_surface, draw_rect)
        else:
            pygame.draw.rect(screen, (100, 100, 200), draw_rect)

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed

        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            self.on_moving_platform = None

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
        self.on_moving_platform = None

        ground_tolerance = 3

        for platform in platforms:
            if not self.rect.colliderect(platform.rect):
                continue

            if self.vel_y >= 0 and self.rect.bottom <= platform.rect.top + ground_tolerance + abs(self.vel_y):
                self.rect.bottom = platform.rect.top
                self.y = self.rect.y
                self.vel_y = 0
                self.on_ground = True

                if platform.type in ("moving_vertical", "moving_horizontal"):
                    self.on_moving_platform = platform
                    if platform.vel_x != 0:
                        self.x += platform.vel_x
                        self.rect.x = self.x
                break

            elif self.vel_y < 0 and self.rect.top < platform.rect.bottom:
                self.rect.top = platform.rect.bottom
                self.y = self.rect.y
                self.vel_y = 0

    def check_saw_collision(self, saws):
        if self.invincible:
            return

        for saw in saws:
            if self.rect.colliderect(saw.rect):
                self.health -= 20
                self.damage_cooldown = self.damage_cooldown_max
                self.invincible = True
                if self.game_loop:
                    self.game_loop.trigger_background_flash()
                break

    def update(self, platforms):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
            if self.damage_cooldown == 0:
                self.invincible = False

        if not self.on_ground:
            self.vel_y = min(self.vel_y + GRAVITY, FALL_SPEED)

        self.y += self.vel_y
        self.rect.y = self.y
        self.check_collision_y(platforms)

        current_platform = self.on_moving_platform

        if current_platform and current_platform.vel_y > 0:
            self.y += current_platform.vel_y
            self.rect.y = self.y
            self.check_collision_y(platforms)
            if self.on_ground:
                current_platform = self.on_moving_platform

        if current_platform and current_platform.vel_x != 0:
            self.x += current_platform.vel_x
            self.rect.x = self.x

        self.x += self.vel_x
        self.rect.x = self.x
        self.check_collision_x(platforms)

        if self.y >= 1000:
            self.health -= 100

        if self.health <= 0:
            self.player_dead = True

        self.update_animation()

class Saw:

    def __init__(self, x, y, sprite_sheet_path="Assets/Saw.png"):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.hitbox_width = 70
        self.hitbox_height = 70
        self.rect = pygame.Rect(x + (self.width - self.hitbox_width) // 2,y + (self.height - self.hitbox_height) // 2,self.hitbox_width,self.hitbox_height)

        self.sprite_sheet = None
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.5
        self.frame_counter = 0

        self.load_sprite_sheet(sprite_sheet_path)

    def load_sprite_sheet(self, path, frame_width=32, frame_height=32, num_frames=4):
        try:
            self.sprite_sheet = pygame.image.load(path).convert_alpha()

            for i in range(num_frames):
                frame_x = i * frame_width
                frame = self.sprite_sheet.subsurface(pygame.Rect(frame_x, 0, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (self.width, self.height))
                self.frames.append(frame)
        except:
            print(f"Could not load sprite sheet: {path}")
            self.sprite_sheet = None

    def update(self):
        if self.frames:
            self.frame_counter += self.animation_speed
            if self.frame_counter >= 1:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen, camera):
        sprite_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        draw_rect = camera.apply(sprite_rect)

        screen.blit(self.frames[self.current_frame], draw_rect)

class Platform:

    def __init__(self, x, y, width, height, platform_type="normal", image_path="Assets/Platform.png"):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = platform_type
        self.original_x = x
        self.original_y = y

        self.move_speed = 2
        self.move_range = 100
        self.move_direction = 1
        self.vel_x = 0
        self.vel_y = 0

        self.load_image(image_path)

    def load_image(self, path):
        try:
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        except:
            print(f"Could not load image: {path}")
            self.image = None

    def update(self):
        self.vel_x = self.vel_y = 0

        if self.type == "moving_vertical":
            self.vel_y = self.move_speed * self.move_direction
            self.rect.y += self.vel_y
            if abs(self.rect.y - self.original_y) > self.move_range:
                self.move_direction *= -1

        elif self.type == "moving_horizontal":
            self.vel_x = self.move_speed * self.move_direction
            self.rect.x += self.vel_x
            if abs(self.rect.x - self.original_x) > self.move_range:
                self.move_direction *= -1

    def draw(self, screen, camera):
        draw_rect = camera.apply(self.rect)

        screen.blit(self.image, draw_rect)

class HealthBar:

    def __init__(self, heart_path="Assets/Heart.png"):
        self.heart_image = None
        self.heart_size = 40
        self.heart_spacing = 10
        self.max_hearts = 10
        self.load_heart(heart_path)

    def load_heart(self, path):
        try:
            self.heart_image = pygame.image.load(path).convert_alpha()
            self.heart_image = pygame.transform.scale(self.heart_image, (self.heart_size, self.heart_size))
        except Exception as e:
            print(f"Could not load heart image: {path}, Error: {e}")
            self.heart_image = None

    def draw(self, screen, health):
        hearts_to_show = max(0, health // 20)

        start_x = 20
        start_y = 20

        for i in range(self.max_hearts):
            x_pos = start_x + i * (self.heart_size + self.heart_spacing)

            if self.heart_image:
                if i < hearts_to_show:
                    screen.blit(self.heart_image, (x_pos, start_y))
                else:
                    grayed_heart = self.heart_image.copy()
                    grayed_heart.set_alpha(50)
                    screen.blit(grayed_heart, (x_pos, start_y))
            else:
                if i < hearts_to_show:
                    pygame.draw.rect(screen, (255, 0, 0), (x_pos, start_y, self.heart_size, self.heart_size))
                else:
                    pygame.draw.rect(screen, (100, 100, 100), (x_pos, start_y, self.heart_size, self.heart_size))

class GameLoop:

    def __init__(self, background_path="Assets/Background.png", damage_background_path="Assets/Background2.png"):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.platforms, self.saws = self.create_level()

        self.player = Player(200, 300)
        self.player.set_game_loop(self)
        self.camera = Camera()

        self.background = None
        self.damage_background = None

        self.health_bar = HealthBar()

        self.load_background(background_path)
        self.load_damage_background(damage_background_path)

        self.flash_background_timer = 0
        self.flash_background_duration = 10
        self.flash_interval = 10

        self.font_large = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 36)

    def load_damage_background(self, path):
        try:
            self.damage_background = pygame.image.load(path).convert()
            self.damage_background = pygame.transform.scale(self.damage_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            print(f"Damage Background loaded: {path}")
        except Exception as e:
            print(f"Could not load damage background: {path}, Error: {e}")
            self.damage_background = None

    def trigger_background_flash(self):
        self.flash_background_timer = self.flash_background_duration

    def load_background(self, path):
        try:
            self.background = pygame.image.load(path).convert()
            print(f"Background loaded: {path}")
        except Exception as e:
            print(f"Could not load background: {path}, Error: {e}")
            self.background = None

    def create_level(self):
        saws = []
        platforms = []

        platforms.append(Platform(50, 400, 300, 40))

        platforms.append(Platform(500, 400, 300, 40))

        platforms.append(Platform(-300, 400, 200, 40))

        platforms.append(Platform(-600, 350, 200, 40))

        platforms.append(Platform(-900, 300, 200, 40))

        saws.append(Saw(600, 300))

        saws.append(Saw(400, 300))

        moving_vert_1 = Platform(200, 200, 100, 20, "moving_vertical")
        moving_vert_1.move_range = 150
        moving_vert_1.move_speed = 3
        platforms.append(moving_vert_1)

        platforms.append(Platform(50, 150, 200, 40))

        moving_horiz_1 = Platform(350, 100, 100, 20, "moving_horizontal")
        moving_horiz_1.move_range = 250
        moving_horiz_1.move_speed = 3
        platforms.append(moving_horiz_1)

        platforms.append(Platform(700, 100, 80, 20))

        saws.append(Saw(700, -100))

        platforms.append(Platform(950, 50, 50, 40))

        moving_vert_2 = Platform(1100, -50, 70, 30, "moving_vertical")
        moving_vert_2.move_range = 100
        moving_vert_2.move_speed = 3
        platforms.append(moving_vert_2)

        saws.append(Saw(1100, 200))

        platforms.append(Platform(900, -150, 200, 40))

        moving_horiz_2 = Platform(700, -250, 120, 20, "moving_horizontal")
        moving_horiz_2.move_range = 150
        moving_horiz_2.move_speed = 2
        platforms.append(moving_horiz_2)

        saws.append(Saw(400, -300))

        platforms.append(Platform(350, -350, 100, 20))

        platforms.append(Platform(600, -400, 100, 20))

        saws.append(Saw(250, -450))

        moving_horiz_3 = Platform(400, -500, 150, 20, "moving_horizontal")
        moving_horiz_3.move_range = 350
        moving_horiz_3.move_speed = 4
        platforms.append(moving_horiz_3)

        platforms.append(Platform(800, -550, 70, 20))

        platforms.append(Platform(950, -550, 300, 20))

        moving_saw_1 = Saw(1000, -400)
        saws.append(moving_saw_1)

        moving_vert_3 = Platform(1300, -600, 80, 20, "moving_vertical")
        moving_vert_3.move_range = 50
        moving_vert_3.move_speed = 2
        platforms.append(moving_vert_3)

        moving_vert_4 = Platform(1450, -650, 80, 20, "moving_vertical")
        moving_vert_4.move_range = 50
        moving_vert_4.move_speed = 2
        platforms.append(moving_vert_4)

        platforms.append(Platform(1600, -750, 50, 20))

        platforms.append(Platform(1700, -800, 50, 20))

        saws.append(Saw(1600, -700))

        platforms.append(Platform(1000, -900, 600, 40))

        moving_horiz_4 = Platform(900, -980, 100, 20, "moving_horizontal")
        moving_horiz_4.move_range = 100
        moving_horiz_4.move_speed = 1
        platforms.append(moving_horiz_4)

        moving_vert_5 = Platform(750, -1100, 100, 20, "moving_vertical")
        moving_vert_5.move_range = 150
        moving_vert_5.move_speed = 3
        platforms.append(moving_vert_5)

        # --- NEW CHALLENGES ADDED BELOW ---

        platforms.append(Platform(500, -1250, 300, 40))

        platforms.append(Platform(350, -1300, 100, 40))

        saws.append(Saw(550, -1350))

        moving_horiz_5 = Platform(300, -1400, 100, 20, "moving_horizontal")
        moving_horiz_5.move_range = 250
        moving_horiz_5.move_speed = 3
        platforms.append(moving_horiz_5)

        moving_vert_6 = Platform(100, -1600, 80, 20, "moving_vertical")
        moving_vert_6.move_range = 150
        moving_vert_6.move_speed = 3
        platforms.append(moving_vert_6)
#1
        platforms.append(Platform(350, -1650, 100, 20))

        platforms.append(Platform(450, -1650, 100, 20))

        saws.append(Saw(600, -1650))

        platforms.append(Platform(750, -1700, 50, 20))

        moving_horiz_6 = Platform(850, -1750, 120, 20, "moving_horizontal")
        moving_horiz_6.move_range = 200
        moving_horiz_6.move_speed = 2
        platforms.append(moving_horiz_6)

        saws.append(Saw(900, -1850))

        platforms.append(Platform(950, -1800, 200, 40))

        platforms.append(Platform(1100, -1900, 100, 40))

        moving_vert_7 = Platform(1250, -2000, 70, 20, "moving_vertical")
        moving_vert_7.move_range = 100
        moving_vert_7.move_speed = 3
        platforms.append(moving_vert_7)

        platforms.append(Platform(1400, -2150, 80, 20))

        platforms.append(Platform(1600, -2250, 150, 20))

        saws.append(Saw(1500, -2250))

        moving_horiz_7 = Platform(1800, -2300, 100, 20, "moving_horizontal")
        moving_horiz_7.move_range = 200
        moving_horiz_7.move_speed = 3
        platforms.append(moving_horiz_7)

        platforms.append(Platform(2100, -2400, 50, 20))

        return platforms, saws

    def restart_game(self):
        self.game_over = False
        self.platforms, self.saws = self.create_level()
        self.player = Player(200, 300)
        self.player.set_game_loop(self)
        self.camera = Camera()

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font_large.render("GAME OVER", True, (255, 50, 50))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)

        restart_text = self.font_small.render("Press R to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(restart_text, restart_rect)

        quit_text = self.font_small.render("Press ESC to Quit", True, (200, 200, 200))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
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

        self.health_bar.draw(self.screen, self.player.health)

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
        self.player.handle_input(keys)
        self.player.update(self.platforms)
        self.player.check_saw_collision(self.saws)
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

        pygame.quit()

game = GameLoop()
game.run()