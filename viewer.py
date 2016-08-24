#!/usr/bin/env python
import argparse
import sys
import os
import pygame
import pygame.locals
import pygame.key
import pygame.time


from constants import CARTESIAN_COORDS

NUM_PIXELS = len(CARTESIAN_COORDS)
BYTES_PER_FRAME = 3 * NUM_PIXELS
FPS = 20
FRAMES_PER_SKIP = 5 * FPS

CANVAS = pygame.Rect((0, 0), (575, 575))
STATUSBAR = pygame.Rect(CANVAS.bottomleft, (CANVAS.width, 20))
SCREEN = pygame.Rect(CANVAS.topleft, (CANVAS.width, CANVAS.height + STATUSBAR.height))

#size = width, height + 30

def convert_to_screen_pos(pos):
    # upper_left is 0,0
    # bottom left is 0, CANVAS.width
    x, y = pos
    scaled_x = (int)(25*x+50)
    scaled_y = (int)(CANVAS.width - 50 - (25*y))
    return (scaled_x, scaled_y)

def get_next_pixel(fin):
    try:
        r, g, b = [ord(c) for c in fin.read(3)]
        return r, g, b
    except:
        print "reached the end of the file"
        sys.exit(0)

def frame_to_timestamp(framenum):
    usecs = framenum * 1000000 / FPS
    seconds, usecs = divmod(usecs, 1000000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%02d:%02d:%02d.%02d" % (hours, minutes, seconds, usecs / 10000)

def run(fin, number_lights=False):
    pygame.init()

    screen = pygame.display.set_mode(SCREEN.size)

    positions = {i: v for i, v in enumerate(CARTESIAN_COORDS)}

    myfont = pygame.font.SysFont("monospace", 15)

    framenum = 0

    clock = pygame.time.Clock()
    while True:
        # did the user close the window?
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                sys.exit(0)

        skip = 0
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            skip += 1
        if pressed[pygame.K_LEFT]:
            skip -= 1

        if skip < 0:
            # seeking backwards from current offset
            for i in range(FRAMES_PER_SKIP):
                try:
                    fin.seek(skip * BYTES_PER_FRAME, 1)
                    framenum += skip
                except IOError:
                    # No error at BOF, or if stream isn't seekable
                    pass
        elif skip > 0:
            # consume frames from the stream. Works even if not seekable.
            for i in range(FRAMES_PER_SKIP):
                fin.read(skip * BYTES_PER_FRAME)
                framenum += 1

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

        screen.fill((0, 0, 0), STATUSBAR)

        label_text = "frame %d" % framenum
        label = myfont.render(label_text, 1, (255, 255, 255))
        label_width, label_height = myfont.size(label_text)
        screen.blit(label, (STATUSBAR.right - label_width, STATUSBAR.bottom - label_height))

        label_text = "%s" % frame_to_timestamp(framenum)
        label = myfont.render(label_text, 1, (255, 255, 255))
        label_width, label_height = myfont.size(label_text)
        screen.blit(label, (STATUSBAR.left, STATUSBAR.bottom - label_height))

        framenum += 1

        pygame.display.update()
        clock.tick(FPS)

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
