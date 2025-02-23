#!/usr/bin/env python
import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

class Hex:
    def __init__(self, size, x, y):
        self.size = size
        self.x = x
        self.y = y
        self.verts = self._verts()

    def _verts(self):
        return [
            (self.x + self.size, self.y),
             (self.x + 0.5*self.size, self.y + 0.5*np.sqrt(3)*self.size),
             (self.x - 0.5*self.size, self.y + 0.5*np.sqrt(3)*self.size),
             (self.x - self.size, self.y),
             (self.x - 0.5*self.size, self.y - 0.5*np.sqrt(3)*self.size),
             (self.x + 0.5*self.size, self.y - 0.5*np.sqrt(3)*self.size)
        ]

    def contains_point(self, xy):
        # TODO: This is a hack for now, just does center rectangle
        x, y = xy
        # Hard requirement that y be in this band
        if y < self.y + 0.5*np.sqrt(3)*self.size\
                and y > self.y - 0.5*np.sqrt(3)*self.size:
            dy = y - self.y
            if x < self.x + 0.5*self.size and x > self.x - 0.5*self.size:
                return True
            elif x > self.x + 0.5*self.size\
                    and x < self.x + self.size - 0.5*np.sqrt(3)*dy:
                return True
        else:
            return False


def render_grid(screen, hex_list, mouse_pos):
    highlighted = None
    for h in hex_list:
        pygame.draw.polygon(screen, "black", h.verts, width=1)
        if h.contains_point(mouse_pos):
            highlighted = h
    if highlighted:
        pygame.draw.polygon(screen, "yellow", highlighted.verts, width=1)


def hex_grid(size, nrows, ncols):
    # Jump by 1.5*size in x coords for each column
    # Jump by sqrt(3)*size in y coords each row
    # Odd columns get offset down in y by (sqrt(3)/2) * size
    hex_list = []
    for col in range(ncols):
        x = size + 1.5*size*col
        for row in range(nrows):
            y = 0.5*np.sqrt(3)*size + np.sqrt(3)*size*row
            if col % 2 == 1:
                y += 0.5*np.sqrt(3)*size
            hex_list.append(Hex(size, x, y))
    return hex_list


size = 100.0
hex_list = hex_grid(size, 4, 8)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    # Render game
    mouse_pos = pygame.mouse.get_pos()
    render_grid(screen, hex_list, mouse_pos)

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
