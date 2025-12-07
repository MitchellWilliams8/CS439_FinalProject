from entities import *
from items import *

def create_level():
    saws = []
    platforms = []
    heart_items = []
    enemies = []
    ammo_items = []

    platforms.append(Platform(50, 400, 300, 40))

    enemy1 = Enemy(50, 250)
    enemy1.move_range = 250
    enemy1.move_speed = 3
    enemies.append(enemy1)

    enemy2 = Enemy(1000, -800)
    enemy2.move_range = 550
    enemy2.move_speed = 5
    enemies.append(enemy2)

    enemy3 = Enemy(300, -1400)
    enemy3.move_range = 350
    enemy3.move_speed = 2
    enemies.append(enemy3)

    enemy4 = Enemy(2000, -2300)
    enemy4.move_range = 1150
    enemy4.move_speed = 3
    enemies.append(enemy4)

    enemy5 = Enemy(700, 0)
    enemy5.move_range = 100
    enemy5.move_speed = 6
    enemies.append(enemy5)

    ammo_items.append(AmmoItem(-230, 350))

    ammo_items.append(AmmoItem(-530, 300))

    heart_items.append(HeartItem(-820, 250))

    heart_items.append(HeartItem(400, 250))

    platforms.append(Platform(500, 400, 300, 40))

    platforms.append(Platform(-300, 400, 200, 40))

    platforms.append(Platform(-600, 350, 200, 40))

    platforms.append(Platform(-900, 300, 200, 40))

    saws.append(Saw(600, 300))

    saws.append(Saw(370, 300))

    moving_vert_1 = Platform(200, 220, 90, 40, "moving_vertical")
    moving_vert_1.move_range = 80
    moving_vert_1.move_speed = 2
    platforms.append(moving_vert_1)

    platforms.append(Platform(50, 150, 150, 40))

    moving_horiz_1 = Platform(450, 100, 100, 20, "moving_horizontal")
    moving_horiz_1.move_range = 150
    moving_horiz_1.move_speed = 3
    platforms.append(moving_horiz_1)

    platforms.append(Platform(700, 100, 80, 20))

    saws.append(Saw(700, -100))

    platforms.append(Platform(950, 50, 50, 40))

    moving_vert_2 = Platform(1100, -50, 70, 40, "moving_vertical")
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

    platforms.append(Platform(500, -1250, 200, 40))

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

    winning_platform = Platform(2100, -2400, 50, 20, "win")
    platforms.append(winning_platform)

    return platforms, saws, heart_items, enemies, ammo_items