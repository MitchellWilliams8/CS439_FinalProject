import pygame
from constants import SCREEN_WIDTH
from functions import load_image

class HealthBar:
    def __init__(self, heart_path="Assets/Heart.png"):
        self.heart_size = 40
        self.heart_spacing = 10
        self.max_hearts = 10
        self.heart_image = load_image(heart_path, self.heart_size, self.heart_size)

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
                    pygame.draw.rect(
                        screen, (255, 0, 0),
                        (x_pos, start_y, self.heart_size, self.heart_size)
                    )
                else:
                    pygame.draw.rect(
                        screen, (100, 100, 100),
                        (x_pos, start_y, self.heart_size, self.heart_size)
                    )

class ScoreDisplay:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.color = (255, 255, 255)

    def draw(self, screen, score):
        score_surface = self.font.render(f"Score: {score}", True, self.color)
        screen.blit(score_surface, (20, 70))

class FrogDisplay:
    def __init__(self, image_path="Assets/Frog.png"):
        self.frog_size = 100
        self.original_image = load_image(image_path, self.frog_size, self.frog_size)
        self.angle = 0
        self.rotation_speed = 40
        self.remaining_rotation = 0

    def trigger_rotation(self):
        self.remaining_rotation += 2000

    def reset(self):
        self.angle = 0
        self.remaining_rotation = 0

    def draw(self, screen):
        if self.remaining_rotation > 0:
            rotate_amount = min(self.rotation_speed, self.remaining_rotation)
            self.angle = (self.angle - rotate_amount) % 360
            self.remaining_rotation -= rotate_amount

        if self.original_image:
            rotated_image = pygame.transform.rotate(self.original_image, self.angle)
            center_pos = (60, 180)
            new_rect = rotated_image.get_rect(center=center_pos)
            screen.blit(rotated_image, new_rect)
        else:
            pygame.draw.rect(screen, (0, 255, 0), (20, 130, self.frog_size, self.frog_size))

class AmmoDisplay:
    def __init__(self, ammo_path="Assets/Ammo.png"):
        self.ammo_image = None
        self.ammo_size = 30
        self.ammo_spacing = 5
        self.max_ammo = 30
        self.load_ammo(ammo_path)

    def load_ammo(self, path):
        try:
            self.ammo_image = pygame.image.load(path).convert_alpha()
            self.ammo_image = pygame.transform.scale(
                self.ammo_image, (self.ammo_size, self.ammo_size)
            )
        except Exception as e:
            print(f"Could not load ammo image: {path}, Error: {e}")
            self.ammo_image = None

    def draw(self, screen, ammo):
        ammo_to_show = max(0, ammo)
        start_x = SCREEN_WIDTH - 350
        start_y = 20

        icons_per_row = 10
        row_height = self.ammo_size + 5

        for i in range(self.max_ammo):
            row = i // icons_per_row
            col = i % icons_per_row

            x_pos = start_x + col * (self.ammo_size + self.ammo_spacing)
            y_pos = start_y + row * row_height

            if self.ammo_image:
                if i < ammo_to_show:
                    screen.blit(self.ammo_image, (x_pos, y_pos))
                else:
                    grayed_ammo = self.ammo_image.copy()
                    grayed_ammo.set_alpha(50)
                    screen.blit(grayed_ammo, (x_pos, y_pos))
            else:
                if i < ammo_to_show:
                    pygame.draw.rect(
                        screen, (255, 0, 0),
                        (x_pos, y_pos, self.ammo_size, self.ammo_size)
                    )
                else:
                    pygame.draw.rect(
                        screen, (100, 100, 100),
                        (x_pos, y_pos, self.ammo_size, self.ammo_size)
                    )