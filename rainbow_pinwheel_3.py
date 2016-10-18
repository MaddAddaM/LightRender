#!/usr/bin/env python
from constants import CARTESIAN_COORDS
import colorsys
import sys
import math

class Pattern(object):
    center_x, center_y = 10, 10

    # mov_x, mov_y = 1, 1
    i = 0

    arms = 4

    def next_frame(self):
        self.i += 1
        # self.center_x += self.mov_x * 0.3
        # self.center_y += self.mov_y * 0.3
        #
        # if self.center_x < 0 or self.center_x > 19:
        #     self.mov_x *= -1
        #
        # if self.center_y < 0 or self.center_y > 19:
        #     self.mov_y *= -1

    def get_color(self, x, y):
        distance = ((x - self.center_x) ** 2 + (y - self.center_y) ** 2) ** 0.5

        # make the center white, it's all garbled in the middle anyways
        # due to sampling
        if distance < 2:
            return 255, 255, 255

        # calc angle between pixel and centerpoint
        atan = math.atan2((y - self.center_y),(x - self.center_x))

        # adjust angle in radians to [0,1]
        h = (atan + math.pi)/(2*math.pi)

        # multiple arms for the color wheel
        h *= self.arms

        # spin the color wheel
        h -= 0.025 * self.i

        # bend the arms for a pin wheel effect

        bend_ratio = math.sin(self.i/100.0)
        h += 0.08* bend_ratio * distance

        r, g, b = colorsys.hsv_to_rgb(h%1, 1, 1)

        red = 255 * r
        green = 255 * g
        blue = 255 * b
        c = (int(red), int(green), int(blue))
        return c

p = Pattern()

for frame in range(6000):
    for x, y in CARTESIAN_COORDS:
        color = p.get_color(x, y)
        r, g, b = color
        sys.stdout.write(chr(r))
        sys.stdout.write(chr(g))
        sys.stdout.write(chr(b))

    sys.stdout.flush()
    p.next_frame()
