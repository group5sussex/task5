

import copy
import numpy as np


"""
for each piece
when x+1 =>x+1 and y+1 and z-1
when y+1 => y+1 z-1

????
when x-1 =>x-1 and y-1 and z+1
when y-1 =>y-1 and z+1
????

for each point in piece
go down
    in piece y=y+1
    in pyramid y=y+1 x=x-1 z=z-1

go right x=x+1
"""

# centeral_triangle
z_base = 4
# x_base = 1
y_base = 0

piece_in_pyramid = [(0, 0), (1, 0), (1, 1)]
PYRAMID_LAYERS = {
    0: (5, 5),
    1: (4, 4),
    2: (3, 3),
    3: (2, 2),
    4: (1, 1)
}


def get_pyramid_layers(layer):
    if layer not in PYRAMID_LAYERS:
        raise ValueError("layer not in layers")
    else:
        y, x = PYRAMID_LAYERS[layer]
        return x


class Triangle:

    # values z_base (diagonal height or biggest y) from [1 to 4]
    # values x_base (diagonal smallest x) [0 to 3]

    def __init__(self, piece, z_base, x_base):

        if not (1 <= z_base <= 4 and 0 <= x_base <= 3):
            raise ValueError(
                f"Invalid x_base:{x_base}  or z_base: {z_base}")

        if x_base > 0 and x_base+z_base != 4:
            raise ValueError(
                f"Invalid x_base+z_base : x_base:{x_base}  or z_base: {z_base}")

        self.piece = piece
        self.z_base = z_base
        self.x_base = x_base
        self.piece_in_pyramid = []

        self.initiate_piece_in_triangle()

    def get_piece_in_pyramid(self):
        return self.piece_in_pyramid

    def get_triangle_piece(self):
        return self.piece

    def initiate_piece_in_triangle(self):

        # problem:every piece needs to be normalized
        if self.x_base > 0:
            for y, x, z in self.piece:
                z = self.z_base-y-x
                x = x+self.x_base
                y = y+self.x_base
                self.piece_in_pyramid.append((y, x, z))
        else:
            self.piece_in_pyramid = [(y, x, self.z_base-y-x)
                                     for y, x, z in self.piece]

        self.piece = [(y+x, x, z)for y, x, z in self.piece]

    def go_down(self):
        self.piece = [(y+1, x, z)for y, x, z in self.piece]
        self.piece_in_pyramid = [(y+1, x, z-1)
                                 for y, x, z in self.piece_in_pyramid]
        print("go down")
        # add_piece

    def go_right(self):
        # y in pyramid -- but y does not change in the piece
        # x in pyramid ++
        # add_piece()
        self.piece = [(y, x+1, z)for y, x, z in self.piece]
        self.piece_in_pyramid = [(y-1, x+1, z)
                                 for y, x, z in self.piece_in_pyramid]

        print("go right")

    def is_valid_triangle(self):

        for y, x, z in self.piece_in_pyramid:

            if z not in PYRAMID_LAYERS:
                # print("false")
                return False

            max_x, max_y = PYRAMID_LAYERS[z]
            is_valid = 0 <= x < max_x and 0 <= y < max_y
            print(f"y,x,z: {y} {x} {z}")
            if not is_valid:
                return False

        return True


"""
        for y, x, z in self.piece:

            if y > z_base or y < 0:
                # print(f"faaallsee y: {y}")
                print(f"Invalid y:{y}")

                return False

            if self.z_base - y in PYRAMID_LAYERS:
                max_x, max_y = PYRAMID_LAYERS[self.z_base - y]
            else:
                print(f"Invalid pyramid layer: z_base: {self.z_base} - y:{y}")
                return False

            max_x, max_y = PYRAMID_LAYERS[self.z_base-y]

            if not (0 <= x < max_x) or not (0 <= y < max_y):
                print(f"x_max {max_x} - y:{max_y}")

                return False

        return True
"""


def find_transformations_in_diagonal(z_base=4, piece=None):
    positions = set()

    for y in range(z_base):
        triangle = Triangle(piece, z_base=z_base, x_base=0)

        for i in range(y):

            if triangle.is_valid_triangle():
                positions.add(tuple(sorted(triangle.get_piece_in_pyramid())))
                # print(triangle.get_piece_in_pyramid())
            triangle.go_down()

        for x in range(y):
            triangle.go_right()
            if triangle.is_valid_triangle():
                # print(triangle.get_piece_in_pyramid())
                positions.add(tuple(sorted(triangle.get_piece_in_pyramid())))

    return positions


piece_k = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]


def rotation_z(angle_degrees):

    angle_rad = np.deg2rad(angle_degrees)

    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad), 0],
        [np.sin(angle_rad), np.cos(angle_rad), 0],
        [0, 0, 1],
    ])
    # return rotation_matrix
    return np.round(rotation_matrix, decimals=10)


transformed_piece = [np.dot(rotation_z(-180), point)
                     for point in piece_k]



triangle = Triangle(transformed_piece, z_base=1, x_base=0)
#triangle.go_down()
#triangle.go_down()

print(triangle.get_piece_in_pyramid())


def normalize(transformed_piece):
    min_y = min(y for y, x, z in transformed_piece)
    min_x = min(x for y, x, z in transformed_piece)
    min_z = min(z for y, x, z in transformed_piece)

    normalized = [(y-min_y, x-min_x, z-min_z)
                  for y, x, z in transformed_piece]

    return normalized


transformed_piece = normalize(transformed_piece)
print(transformed_piece)

# for x in range(1,4):
#     transformations = find_transformations_in_diagonal(z_base=4,x_base=x, piece=piece_k)


# print(find_transformations_in_diagonal(piece=transformed_piece, z_base=1))
