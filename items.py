import pygame
from functions import load_image, create_centered_rect


class HeartItem:
    def __init__(self, x, y, image_path="Assets/Heart.png"):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.hitbox_width = 30
        self.hitbox_height = 30
        self.rect = create_centered_rect(
            x, y, self.width, self.height,
            self.hitbox_width, self.hitbox_height
        )
        self.image = load_image(image_path, self.hitbox_width, self.hitbox_height)

    def draw(self, screen, camera):
        sprite_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        draw_rect = camera.apply(sprite_rect)
        screen.blit(self.image, draw_rect)


class AmmoItem:
    def __init__(self, x, y, image_path="Assets/Ammo.png"):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.hitbox_width = 40
        self.hitbox_height = 40
        self.rect = pygame.Rect(
            x + (self.width - self.hitbox_width) // 2,
            y + (self.height - self.hitbox_height) // 2,
            self.hitbox_width,
            self.hitbox_height
        )
        self.ammo_amount = 10
        self.image = None
        self.load_image(image_path)

    def load_image(self, path):
        self.image = load_image(path, self.rect.width, self.rect.height)
        if self.image is None:
            print(f"Could not load image for AmmoItem: {path}")

    def draw(self, screen, camera):
        sprite_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        draw_rect = camera.apply(sprite_rect)
        screen.blit(self.image, draw_rect)