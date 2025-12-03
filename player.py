import pygame

from constants import GRAVITY, FALL_SPEED
from entities import Projectile
from functions import update_animation_frame, load_sprite_sheet

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

        self.projectiles = []
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 20
        self.ammo = 30
        self.max_ammo = 30
        self.frog = 0
        self.score = 0

        self.animation_speeds = {
            'idle': 15,
            'walk_right': 8,
            'walk_left': 8,
            'jump': 12,
            'fall': 12
        }

        self.load_player_assets(sprite_sheet_path)

        self.damage_sound = None
        self.collection_sound = None
        self.shoot_sound = None
        self.load_sounds()

    def set_game_loop(self, game_loop_instance):
        self.game_loop = game_loop_instance

    def load_sounds(self):
        self.damage_sound = pygame.mixer.Sound("Assets/damage.wav")
        self.damage_sound.set_volume(0.2)
        self.collection_sound = pygame.mixer.Sound("Assets/collection.wav")
        self.collection_sound.set_volume(1.5)
        self.shoot_sound = pygame.mixer.Sound("Assets/shoot.wav")
        self.shoot_sound.set_volume(1.5)

    def load_player_assets(self, path, frame_width=32, frame_height=32,
                           idle_frames=2, walk_frames=3, jump_frames=2):

        total_frames = idle_frames + walk_frames + jump_frames

        all_frames = load_sprite_sheet(
            path,
            frame_width,
            frame_height,
            total_frames,
            scale_width=self.width,
            scale_height=self.height
        )

        current_index = 0

        self.animations['idle'] = all_frames[current_index: current_index + idle_frames]
        current_index += idle_frames

        self.animations['walk_right'] = all_frames[current_index: current_index + walk_frames]
        current_index += walk_frames

        self.animations['jump'] = all_frames[current_index: current_index + jump_frames]
        current_index += jump_frames

        for frame in self.animations['walk_right']:
            flipped = pygame.transform.flip(frame, True, False)
            self.animations['walk_left'].append(flipped)

        if self.animations['jump']:
            self.animations['fall'] = [self.animations['jump'][-1]]

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

            self.current_frame, self.frame_counter = update_animation_frame(
                self.current_frame,
                self.frame_counter,
                1 / current_speed,
                len(frames)
            )

    def draw(self, screen, camera):
        sprite_rect = pygame.Rect(
            self.rect.x - (self.width - self.hitbox_width) // 2,
            self.rect.y - (self.height - self.hitbox_height) // 2,
            self.width,
            self.height
        )
        draw_rect = camera.apply(sprite_rect)

        if self.animations[self.current_animation] and \
                len(self.animations[self.current_animation]) > 0:
            frames = self.animations[self.current_animation]

            if self.current_frame >= len(frames):
                self.current_frame = 0

            current_surface = frames[self.current_frame]
            screen.blit(current_surface, draw_rect)
        else:
            pygame.draw.rect(screen, (100, 100, 200), draw_rect)

        for projectile in self.projectiles:
            projectile.draw(screen, camera)

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed

        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) \
                and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            self.on_moving_platform = None

        if keys[pygame.K_x]:
            self.shoot()

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            projectile_x = self.rect.centerx
            projectile_y = self.rect.centery
            direction = 1 if self.facing_right else -1
            self.projectiles.append(Projectile(projectile_x, projectile_y, direction))
            self.shoot_cooldown = self.shoot_cooldown_max
            self.ammo -= 1
            self.shoot_sound.play()

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

        if not self.on_moving_platform:
            self.on_moving_platform = None

        ground_tolerance = 10

        for platform in platforms:
            if not self.rect.colliderect(platform.rect):
                continue

            if self.vel_y >= 0:
                if self.rect.bottom <= platform.rect.top + ground_tolerance + abs(self.vel_y):
                    self.rect.bottom = platform.rect.top
                    self.y = self.rect.y
                    self.vel_y = 0
                    self.on_ground = True

                    if platform.type == "win":
                        if self.game_loop:
                            self.game_loop.trigger_victory()
                        return

                    if platform.type in ("moving_vertical", "moving_horizontal"):
                        self.on_moving_platform = platform
                    else:
                        self.on_moving_platform = None
                    return

            elif self.vel_y < 0:
                if self.rect.top < platform.rect.bottom:
                    self.rect.top = platform.rect.bottom
                    self.y = self.rect.y
                    self.vel_y = 0

    def update(self, platforms):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
            if self.damage_cooldown == 0:
                self.invincible = False

        if self.on_moving_platform:
            if (self.rect.right > self.on_moving_platform.rect.left and
                    self.rect.left < self.on_moving_platform.rect.right):

                self.x += self.on_moving_platform.vel_x
                self.y += self.on_moving_platform.vel_y
            else:
                self.on_moving_platform = None

        if not self.on_ground:
            self.vel_y = min(self.vel_y + GRAVITY, FALL_SPEED)

        self.y += self.vel_y
        self.rect.y = round(self.y)
        self.check_collision_y(platforms)

        self.x += self.vel_x
        self.rect.x = round(self.x)
        self.check_collision_x(platforms)

        if self.y >= 1000:
            self.health -= 100
        if self.health <= 0:
            self.player_dead = True

        self.update_animation()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def check_saw_collision(self, saws):
        if self.invincible:
            return

        for saw in saws:
            if self.rect.colliderect(saw.rect):
                self.health -= 20
                self.damage_cooldown = self.damage_cooldown_max
                self.invincible = True
                self.damage_sound.play()
                if self.game_loop:
                    self.game_loop.trigger_background_flash()
                break

    def check_enemy_collision(self, enemies):
        if self.invincible:
            return

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.health -= 20
                self.damage_cooldown = self.damage_cooldown_max
                self.invincible = True
                self.damage_sound.play()
                if self.game_loop:
                    self.game_loop.trigger_background_flash()
                break

    def check_heart_item_collision(self, heart_items):
        for heart_item in heart_items:
            if self.rect.colliderect(heart_item.rect):
                self.health = min(self.health + 20, 200)
                heart_items.remove(heart_item)
                self.collection_sound.play()
                break

    def check_projectile_collisions(self, enemies):
        for projectile in self.projectiles[:]:
            for enemy in enemies:
                if projectile.rect.colliderect(enemy.rect):
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    enemy.health -= 20
                    if enemy.health <= 0 and enemy in enemies:
                        enemies.remove(enemy)
                        self.score += 1
                        if self.game_loop:
                            self.game_loop.trigger_score_event()
                    break

    def check_ammo_item_collision(self, ammo_items):
        for ammo_item in ammo_items[:]:
            if self.rect.colliderect(ammo_item.rect):
                self.ammo = min(self.ammo + ammo_item.ammo_amount, self.max_ammo)
                ammo_items.remove(ammo_item)
                self.collection_sound.play()
                break