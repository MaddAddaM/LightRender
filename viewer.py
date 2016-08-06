import pygame
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


pos = {i: v for i, v in enumerate(pos_list)}

red = (255, 0, 0)

def get_color(i):
    red = 255 * (i / 199.0)
    green = 0
    blue = 255 * ((199-i) / 199.0)
    c = (int(red), int(green), int(blue))
    return c

def get_screen_pos(x, y):
    # upper_left is 0,0
    # bottom left is 0, width
    scaled_x = (int)(50*x+50)
    scaled_y = (int)(width - 50 - (50*y))
    return (scaled_x, scaled_y)

myfont = pygame.font.SysFont("monospace", 15)

for k, v in pos.items():
    x, y = v
    pos = get_screen_pos(x, y)
    pygame.draw.circle(screen, get_color(k), pos, 10)

    if label_lights:
        label = myfont.render(str(k), 1, (255, 255, 255))
        screen.blit(label, pos)

pygame.display.update()

import time
time.sleep(10)
