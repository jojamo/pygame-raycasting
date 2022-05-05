import pygame
import audio
from settings import *
from audio import *
from player import Player
from sprite_objects import *
from ray_casting import ray_casting
from ray_casting import ray_casting_walls
from drawing import Drawing

pygame.init()
audio.play_track()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(False)
sc_map = pygame.Surface(MINIMAP_RES)

sprites = Sprites()
clock = pygame.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map)
winGame = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    player.pickup([obj.pickup_object(player) for obj in sprites.list_of_objects])
    sc.fill(BLACK)

    drawing.background(player.angle)
    walls = ray_casting_walls(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.mini_map(player)

    # if player touches gem
    if player.returnWin() == 1:
        drawing.win_screen()

    pygame.display.flip()
    clock.tick(FPS)

    pygame.display.set_caption("Pygame Raycasting - FPS: " + str(int(clock.get_fps())))