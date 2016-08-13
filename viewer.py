#!/usr/bin/env python
import argparse
import sys
import os
import pygame
import pygame.locals
import pygame.time


from constants import CARTESIAN_COORDS

size = width, height = 575, 575

def convert_to_screen_pos(pos):
    # upper_left is 0,0
    # bottom left is 0, width
    x, y = pos
    scaled_x = (int)(25*x+50)
    scaled_y = (int)(width - 50 - (25*y))
    return (scaled_x, scaled_y)

def get_next_pixel(fin):
    try:
        r = ord(fin.read(1))
        g = ord(fin.read(1))
        b = ord(fin.read(1))

        color = (r, g, b)
        return color
    except:
        print "reached the end of the file"
        sys.exit(0)

def run(fin, number_lights=False):
    pygame.init()

    screen = pygame.display.set_mode(size)

    positions = {i: v for i, v in enumerate(CARTESIAN_COORDS)}

    myfont = pygame.font.SysFont("monospace", 15)

    clock = pygame.time.Clock()
    while True:
        # did the user close the window?
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                sys.exit(0)

        # update all the lights
        for i, pos in positions.items():
            screen_pos = convert_to_screen_pos(pos)

            color = get_next_pixel(fin)

            pygame.draw.circle(screen, color, screen_pos, 17)

            if number_lights:
                s = str(i)

                label = myfont.render(s, 1, (255, 255, 255))

                # center text on the light
                x,y = screen_pos
                x_s, y_s = myfont.size(s)
                x, y = x-x_s/2, y-y_s/2

                screen.blit(label, (x,y))

        pygame.display.update()
        clock.tick(20)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='View a data file')
    parser.add_argument('-n', '--number-lights', dest='number_lights',
                        action='store_true', default=False,
                        help='Label the lights with their index')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('rb'),
                        help='The file to view.  You can also pipe the file to the process.')

    args = parser.parse_args()

    if args.file:
        fin = args.file
        print("reading from " + args.file.name)
    else:
        fin = sys.stdin
        print("reading from stdin")

    run(fin, number_lights=args.number_lights)
