import pygame

import settings
from settings import *
from ray_casting import ray_casting
from map import mini_map

class Drawing:
    def __init__(self, sc, sc_map):
        self.sc = sc
        self.sc_map = sc_map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {1: pygame.image.load('assets/walls/wall-1.png').convert(),
                         2: pygame.image.load('assets/walls/wall-2.png').convert(),
                         3: pygame.image.load('assets/walls/wall-3.png').convert(),
                         4: pygame.image.load('assets/walls/wall-4.png').convert(),
                         5: pygame.image.load('assets/walls/wall-5.png').convert(),
                         6: pygame.image.load('assets/walls/wall-6.png').convert(),
                         7: pygame.image.load('assets/walls/wall-7.png').convert(),
                         8: pygame.image.load('assets/walls/wall-8.png').convert(),
                         'S': pygame.image.load('assets/skies/clouds-1.png').convert()
                         }

        # create a text object for the win screen
        self.font2 = pygame.font.Font('assets/font/Pixelmania.ttf', 32)
        self.text = self.font2.render('YOU WIN', True, settings.SKYBLUE, settings.PINK)
        self.textRect = self.text.get_rect()
        self.textRect.center = (settings.WIDTH // 2, settings.HEIGHT // 2)

    def background(self, angle):
        sky_offset = -5 * math.degrees(angle) % WIDTH
        self.sc.blit(self.textures['S'], (sky_offset, 0))
        self.sc.blit(self.textures['S'], (sky_offset - WIDTH, 0))
        self.sc.blit(self.textures['S'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.sc, GREEN, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)

    def mini_map(self, player):
        self.sc_map.fill(SANDY)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.line(self.sc_map, GREEN, (map_x, map_y), (map_x + 12 * math.cos(player.angle),
                                                 map_y + 12 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.sc_map, YELLOW, (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, MAROON, (x, y, MAP_TILE, MAP_TILE))
        self.sc.blit(self.sc_map, MAP_POS)

    def win_screen(self):
        self.sc.blit(self.text, self.textRect)