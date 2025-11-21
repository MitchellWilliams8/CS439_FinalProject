from constants import *
import pygame

class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0

    def apply(self, rect):
        return pygame.Rect(rect.x - self.offset_x, rect.y - self.offset_y, rect.width, rect.height)

    def update(self, target):
        self.offset_x = target.rect.centerx - SCREEN_WIDTH // 2
        self.offset_y = target.rect.centery - SCREEN_HEIGHT // 2