#!/usr/bin/env python3

import pygame

pygame.init()

TITLE = "Name of Game"
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60
GRID_SIZE = 64

class TextBlitter():
    def __init__(self):
        pass

    def do_something(self, screen):
        pass

class ImageManager():
    def __init__(self):
        pass

    def load_image(self):
        pass

class SoundManager():
    def __init__(self):
        self.muted = False

    def toggle_mute(self):
        self.muted = not self.muted

    def play_sound(self):
        pass

    def play_music(self):
        pass

class Physics():
    def __init(self, gravity, terminal_velocity):
        self.gravity = gravity
        self.terminal_velocity = terminal_velocity

    def apply_gravity(entity):
        entity.vy += self.gravity
        entity.vy = min(self.gravity, self.terminal_velocity)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pass

    def is_near(self, hero):
        pass

    def update(self):
        pass

class Hero(Entity):
    def __init__(self):
        pass

    def check_level_boundaries(self, level):
        pass

    def move_and_process_blocks(self, blocks):
        pass

    def process_items(self):
        pass

    def process_enemies(self):
        pass

    def update(self, level):
        level.physics_engine.apply_gravity(self)
        check_level_boundaries(level)
        move_and_process_blocks(level.blocks)
        process_items(level.items)
        process_enemies(level.enemies)

class Enemy(Entity):

    def __init__(self, animation_frames):
        pass

    def reverse(self):
        pass

    def update(self, level, hero):
        pass

class Block(Entity):
    def __init__(self):
        pass

class Item(Entity):
    def __init__(self, value=0):
        value = self.value

    def apply(self, character):
        pass

    def update(self):
        pass

class Level():
    def __init__(self, level_file):
        self.level_file = level_file

    def load(self):
        self.physics_engine = Physics(5, 32)

    def reset(self):
        pass


class Scene():
    def __init__():
        pass

    def process_input(self, events, pressed_keys):
        pass

    def update(self, game):
        pass

    def render(self, screen):
        pass


class Splash(Scene):
    def __init__(self):
        pass

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass

    def update(self, game):
        pass

    def render(self, screen):
        pass


class Playing(Scene):

    def __init__(self):
        pass

    def update(self, game):
        pass

    def render(self, screen):
        pass

class Paused(Scene):

    def __init__(self):
        pass

    def update(self, game):
        pass

    def render(self, screen):
        pass

class LevelComplete(Scene):

    def __init__(self):
        pass

    def update(self, game):
        pass

    def render(self, screen):
        pass

class GameOver(Scene):
    def __init__(self):
        pass

    def update(self, game):
        pass

    def render(self, screen):
        pass

class Victory(Scene):
    def __init__(self):
        pass

    def update(self, game):
        pass

    def render(self, screen):
        pass


class SceneManager():
    def __init__(self, current_scene):
        self.current_scene = current_scene

    def advance(self, next_scene):
        self.current_scene = next_scene


class MyGame():
    def __init__(self, start_scene):
        self.current_scene = start_scene

    def run(self):
        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption(TITLE)
        clock = pygame.time.Clock()
        running = True

        while running:
            # get events
            filtered_events = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    filtered_events.append(event)

            # poll input states
            pressed_keys = pygame.key.get_pressed()

            # game logic
            if running:
                self.current_scene.process_input(filtered_events, pressed_keys)
                self.current_scene.update(self)
                self.current_scene.render(screen)

            # wait a bit
            clock.tick(FPS)

if __name__ == "__main__":
    start_scene = Splash()
    game = MyGame(start_scene)
    game.run()
    pygame.quit()
