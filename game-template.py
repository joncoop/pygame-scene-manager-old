#!/usr/bin/env python3

import json
import pygame

pygame.mixer.pre_init()
pygame.init()

# Display settings
TITLE = "Name of Game"
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60
GRID_SIZE = 64

# Options
sound_on = True

# Level files
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

# Some utility classes
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
        return pygame.image.load(file_path).convert_alpha()

    def load_scaled_image(file_path, width=GRID_SIZE, height=GRID_SIZE):
        img = pygame.image.load(file_path).convert_alpha()
        return pygame.transform.scale(img, (width, height))

    def reverse_image(img):
        return pygame.transform.flip(img, 1, 0)

    def reverse_images(img_list):
        return [pygame.transform.flip(img, 1, 0) for img in img_list]

    def scale_to_size(img, width, height):
        return pygame.transform.scale(img, (width, height))
    
    def scale_to_height(img, height):
        h = img.get_height()
        w = int(img.get_width() * height / h)
        return pygame.transform.scale(img, (w, height))
                
    def scale_to_width(img, width):
        h = int(img.get_height() * width / w)
        w = img.get_width()
        return pygame.transform.scale(img, (width, h))

    def tile_to_surface(img, surface, tile_x=True, tile_y=True):
        x_start = 0
        y_start = 0
        
        if tile_x:
            x_end = surface.get_width()
        else:
            x_end = img.get_width()

        if tile_y:
            y_end = surface.get_height()
        else:
            y_end = img.get_height()

        x_step = img.get_width()
        y_step = img.get_height()
            
        for y in range(y_start, y_end, y_step):
            for x in range(x_start, x_end, x_step):
                surface.blit(img, [x, y])

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

# Game assets
block_images = {"TL": ImageUtil.load_scaled_image("assets/tiles/top_left.png"),
                "TM": ImageUtil.load_scaled_image("assets/tiles/top_middle.png"),
                "TR": ImageUtil.load_scaled_image("assets/tiles/top_right.png"),
                "ER": ImageUtil.load_scaled_image("assets/tiles/end_right.png"),
                "EL": ImageUtil.load_scaled_image("assets/tiles/end_left.png"),
                "TP": ImageUtil.load_scaled_image("assets/tiles/top.png"),
                "CN": ImageUtil.load_scaled_image("assets/tiles/center.png"),
                "LF": ImageUtil.load_scaled_image("assets/tiles/lone_float.png"),
                "SP": ImageUtil.load_scaled_image("assets/tiles/special.png")}

item_images = {"Coin": ImageUtil.load_scaled_image("assets/items/coin.png"),
               "Heart": ImageUtil.load_scaled_image("assets/items/bandaid.png"),
               "OneUp": ImageUtil.load_scaled_image("assets/items/first_aid.png"),
               "Flag": ImageUtil.load_scaled_image("assets/items/flag.png"),
               "Pole": ImageUtil.load_scaled_image("assets/items/flagpole.png")}

hero_images = {"Walk": [ImageUtil.load_scaled_image("assets/hero/adventurer_walk1.png"),
                        ImageUtil.load_scaled_image("assets/hero/adventurer_walk2.png")],
               "Jump": [ImageUtil.load_scaled_image("assets/hero/adventurer_jump.png")],
               "Idle": [ImageUtil.load_scaled_image("assets/hero/adventurer_idle.png")]}

enemy_images = {"Bear": [ImageUtil.load_scaled_image("assets/enemies/bear-0.png"),
                         ImageUtil.load_scaled_image("assets/enemies/bear-1.png"),
                         ImageUtil.load_scaled_image("assets/enemies/bear-2.png")],
                "Monster": [ImageUtil.load_scaled_image("assets/enemies/monster-1.png"),
                            ImageUtil.load_scaled_image("assets/enemies/monster-2.png")]}

sound_effects = {'jump': pygame.mixer.Sound("assets/sounds/jump.wav"),
                 'coin': pygame.mixer.Sound("assets/sounds/pickup_coin.wav"),
                 'powerup': pygame.mixer.Sound("assets/sounds/powerup.wav"),
                 'hurt': pygame.mixer.Sound("assets/sounds/hurt.ogg"),
                 'die': pygame.mixer.Sound("assets/sounds/death.wav"),
                 'levelup': pygame.mixer.Sound("assets/sounds/level_up.wav"),
                 'gameover': pygame.mixer.Sound("assets/sounds/game_over.wav")}

# Game entities
class Entity(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vy = 0
        self.vx = 0

    def is_near(self, other, distance=SCREEN_WIDTH):
        '''
        Returns true if entity is within a certain distance from another.
        Useful for only calling update on sprites near hero to reduce lag.
        '''
        return abs(self.rect.centerx - other.rect.centerx) < distance

    def apply_gravity(self, level):
        self.vy += level.gravity
        self.vy = min(self.vy, level.terminal_velocity)

class Block(Entity):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

class Hero(Entity):
    def __init__(self, all_images):
        super().__init__(all_images['Idle'][0])

        self.speed = 5
        self.jump_power = 20

        self.score = 0
        self.lives = 3
        self.hearts = 3
        self.max_hearts = 3
        self.invincibility = 0
        
    def move_left(self):
        self.vx = -self.speed

    def move_right(self):
        self.vx = self.speed

    def stop(self):
        self.vx = 0
        
    def jump(self, level):
        self.rect.y += 2

        hit_list = pygame.sprite.spritecollide(self, level.blocks, False)

        if len(hit_list) > 0:
            self.vy = -1 * self.jump_power
            SoundUtil.play_sound(sound_effects['jump'])

        self.rect.y -= 2

    def check_boundaries(self, level):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > level.width:
            self.rect.right = level.width
            
    def move_and_process_blocks(self, blocks):
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.vx = 0
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.vx = 0

        self.rect.y += self.vy + 1 # the +1 is hacky. not quite sure why it helps. should I round?
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

    def process_items(self, items):
        hit_list = pygame.sprite.spritecollide(self, items, True)

        for item in hit_list:
            item.apply(self)

    def process_enemies(self, enemies):
        hit_list = pygame.sprite.spritecollide(self, enemies, False)

        if self.invincibility == 0:
            for item in hit_list:
                SoundUtil.play_sound(sound_effects['hurt'])
                self.hearts -= 1
                self.invincibility = int(0.75 * FPS)

    def check_flag(self, level):
        hit_list = pygame.sprite.spritecollide(self, level.flag, False)

        if len(hit_list) > 0:
            hit_list[0].apply(self)
            level.completed = True

    def die(self):
        SoundUtil.play_sound(sound_effects['die'])
        self.lives -= 1
            
    def update(self, level):
        self.apply_gravity(level)
        self.check_boundaries(level)
        self.move_and_process_blocks(level.blocks)

        if self.hearts > 0:
            self.process_items(level.items)
            self.process_enemies(level.enemies)
            self.check_flag(level)

            if self.invincibility > 0:
                self.invincibility -= 1
        else:
            self.die()

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        
        self.hearts = self.max_hearts
        self.invincibility = 0
        self.facing_right = True
        
class Enemy(Entity):
    def __init__(self, all_images, x, y):
        super().__init__(all_images[0], x, y)

        self.left_images = all_images
        self.right_images = ImageUtil.reverse_images(all_images)
        
        self.start_x = x
        self.start_y = y
        self.start_vx = -2
        self.start_vy = 0

        self.reset()
        
    def reverse(self):
        '''
        Changes the direction an enemy is moving.
        '''
        self.vx *= -1

    def check_world_boundaries(self, level):
        '''
        Enemies turn around when reaching level boundaries.
        '''
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > level.width:
            self.rect.right = level.width
            self.reverse()

    def move_and_process_blocks(self, blocks):
        '''
        Enemies move and then turn around when colliding with blocks.
        '''
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy # the +1 is hacky. not sure why it helps.
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

    def set_image(self):
        if self.vx < 0:
            self.current_images = self.left_images
        else:
            self.current_images = self.right_images
            
        if self.steps == 0:
            self.image = self.current_images[self.image_index]
            self.image_index = (self.image_index + 1) % len(self.current_images)

        self.steps = (self.steps + 1) % 15 # Nothing significant about 15. It just seems to work okay.

    def update(self, level):
        if self.is_near(level.hero):
            self.apply_gravity(level)
            self.move_and_process_blocks(level.blocks)
            self.check_world_boundaries(level)
            self.set_image()
            
    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vx = self.start_vx
        self.vy = self.start_vy
        
        self.current_images = self.left_images
        self.image_index = 0
        self.image = self.current_images[self.image_index]
        self.steps = 0
        
class Bear(Enemy):
    '''
    Bears behave like default enemy. No overrides needed.
    '''

    def __init__(self, all_images, x, y):
        super().__init__(all_images, x, y)

class Monster(Enemy):
    def __init__(self, all_images, x, y):
        super().__init__(all_images, x, y)

    def move_and_process_blocks(self, blocks):
        '''
        Monsters turn around when reaching ends of platforms.
        '''
        
        reverse = False

        self.rect.x += self.vx

        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy + 1 # the +1 is hacky. not sure why it helps.
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        reverse = True

        for block in hit_list:
            if self.vy >= 0:
                self.rect.bottom = block.rect.top
                self.vy = 0

                if self.vx > 0 and self.rect.right <= block.rect.right:
                    reverse = False

                elif self.vx < 0 and self.rect.left >= block.rect.left:
                    reverse = False

            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0


        if reverse:
            self.reverse()
            
class Item(Entity):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def apply(self, character):
        raise NotImplementedError

class Coin(Item):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.value = 1

    def apply(self, character):
        SoundUtil.play_sound(sound_effects['coin'])
        character.score += self.value

class Heart(Item):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def apply(self, character):
        SoundUtil.play_sound(sound_effects['powerup'])
        character.hearts += 1

class OneUp(Item):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def apply(self, character):
        SoundUtil.play_sound(sound_effects['powerup'])
        character.lives += 1

class Flag(Item):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def apply(self, character):
        SoundUtil.play_sound(sound_effects['levelup'])

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
        self.hero = Hero(hero_images) # Initialize a hero before starting GameScene scenes

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.change_to_scene( GameScene(self.hero, 0) )

    def update(self):
        '''
        Use this if the TitleScene is animated.
        '''
        pass

    def render(self, screen):
        screen.fill(BLACK)
        TextUtil.display_message(screen, "Name of Game", "Ready?!!! Press any key to start.")

class GameScene(Scene):
    def __init__(self, hero, level_num):
        super().__init__()

        self.hero = hero
        self.level_num = level_num
        self.completed = False
        self.paused = False
        
        self.starting_blocks = []
        self.starting_items = []
        self.starting_flag = []
        self.starting_enemies = []
        
        self.blocks = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.flag = pygame.sprite.Group()

        self.active_sprites = pygame.sprite.Group()
        self.inactive_sprites = pygame.sprite.Group()

        self.load_level()

    def load_level(self):
        data_file = levels[self.level_num]

        with open(data_file, 'r') as f:
            data = f.read()

        map_data = json.loads(data)

        self.width = map_data['width'] * GRID_SIZE
        self.height = map_data['height'] * GRID_SIZE
        
        self.start_x = map_data['start'][0] * GRID_SIZE
        self.start_y = map_data['start'][1] * GRID_SIZE

        self.gravity = map_data['gravity']
        self.terminal_velocity = map_data['terminal-velocity']

        self.background_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.scenery_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.inactive_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.active_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)

        if map_data['background-color'] != "":
            self.background_layer.fill(map_data['background-color'])

        if map_data['background-img'] != "":
            background_img = ImageUtil.load_image(map_data['background-img'])

            if map_data['background-scale-to-screen-height']:
                background_img = ImageUtil.scale_to_height(background_img, SCREEN_HEIGHT)

            repeat_x = map_data['background-repeat-x']
            repeat_y = map_data['background-repeat-y']
            
            ImageUtil.tile_to_surface(background_img, self.background_layer, repeat_x, repeat_y)

        if map_data['scenery-img'] != "":
            scenery_img = ImageUtil.load_image(map_data['scenery-img'])

            if map_data['scenery-scale-to-screen-height']:
                scenery_img = ImageUtil.scale_to_height(scenery_img, SCREEN_HEIGHT)

            repeat_x = map_data['scenery-repeat-x']
            repeat_y = map_data['scenery-repeat-y']
            
            ImageUtil.tile_to_surface(scenery_img, self.background_layer, repeat_x, repeat_y)

        for item in map_data['blocks']:
            x = item[0] * GRID_SIZE
            y = item[1] * GRID_SIZE
            kind = item[2]
            
            img = block_images[kind]
            self.starting_blocks.append( Block(img, x, y) )

        for item in map_data['items']:
            x = item[0] * GRID_SIZE
            y = item[1] * GRID_SIZE
            kind = item[2]
            
            img = item_images[kind]

            if kind == "Coin":
                self.starting_items.append( Coin(img, x, y) )
            elif kind == "Heart":
                self.starting_items.append( Heart(img, x, y) )
            elif kind == "OneUp":
                self.starting_items.append( OneUp(img, x, y) )

        for item in map_data['flag']:
            x = item[0] * GRID_SIZE
            y = item[1] * GRID_SIZE
            kind = item[2]
            
            img = item_images[kind]
            self.starting_flag.append( Flag(img, x, y) )

        for item in map_data['enemies']:
            x = item[0] * GRID_SIZE
            y = item[1] * GRID_SIZE
            kind = item[2]
            
            imgs = enemy_images[kind]

            if kind == "Bear":
                self.starting_enemies.append( Bear(imgs, x, y) )
            elif kind == "Monster":
                self.starting_enemies.append( Monster(imgs, x, y) )

        self.reset()

    def reset(self):
        self.blocks.add(self.starting_blocks)
        self.flag.add(self.starting_flag)
        self.items.add(self.starting_items)
        self.enemies.add(self.starting_enemies)
        
        self.inactive_sprites.add(self.starting_blocks, self.starting_flag)
        self.active_sprites.add(self.hero, self.items, self.enemies)

        self.hero.reset(self.start_x, self.start_y)

        for e in self.enemies:
            e.reset()
        
        # draw inactive layer here since we don't need to redraw on each iteration of game loop
        self.inactive_sprites.draw(self.inactive_layer)

    def display_stats(self, surface):
        hearts_text = FONT_SM.render("Hearts: " + str(self.hero.hearts), 1, WHITE)
        lives_text = FONT_SM.render("Lives: " + str(self.hero.lives), 1, WHITE)
        score_text = FONT_SM.render("Score: " + str(self.hero.score), 1, WHITE)

        surface.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 32, 32))
        surface.blit(hearts_text, (32, 32))
        surface.blit(lives_text, (32, 64))
    
    def calculate_offset(self):
        x = -1 * self.hero.rect.centerx + SCREEN_WIDTH / 2

        if self.hero.rect.centerx < SCREEN_WIDTH / 2:
            x = 0
        elif self.hero.rect.centerx > self.width - SCREEN_WIDTH / 2:
            x = -1 * self.width + SCREEN_WIDTH

        return x, 0
    
    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.completed:
                    if event.key == pygame.K_SPACE:
                        # advance to next scene
                        self.level_num += 1

                        if self.level_num < len(levels):
                            self.change_to_scene( GameScene(self.hero, self.level_num) )
                        else:
                            self.change_to_scene( VictoryScene(self.hero) )

                else:
                    if event.key == pygame.K_p:
                        # toggle paused state
                        self.paused = not self.paused

                    if not self.paused:
                        # deal with actions bound to game events such as jumping
                        if event.key == pygame.K_SPACE:
                            self.hero.jump(self)

                        # temp stuff for scene testing
                        if event.key == pygame.K_c:
                            self.completed = True

        if not (self.completed or self.paused):
            # deal with actions bound to pressed keys
            if pressed_keys[pygame.K_LEFT]:
                self.hero.move_left()
            elif pressed_keys[pygame.K_RIGHT]:
                self.hero.move_right()
            else:
                self.hero.stop()

    def update(self):
        if not (self.completed or self.paused):
            self.active_sprites.update(self)

            if self.hero.lives == 0:
                self.change_to_scene( GameOverScene(self) )
            elif self.hero.hearts == 0:
                self.reset()

    def render(self, surface):
        offset_x, offset_y = self.calculate_offset()
        
        self.active_layer.fill(TRANSPARENT)
        self.active_sprites.draw(self.active_layer)

        surface.blit(self.background_layer, [offset_x / 3, offset_y])
        surface.blit(self.scenery_layer, [offset_x / 2, offset_y])
        surface.blit(self.inactive_layer, [offset_x, offset_y])
        surface.blit(self.active_layer, [offset_x, offset_y])
        self.display_stats(surface)
        
        # special messages
        if self.completed:
            TextUtil.display_message(surface, "Level complete!", "Press any key to continue.")
        elif self.paused:
            TextUtil.display_message(surface, "Paused", "Press 'P' to continue.")

class GameOverScene(Scene):
    def __init__(self, hero):
        super().__init__(hero)
        self.hero = hero

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.change_to_scene( TitleScene() )

    def update(self):
        pass

    def render(self, surface):
        surface.fill(BLACK)
        TextUtil.display_message(surface, "Game Over", "Press 'R' to restart.")

class VictoryScene(Scene):
    def __init__(self, hero):
        super().__init__()
        self.hero = hero

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.change_to_scene( TitleScene() )

    def update(self):
        pass

    def render(self, surface):
        surface.fill(BLACK)
        TextUtil.display_message(surface, "You win!", "Press 'R' to restart.")

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
