import pygame

def load_image(path, width=None, height=None, convert_alpha=True):
    if convert_alpha:
        image = pygame.image.load(path).convert_alpha()
    else:
        image = pygame.image.load(path).convert()

    if width and height:
        image = pygame.transform.scale(image, (width, height))

    return image

def load_sprite_sheet(path, frame_width, frame_height, num_frames,
                      scale_width=None, scale_height=None):
    frames = []

    sprite_sheet = pygame.image.load(path).convert_alpha()

    for i in range(num_frames):
        frame_x = i * frame_width
        frame = sprite_sheet.subsurface(
            pygame.Rect(frame_x, 0, frame_width, frame_height)
        )

        if scale_width and scale_height:
            frame = pygame.transform.scale(frame, (scale_width, scale_height))

        frames.append(frame)

    return frames

def create_centered_rect(x, y, sprite_width, sprite_height,
                         hitbox_width, hitbox_height):
    offset_x = (sprite_width - hitbox_width) // 2
    offset_y = (sprite_height - hitbox_height) // 2
    return pygame.Rect(x + offset_x, y + offset_y, hitbox_width, hitbox_height)

def update_animation_frame(current_frame, frame_counter, animation_speed, num_frames):
    frame_counter += animation_speed
    if frame_counter >= 1:
        frame_counter = 0
        current_frame = (current_frame + 1) % num_frames

    return current_frame, frame_counter

def load_sound(path, volume=1.0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    return sound