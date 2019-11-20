COURSES = 3
BRICKS_PER_COURSE = 5
W = 0.1
L = 0.2
H = 0.05
MORTAR_PERPENDS = 0.003
MORTAR_BEDS = 0.003

assembly = Assembly()
frame = Frame.worldXY()
row_frame = Frame.worldXY()

t = Translation([0.0, L + MORTAR_PERPENDS, 0]) 

for row in range(COURSES):
    prev_brick_key = None
    half_brick_ends = row % 2 != 0

    row_frame = Frame.worldXY()
    row_frame.point.z = (row * H) + (row * MORTAR_BEDS)

    for i in range(BRICKS_PER_COURSE + (1 if half_brick_ends else 0)):
        w = W
        l = L
        h = H
        first = i == 0
        last = i == BRICKS_PER_COURSE
        is_half_brick = (first or last) and half_brick_ends

        if is_half_brick:
            l = L / 2 - MORTAR_PERPENDS / 2

        brick = Brick(row_frame, w, l, h)
        brick_key = assembly.add_element(brick)

        if prev_brick_key is not None:
            assembly.add_connection(brick_key, prev_brick_key)
        prev_brick_key = brick_key

        if is_half_brick:
            row_frame = row_frame.transformed(Translation([0.0, l + MORTAR_PERPENDS, 0.0]))
        else:
            row_frame = row_frame.transformed(t)