#!/usr/bin/env python3

import json
import pygame

pygame.init()

# Display settings
TITLE = "Name of Game"
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60
GRID_SIZE = 64

# Options
sound_on = True

# Levels
levels = ["levels/world-1.json",
          "levels/world-2.json",
          "levels/world-3.json"]

# Colors
TRANSPARENT = (0, 0, 0, 0)
DARK_BLUE = (16, 86, 103)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
FONT_SM = pygame.font.Font("assets/fonts/minya_nouvelle_bd.ttf", 32)
FONT_MD = pygame.font.Font("assets/fonts/minya_nouvelle_bd.ttf", 64)
FONT_LG = pygame.font.Font("assets/fonts/thats_super.ttf", 72)

# Make the display
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Some helper classes
class TextUtil():
    def display_message(surface, primary_text, secondary_text=None):
        w = surface.get_width()
        h = surface.get_height()

        line1 = FONT_MD.render(primary_text, 1, WHITE)
        x1 = w / 2 - line1.get_width() / 2;
        y1 = h / 3 - line1.get_height() / 2;
        surface.blit(line1, (x1, y1))

        if secondary_text != None:
            line2 = FONT_SM.render(secondary_text, 1, WHITE)
            x2 = w / 2 - line2.get_width() / 2;
            y2 = y1 + line1.get_height() + 16;
            surface.blit(line2, (x2, y2))

class ImageUtil():
    def load_image(file_path):
        return pygame.image.load(file_path).convert()

    def load_scaled_image(file_path, width=GRID_SIZE, height=GRID_SIZE):
        img = pygame.image.load(file_path).convert()
        return pygame.transform.scale(img, (width, height))

    def reverse_image(img):
        return pygame.transform.flip(img, 1, 0)

    def reverse_images(img_list):
        return [pygame.transform.flip(img, 1, 0) for img in img_list]

class SoundUtil():
    def toggle_mute(self):
        global sound_on
        sound_on = not sound_on

    def play_sound(sound, loops=0, maxtime=0, fade_ms=0):
        if sound_on:
            sound.play(loops, maxtime, fade_ms)

    def play_music(self):
        if sound_on:
            pygame.mixer.music.play(-1)

class Assets():
    block_types = {"TL": ImageUtil.load_scaled_image("assets/tiles/top_left.png"),
                   "TM": ImageUtil.load_scaled_image("assets/tiles/top_middle.png"),
                   "TR": ImageUtil.load_scaled_image("assets/tiles/top_right.png"),
                   "ER": ImageUtil.load_scaled_image("assets/tiles/end_right.png"),
                   "EL": ImageUtil.load_scaled_image("assets/tiles/end_left.png"),
                   "TP": ImageUtil.load_scaled_image("assets/tiles/top.png"),
                   "CN": ImageUtil.load_scaled_image("assets/tiles/center.png"),
                   "LF": ImageUtil.load_scaled_image("assets/tiles/lone_float.png"),
                   "SP": ImageUtil.load_scaled_image("assets/tiles/special.png")}

# Game entities
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pass

    def is_near(self, other, distance=SCREEN_WIDTH):
        '''
        Returns true if entity is within a certain distance from another.
        Useful for only calling update on sprites near hero to reduce lag.
        '''
        return abs(self.rect.centerx - other.rect.centerx) < distance

    def apply_gravity(self, level):
        self.vy += self.level.gravity
        self.vy = min(self.level.gravity, self.level.terminal_velocity)
        
class Block(Entity):
    def __init__(self, x, y, kind):
        pass

class Hero(Entity):
    def __init__(self):
        pass

    def check_boundaries(self, level):
        pass

    def move_and_process_blocks(self, blocks):
        pass

    def process_items(self):
        pass

    def process_enemies(self):
        pass

    def update(self, level):
        level.physics.apply_gravity(self)
        check_boundaries(level)
        move_and_process_blocks(level.blocks)
        process_items(level.items)
        process_enemies(level.enemies)

class Enemy(Entity):
    def __init__(self, animation_frames):
        pass

    def reverse(self):
        pass

    def check_boundaries(self, level):
        pass

    def move_and_process_blocks(self, blocks):
        pass

    def update(self, level, hero):
        pass

class Bear(Enemy):
    def __init__(self):
        pass

class Monster(Enemy):
    def __init__(self):
        pass

class Item(Entity):
    def __init__(self):
        pass

    def apply(self, character):
        raise NotImplementedError

class Coin(Item):
    def __init__(self):
        self.value = 1

    def apply(self, character):
        character.score += self.value

class Heart(Item):
    def __init__(self):
        pass

    def apply(self, character):
        character.hearts += 1

# Scenes
class Scene():
    def __init__(self):
        self.next_scene = self

    def process_input(self, events, pressed_keys):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self, surface):
        raise NotImplementedError

    def change_to_scene(self, next_scene):
        self.next_scene = next_scene

    def terminate(self):
        self.next_scene = None

class TitleScene(Scene):
    def __init__(self):
        super().__init__()

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.change_to_scene( Level(0) )

    def update(self):
        '''
        Use this if the TitleScene is animated.
        '''
        pass

    def render(self, screen):
        screen.fill(BLACK)
        TextUtil.display_message(screen, "Name of Game", "Press SPACE to start.")

class Level(Scene):
    def __init__(self, level_num):
        super().__init__()

        self.level_num = level_num
        self.completed = False
        self.paused = False

        self.load(self.level_num)

    def load(self, level_num):
        data_file = levels[level_num]

        self.starting_blocks = []

        with open(data_file, 'r') as f:
            data = f.read()

        map_data = json.loads(data)

        self.width = map_data['width'] * GRID_SIZE
        self.height = map_data['height'] * GRID_SIZE

        self.start_x = map_data['start'][0] * GRID_SIZE
        self.start_y = map_data['start'][1] * GRID_SIZE

        for item in map_data['blocks']:
            x, y, kind = item[0], item[1], item[2]
            self.starting_blocks.append( Block(x, y, kind) )

    def reset(self):
        pass

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.completed:
                    if event.key == pygame.K_SPACE:
                        # advance to next scene
                        self.level_num += 1

                        if self.level_num < len(levels):
                            self.change_to_scene( Level(self.level_num) )
                        else:
                            self.change_to_scene( Victory() )

                else:
                    if event.key == pygame.K_p:
                        # toggle paused state
                        self.paused = not self.paused

                    if not self.paused:
                        # deal with actions bound to game events such as jumping
                        pass

                        # temp stuff for scene testing
                        if event.key == pygame.K_c:
                            self.completed = True

        if not (self.completed or self.paused):
            # deal with actions bound to pressed keys
            pass

    def update(self):
        if not (self.completed or self.paused):
            # game is active, update all entities
            pass

    def render(self, surface):
        surface.fill(BLACK)
        if not (self.completed or self.paused):
            TextUtil.display_message(surface, str(self.level_num))

        # special messages
        if self.completed:
            TextUtil.display_message(surface, "Level complete!", "Press SPACE to continue.")
        elif self.paused:
            pass

class GameOver(Scene):
    def __init__(self):
        super().__init__()

    def process_input(self, events, pressed_keys):
        pass

    def update(self):
        pass

    def render(self, surface):
        surface.fill(BLACK)
        TextUtil.display_message(surface, "Game Over")

class Victory(Scene):
    def __init__(self):
        super().__init__()

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.change_to_scene( TitleScene() )

    def update(self):
        pass

    def render(self, surface):
        surface.fill(BLACK)
        TextUtil.display_message(surface, "You win!", "Press SPACE to restart.")

# The actual game
class MyGame():
    def __init__(self):
        self.active_scene = TitleScene()

    def is_quit_event(self, event, pressed_keys):
        x_out = event.type == pygame.QUIT

        ctrl_q = (event.type == pygame.KEYDOWN and
                  event.key == pygame.K_q and
                  (pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]))

        return x_out or ctrl_q

    def run(self):
        while self.active_scene != None:
            # poll input states
            pressed_keys = pygame.key.get_pressed()

            # get events
            filtered_events = []
            for event in pygame.event.get():
                if self.is_quit_event(event, pressed_keys):
                    self.active_scene.terminate()
                else:
                    filtered_events.append(event)

            # game logic
            self.active_scene.process_input(filtered_events, pressed_keys)
            self.active_scene.update()
            self.active_scene.render(screen)
            self.active_scene = self.active_scene.next_scene

            # update screen
            pygame.display.flip()

            # wait a bit
            clock.tick(FPS)

if __name__ == "__main__":
    game = MyGame()
    game.run()
    pygame.quit()
