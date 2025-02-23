#!/usr/bin/env python
import pygame
import numpy as np
from math import sqrt

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

class Hex:
    def __init__(self, coords):
        self.coords = coords

    def _x(self, size):
        return size + 1.5*size*self.coords[1]
    
    def _y(self, size):
        y = 0.5*sqrt(3)*size + sqrt(3)*size*self.coords[0]
        if self.coords[1] % 2 == 1:
            y += 0.5*sqrt(3)*size
        return y

    def _verts(self, size):
        x = self._x(size)
        y = self._y(size)
        return [
            (x + size, y),
            (x + 0.5*size, y + 0.5*sqrt(3)*size),
            (x - 0.5*size, y + 0.5*sqrt(3)*size),
            (x - size, y),
            (x - 0.5*size, y - 0.5*sqrt(3)*size),
            (x + 0.5*size, y - 0.5*sqrt(3)*size)
        ]

    def contains_point(self, size, xy):
        # TODO: This is a hack for now, just does center rectangle
        x, y = xy
        sx = self._x(size)
        sy = self._y(size)
        # Hard requirement that y be in this band
        if y < sy + 0.5*sqrt(3)*size and y > sy - 0.5*sqrt(3)*size:
            dy = y - sy
            if x < sx + 0.5*size and x > sx - 0.5*size:
                return True
            elif x > sx + 0.5*size and x < sx + size - 0.5*sqrt(3)*dy:
                return True
        else:
            return False
    
    def render(self, screen, size, color="black"):
        verts = self._verts(size)
        pygame.draw.polygon(screen, color, verts, width=1)


def render_grid(screen, size, hex_list, mouse_pos):
    highlighted = None
    for h in hex_list:
        h.render(screen, size)
        if h.contains_point(size, mouse_pos):
            highlighted = h
    if highlighted:
        highlighted.render(screen, size, color="yellow")


def hex_grid(size, nrows, ncols):
    # Jump by 1.5*size in x coords for each column
    # Jump by sqrt(3)*size in y coords each row
    # Odd columns get offset down in y by (sqrt(3)/2) * size
    hex_list = []
    for col in range(ncols):
        for row in range(nrows):
            hex_list.append(Hex((row, col)))
    return hex_list


size = 100
hex_list = hex_grid(size, 41, 85)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                # Scroll up
                if size < 200:
                    size += 10
            elif event.y < 0:
                # Scroll down
                if size > 10:
                    size -= 10
    
    # 0 - Left click
    # 1 - Middle click
    # 2 - Right click
    mouse_click_tuple = pygame.mouse.get_pressed()

    if mouse_click_tuple[1]:
        # Middle click to pan
        x, y = pygame.mouse.get_rel()
        screen_center[0] += x
        screen_center[1] += y

    screen.fill("white")

    # Render game
    mouse_pos = pygame.mouse.get_pos()
    render_grid(screen, size, hex_list, mouse_pos)

    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
    """

    pygame.display.flip()

    # Limit game to 60 fps
    dt = clock.tick(60) / 1000

pygame.quit()
