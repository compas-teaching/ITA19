# Assignment

## Task 1

Write a function that returns `True` if the rotation from `AB` onto `AC` is counter-clockwise (ccw).

`A`, `B`, `C` are points in the xy-plane...

```python
def is_ccw(A, B, C):
  # .....
```

## Task 2

Read points from the `points.txt` text file in this folder. Each line contains a tuple with three 2D points. Each point is a tuple of 2 floats (`x,y`), e.g. `((1895.0943, 2291.517), (589.296, 207.324), (1360.998, 1611.965))`.

Calculate and print out `is_ccw` for each tuple of points.

## Extra brownie points 🍪

Given a point `P` and a normal that span a plane in 3D space, return an arbitrary vector that rests within that plane.
