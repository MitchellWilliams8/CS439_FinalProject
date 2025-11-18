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
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.on_ground = False
        self.jump_power = -15
        self.on_moving_platform = None
        self.health = 100
        self.player_dead = False
        self.facing_right = True

        self.sprite_sheet = None
        self.animations = {
            'idle': [],
            'walk_right': [],
            'walk_left': [],
            'jump': [],
            'fall': []
        }
        self.current_animation = 'idle'
        self.current_frame = 0
        self.frame_counter = 0

        self.animation_speeds = {
            'idle': 15,
            'walk_right': 8,
            'walk_left': 8,
            'jump': 12,
            'fall': 12
        }

        self.load_sprite_sheet(sprite_sheet_path)

    def load_sprite_sheet(self, path, frame_width=32, frame_height=32,
                          idle_frames=2, walk_frames=3, jump_frames=2):
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
        draw_rect = camera.apply(self.rect)

        if self.animations[self.current_animation] and len(self.animations[self.current_animation]) > 0:
            frames = self.animations[self.current_animation]

            if self.current_frame >= len(frames):
                self.current_frame = 0

            screen.blit(frames[self.current_frame], draw_rect)
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
        for saw in saws:
            if self.rect.colliderect(saw.rect):
                self.health -= 20

    def update(self, platforms):
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
        self.rect = pygame.Rect(x, y, self.width, self.height)

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
        draw_rect = camera.apply(self.rect)

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

class GameLoop:

    def __init__(self, background_path="Assets/Background.png"):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("")
        self.clock = pygame.time.Clock()
        self.running = True
        self.platforms, self.saws = self.create_level()

        self.player = Player(200, 300)

        self.camera = Camera()

        self.background = None

        self.load_background(background_path)

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

        platforms.append(Platform(900, 350, 200, 40))
        platforms.append(Platform(1200, 300, 200, 40))
        platforms.append(Platform(1400, 250, 200, 40))
        platforms.append(Platform(1500, 200, 200, 40))

        platforms.append(Platform(-300, 400, 200, 40))
        platforms.append(Platform(-600, 350, 200, 40))
        platforms.append(Platform(-900, 300, 200, 40))

        moving_vert = Platform(200, 200, 100, 20, "moving_vertical")
        moving_vert.move_range = 120
        platforms.append(moving_vert)

        moving_horiz = Platform(400, 300, 100, 20, "moving_horizontal")
        moving_horiz.move_range = 150
        platforms.append(moving_horiz)

        saws.append(Saw(600, 300))
        saws.append(Saw(400, 300))

        return platforms, saws

    def draw(self):
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

        pygame.display.flip()

    def update(self):
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
            self.running = False

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