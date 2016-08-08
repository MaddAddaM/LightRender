# 20 lights down, then 20 lights back up at the same heights, 5 times.
_rows = (range(20)[::-1] + range(20)[::]) * 5

# 20 lights switching between cols 1 and 2, then 20 switching between 4 and 3,
# repeated 5 times offset by 4 columns per repetition.
_cols = [v + 4 * i for i in range(5)
         for v in [j % 2 for j in range(20)] + [3 - j % 2 for j in range(20)]
         ]

# [(x0,y0), (x1, y1), ... (x199, y199)]
CARTESIAN_COORDS = zip(_cols, _rows)
