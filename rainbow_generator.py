from constants import CARTESIAN_COORDS
import colorsys
import sys

class Pattern(object):
    center_x, center_y = 15, 10

    mov_x, mov_y = -1, -1
    i = 0

    def next_frame(self):
        self.i += 1
        self.center_x += self.mov_x * 0.1
        self.center_y += self.mov_y * 0.1

        if self.center_x < 0 or self.center_x > 19:
            self.mov_x *= -1

        if self.center_y < 0 or self.center_y > 19:
            self.mov_y *= -1

    def get_color(self, x, y):
        d = ((x - self.center_x) ** 2 + (y - self.center_y) ** 2) ** 0.5
        d *= 0.1
        d -= 0.025 * self.i
        r, g, b = colorsys.hsv_to_rgb(d%1, 1, 1)

        red = 255 * r
        green = 255 * g
        blue = 255 * b
        c = (int(red), int(green), int(blue))
        return c

p = Pattern()

for frame in range(1000):
    for x, y in CARTESIAN_COORDS:
        color = p.get_color(x, y)
        r, g, b = color
        sys.stdout.write(chr(r))
        sys.stdout.write(chr(g))
        sys.stdout.write(chr(b))

    sys.stdout.flush()
    p.next_frame()
