import pygame
import colorsys

pygame.init()
size = width, height = 575, 575

screen = pygame.display.set_mode(size)

label_lights = False


def up_row(x_offset):
    for i in range(20):
        x = x_offset + (i % 2) * 0.5
        y = i * 0.5
        yield x, y

def down_row(x_offset):
    for i in range(20):
        x = x_offset + ((i+ 1) % 2) * 0.5
        y = 9.5 - (i * 0.5)
        yield x, y

pos_list = []

for strip_pair in range(5):
    pos_list += list(up_row(2 * strip_pair))
    pos_list += list(down_row(2 * strip_pair + 1))


positions = {i: v for i, v in enumerate(pos_list)}

red = (255, 0, 0)

def get_color(x, y, i):
    # min 0,0
    # max 9.5, 9.5
    center_x, center_y = 5, 5
    d = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
    d *= 0.1
    d += 0.01 * i
    r, g, b = colorsys.hsv_to_rgb(d, 1, 1)

    red = 255 * r
    green = 255 * g
    blue = 255 * b
    c = (int(red), int(green), int(blue))
    return c

def get_screen_pos(x, y):
    # upper_left is 0,0
    # bottom left is 0, width
    scaled_x = (int)(50*x+50)
    scaled_y = (int)(width - 50 - (50*y))
    return (scaled_x, scaled_y)

myfont = pygame.font.SysFont("monospace", 15)

import time

for frame in range(1000):
    for k, v in positions.items():
        x, y = v
        pos = get_screen_pos(x, y)
        color = get_color(x, y, frame)
        pygame.draw.circle(screen, color, pos, 10)

        if label_lights:
            label = myfont.render(str(k), 1, (255, 255, 255))
            screen.blit(label, pos)

    pygame.display.update()
    time.sleep(0.05)

