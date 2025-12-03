import pygame
from functions import load_image, load_sprite_sheet, update_animation_frame
from constants import SCREEN_WIDTH

class Projectile:
    def __init__(self, x, y, direction, image_path="Assets/Ammo.png"):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 8
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 10
        self.direction = direction
        self.color = (255, 255, 0)
        self.image = load_image(image_path, self.width, self.height)

    def update(self):
        self.x += self.speed * self.direction
        self.rect.x = self.x

    def draw(self, screen, camera):
        sprite_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        draw_rect = camera.apply(sprite_rect)
        screen.blit(self.image, draw_rect)

    def is_off_screen(self, camera):
        if camera is None:
            return False
        distance = abs(self.x - (camera.offset_x + SCREEN_WIDTH // 2))
        return distance > SCREEN_WIDTH * 2


class Saw:
    def __init__(self, x, y, sprite_sheet_path="Assets/Saw.png"):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.hitbox_width = 70
        self.hitbox_height = 70
        self.rect = pygame.Rect(
            x + (self.width - self.hitbox_width) // 2,
            y + (self.height - self.hitbox_height) // 2,
            self.hitbox_width,
            self.hitbox_height
        )

        self.sprite_sheet = None
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.5
        self.frame_counter = 0

        self.load_sprite_sheet(sprite_sheet_path)

    def load_sprite_sheet(self, path, frame_width=32, frame_height=32, num_frames=4):
        self.frames = load_sprite_sheet(
            path,
            frame_width,
            frame_height,
            num_frames,
            scale_width=self.width,
            scale_height=self.height
        )

    def update(self):
        if self.frames:
            self.current_frame, self.frame_counter = update_animation_frame(
                self.current_frame,
                self.frame_counter,
                self.animation_speed,
                len(self.frames)
            )

    def draw(self, screen, camera):
        sprite_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        draw_rect = camera.apply(sprite_rect)
        screen.blit(self.frames[self.current_frame], draw_rect)


class Enemy:
    def __init__(self, x, y, sprite_sheet_path="Assets/Enemy.png"):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 60
        self.hitbox_width = 70
        self.hitbox_height = 60
        self.rect = pygame.Rect(
            x + (self.width - self.hitbox_width) // 2,
            y + (self.height - self.hitbox_height) // 2,
            self.hitbox_width,
            self.hitbox_height
        )
        self.original_x = x
        self.original_y = y

        self.move_speed = 2
        self.move_range = 100
        self.move_direction = 1
        self.vel_x = 0
        self.vel_y = 0

        self.sprite_sheet = None
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.5
        self.frame_counter = 0

        self.health = 60

        self.load_sprite_sheet(sprite_sheet_path)

    def load_sprite_sheet(self, path, frame_width=32, frame_height=21, num_frames=4):
        self.frames = load_sprite_sheet(
            path,
            frame_width,
            frame_height,
            num_frames,
            scale_width=self.width,
            scale_height=self.height
        )

    def update(self):
        self.vel_x = self.vel_y = 0
        self.vel_x = self.move_speed * self.move_direction
        self.rect.x += self.vel_x
        if abs(self.rect.x - self.original_x) > self.move_range:
            self.move_direction *= -1
        if self.frames:
            self.current_frame, self.frame_counter = update_animation_frame(
                self.current_frame,
                self.frame_counter,
                self.animation_speed,
                len(self.frames)
            )

    def draw(self, screen, camera):
        sprite_rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)
        draw_rect = camera.apply(sprite_rect)
        screen.blit(self.frames[self.current_frame], draw_rect)


class Platform:
    def __init__(self, x, y, width, height, platform_type="normal",
                 image_path="Assets/Platform.png"):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = platform_type
        self.original_x = x
        self.original_y = y

        self.move_speed = 2
        self.move_range = 100
        self.move_direction = 1
        self.vel_x = 0
        self.vel_y = 0
        self.image = None
        self.load_image(image_path)

    def load_image(self, path):
        self.image = load_image(path, self.rect.width, self.rect.height)

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