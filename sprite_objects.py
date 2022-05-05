import pygame

from settings import *
from collections import deque

class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'bush': {
                'name' : 'bush',
                'sprite': pygame.image.load('assets/sprites/bush.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1,
                'scale': 0.5,
                'animation': [],
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
                'pickup': False
            },
            'tree': {
                'name': 'tree',
                'sprite': pygame.image.load('assets/sprites/tree.png').convert_alpha(),
                'viewing_angles': None,
                'shift': -0.1,
                'scale': 1.2,
                'animation': [],
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
                'pickup': False
            },
            'column-1': {
                'name': 'column-1',
                'sprite': pygame.image.load('assets/sprites/column-1.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.2,
                'scale': 0.5,
                'animation': [],
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
                'pickup': False
            },
            'column-2': {
                'name': 'column-2',
                'sprite': pygame.image.load('assets/sprites/column-2.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 1.2,
                'scale': 0.5,
                'animation': [],
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
                'pickup': False
            },
            'gem': {
                'name': 'gem',
                'sprite': pygame.image.load('assets/sprites/gems/0.png').convert_alpha(),
                'viewing_angles': None,
                'shift': 0.5,
                'scale': 0.5,
                'animation': deque(
                    [pygame.image.load(f'assets/sprites/gems/anim/{i}.png').convert_alpha() for i in range(5)]),
                'animation_dist': 800,
                'animation_speed': 20,
                'blocked': None,
                'pickup': True
            },
        }

        self.list_of_objects = [
            # start area
            SpriteObject(self.sprite_parameters['tree'], (5.9, 2.1)),
            SpriteObject(self.sprite_parameters['bush'], (8.8, 2.5)),
            SpriteObject(self.sprite_parameters['bush'], (8.8, 4.6)),
            # mid area
            SpriteObject(self.sprite_parameters['tree'], (18.5, 9)),
            SpriteObject(self.sprite_parameters['tree'], (18.5, 12)),
            SpriteObject(self.sprite_parameters['tree'], (22.5, 9)),
            SpriteObject(self.sprite_parameters['tree'], (22.5, 12)),
            # temple
            SpriteObject(self.sprite_parameters['column-1'], (6.8, 9.3)),
            SpriteObject(self.sprite_parameters['column-2'], (6.8, 11.72)),
            SpriteObject(self.sprite_parameters['column-2'], (8.8, 9.3)),
            SpriteObject(self.sprite_parameters['column-1'], (8.8, 11.72)),
            SpriteObject(self.sprite_parameters['column-1'], (10.8, 9.3)),
            SpriteObject(self.sprite_parameters['column-2'], (10.8, 11.72)),
            SpriteObject(self.sprite_parameters['column-1'], (12.8, 9.3)),
            SpriteObject(self.sprite_parameters['column-2'], (12.8, 11.72)),
            SpriteObject(self.sprite_parameters['tree'], (5.0, 9.4)),
            SpriteObject(self.sprite_parameters['tree'], (5.0, 11.60)),
            SpriteObject(self.sprite_parameters['gem'], (5, 10.45))
            #SpriteObject(self.sprite_types['snake'], False, (7, 4), -0.1, 0.6)
        ]


class SpriteObject:
    def __init__(self, parameters, pos):
        self.name = parameters['name']
        self.object = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.pickup = parameters['pickup']
        self.side = 30
        self.animation_count = 0
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.pos = self.x - self.side // 2, self.y - self.side // 2
        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and distance_to_sprite > 30:
            proj_height = min(int(PROJ_COEFF / distance_to_sprite * self.scale), DOUBLE_HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift
            # choosing sprite for angle
            if self.viewing_angles:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            # sprite animation
            sprite_object = self.object
            if self.animation and distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            # sprite scale and pos
            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def pickup_object(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)
        return self.name, self.pickup, distance_to_sprite
