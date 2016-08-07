# 20 lights up, then 20 lights back down at the same heights, 5 times.
ROWS = (range(20)[::] + range(20)[::-1]) * 5

# 20 lights switching between cols 1 and 2, then 20 switching between 4 and 3,
# repeated 5 times offset by 4 columns per repetition.
COLS = [v + 4 * i for i in range(5) for v in [j % 2 for j in range(20)] + [3 - j % 2 for j in range(20)]]

# [(x0,y0), (x1, y1), ... (x199, y199)]
POSITIONS = zip(COLS, ROWS)
