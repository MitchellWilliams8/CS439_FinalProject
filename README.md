# Wizard Frog

**Wizard Frog** is a 2D vertical scrolling platformer written in Python using the Pygame library. The player navigates across moving platforms dodging obstacles and fighting enemies to reach the top.

## Overview

- **Win Condition:** Reach the platform at the top of the map with a score of 4 or higher.
- **Lose Condition:** The game ends if the player's health drops to 0 or if the player falls off the bottom of the screen.

## Key Features

- **Physics:** Gravity, max fall speed, and momentum based movement.
- **Sprite Animation:** Frame based animation for the player when idle, walking, and jumping and looping animations for enemy and obstacle movement.
- **Camera:** A camera that keeps the player centered by calculating coordinate offsets.
- **Combat System:**
    - Projectile shooting with cooldowns.
    - Limited ammo.
    - Enemy hit detection.
* **Level Elements:**
    - **Moving Platforms:** Horizontal and vertical moving platforms that have a movement range and speed.
    - **Obstacles:** Animated rotating saws and moving enemies.
- **UI:** Displays health, ammo count, score, and a display that rotates when score is increased.

## Installation & Prerequisites

### 1. Requirements
- **Python**
- **Pygame library**

### 2. Setup Instructions
1.  **Clone the repository**
2.  **Ensure Pygame is installed** 
3.  **Check that all necessary assets are present**
4.  **Launch the game**

## Controls

This game supports keyboard input. Input handling is processed in player.py and game_loop.py.

- **Move Left** | Left Arrow | A | Move character left.
- **Move Right** | Right Arrow | D | Move character right.
- **Jump** | Spacebar | W | Up Arrow | Initiate jump.
- **Shoot** | X | Fire projectile.
- **Start Game** | Spacebar | Begins game from start screen.
- **Restart** | R | Resets level on win/loss screens.
- **Quit** | ESC | Exits the application.

## Gameplay Mechanics

### 1. Health & Damage
- **Starting Health:** 100 HP (Represented by 5 hearts in the UI; 1 heart = 20 HP).
- **Taking Damage:** Colliding with a saw or enemy deals 20 damage.
- **Invincibility Frames:** After taking damage, the player becomes invincible for 60 frames to prevent instant death.
- **Visual Feedback:** The background flashes to an alternate background when damage is taken.
- **Audio Feedback:** A sound effect plays when taking damage.

### 2. Items & Collectibles
- **Hearts:** Restore 20 HP (up to a max of 200 HP).
- **Ammo Items:** Restore 10 Ammo (up to a max of 30).
- **Collection Audio:** A sound effect plays upon item pickup.

### 3. Combat & Scoring
- **Shooting:** There is a short cooldown (20 frames) between shots.
- **Enemies:** Enemies traverse a fixed horizontal range. Enemies have 60 HP.
- **Damage Logic:** Player projectiles deal 20 damage to enemies.
- **Score:** Defeating an enemy awards 1 point. You must collect at least 4 points to trigger the win condition at the end of the level.

### 4. Moving Platforms
When on a moving platform the player's x coordinate is updated by the platform's velocity, preventing them from sliding off.

## Project Structure & File Descriptions

### main.py
The entry point of the game.
- **Initialization:** Instantiates the GameLoop class.
- **Execution:** Triggers the main application loop via .run().

### game_loop.py
The core of the game.
- **Main Loop:** Manages the primary while self.running: loop, clock ticking, and event handling.
- **State Management:** Tracks game states using booleans (game_started, game_over, game_won) to switch between the start screen, gameplay, and end screen overlays.
- **Rendering:** Clears the screen, handles background drawing, and calls .draw() for all entities.
- **Audio:** Initializes a 64 channel mixer for sound layering and loops background music.

### level.py
Sets up the level.
- **Instantiation:** Contains the create_level() function. It manually instantiates every Platform, Enemy, Saw, and Item with specific x, y coordinates and properties.

### player.py
The logic for the user controlled character.
- **Physics:** Implements gravity, fall speed, and jumping.
- **Separated Collision:** Handles x and y collisions independently to prevent sticking to platforms. It allows the player to stand on moving platforms by transferring the platform's velocity to the player.
- **Animation State Machine:** Uses a dictionary to store lists of frames (idle, walk_right, jump). It automatically switches states based on velocity and ground status.
- **Combat Logic:** Manages projectile shooting, ammo amount, and cooldowns after taking damage.

### entities.py
All dynamic non player objects.
* **Platform:** Supports three behavior types:
    - **Normal:** Static ground.
    - **Moving (Vertical/Horizontal):** Reverses direction when the object travels a set distance (move_range) from its origin.
    - **Win:** Triggers the victory condition upon collision.
- **Enemy:** Traverses a fixed horizontal range. Cycles through animation frames.
- **Saw:** Cycles through animation frames to simulate spinning.
- **Projectile:** Moves horizontally based on direction of the player and gets removed when it leaves the camera view.

### items.py
All collectible items.
- **HeartItem / AmmoItem:** Collectible sprites. Use a hitbox that allows the player to pick up the item on contact.

### camera.py
Keeps the player in view.
- **Logic:** Calculates an offset_x and offset_y based on the difference between the player's center and the screen's center.
- **Coordinate Transformation:** The .apply(rect) method takes an object's world coordinates and converts them to screen coordinates for drawing, creating the scrolling effect.

### ui.py
Manages the display elements.
- **HealthBar:** Shows player health. It calculates how many hearts to show based on health // 20 and draws empty (grayed out) hearts for missing health.
- **AmmoDisplay:** Shows a grid of bullet icons. It uses rows and columns to stack icons neatly and lowers the transparency of used ammo slots.
- **FrogDisplay:** A display that rotates when score increases.

### functions.py
A library of static helper methods.
- **load_sprite_sheet:** Iterates through a main image file, extracting frames to create a list of animation frames.
- **update_animation_frame:** A utility that increments a floating point counter. When the counter exceeds 1, it advances the frame index, separating animation speed from the game's framerate.

### constants.py
Constants for the game.
- Centralizes constants like SCREEN_WIDTH, SCREEN_HEIGHT, FPS, and GRAVITY to make global tuning easier.

## Asset Requirements

To run successfully, the Assets/ folder must contain:

- Player.png - Main character sprite sheet. 
- Enemy.png - Enemy sprite sheet. 
- Saw.png - Hazard sprite sheet. 
- Platform.png - Ground texture. 
- Heart.png - Health item and UI icon. 
- Ammo.png - Ammo item and UI icon, projectile sprite. 
- Background.png - Main level background. 
- Background2.png - Alternate background for damage. 
- Frog.png - UI element. 
- damage.wav - Sound effect. 
- shoot.wav - Sound effect. 
- collection.wav - Sound effect. 
- background_music.mp3 - Music track. 
- ShinyEyes-prr1.ttf - Custom font file. 

