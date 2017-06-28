#!/usr/bin/env python
from constants import CARTESIAN_COORDS
import colorsys
import sys
import math

class Pattern(object):
    i = 0

    def next_frame(self):
        self.i += 1

    def rotation_matrix(self, x, y, theta):
        x_prime = math.cos(theta) * x - math.sin(theta) * y
        y_prime = math.sin(theta) * x + math.cos(theta) * y
        return x_prime, y_prime

    def get_hue(self, x, y):
        x, y = self.rotation_matrix(x-10, y-10, self.i/50.0)

        d = y - self.i / 4.0
        # d = y

        d *= 0.02

        return d

    def get_saturation(self, x, y):
        s = (math.sin(y/2.0 + self. i / 10.0) + 1) / 2 # 0, 1
        s = s * 2.0 / 3 + 1.0/3 # 0.33, 1

        return s

    def get_color(self, x, y):

        h = self.get_hue(x, y)

        s = self.get_saturation(x, y)

        r, g, b = colorsys.hsv_to_rgb(h % 1, s, 1)

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
