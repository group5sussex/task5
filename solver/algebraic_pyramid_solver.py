

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

"""
---neww---

diagonal 1: from [y1 x0] => [y0 x1] to [y4 x0] to [y0 x4]
diagonal 2: from [y4 x1] => [y1 x4] to [y4 x3] to [y3 x4]

intitial pyramid values for peacce:

diagonal1: z=0, bases [y1 x0], [y2,x0], [y3 x0], [y4 x0]
diagonal2: z=0, [y4, x1], [y4,x2], [y4,x3]

when go up:
    in pyramid piece: z+1, y-1, x=x
    in diagonal: y+1

when go right:
    in pyramid piece: y-1 x+1 z=z
    in diagonal: x+1

convert diagonal coordinates to pyramid coordinate:

for 4,3,2,1

first:
in piece:
    change y to -y
then:
in pyramid_piece:
    z_p_initial=y-x
    y_p_initial=(4,3,2,1)-y
    x_p_initial=(4,3,2,1)-x






second
in pyramid:
    z_initial= y-x

"""

y_values = []
x_values1 = ['x0']
x_values2 = ['x1', 'x2', 'x3']


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

def cell_id(x, y, z):
    offset = sum((5-l)*(5-l) for l in range(int(z)))
    return offset + x * (5-z) + y


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

        if not (0 <= z_base <= 4 and 0 <= x_base <= 3):
            raise ValueError(
                f"Invalid x_base:{x_base}  or z_base: {z_base}")

        # if x_base > 0 and x_base+z_base != 4:
        #     raise ValueError(
        #         f"Invalid x_base+z_base : x_base:{x_base}  or z_base: {z_base}")

        self.piece = piece
        self.z_base = z_base
        self.x_base = x_base
        self.piece_in_pyramid = []

        self.initiate_piece_in_triangle()

    def get_piece_in_pyramid(self):

        # self.piece_in_pyramid = [
        #     (self.z_base-z-x+self.x_base, x+self.x_base, z)for y, x, z in self.piece]

        if (self.z_base != 0):
            self.piece_in_pyramid = [
                (self.z_base-z-x+self.x_base, x+self.x_base, z)for y, x, z in self.piece]

        if (self.x_base != 0):
            self.piece_in_pyramid = [
                (4-z-x, x+self.x_base, z)for y, x, z in self.piece]

        return self.piece_in_pyramid

    def get_triangle_piece(self):
        return self.piece

    def initiate_piece_in_triangle(self):
        # z = z_base-x-y
        # make every y =-y
        # for every piece y =y-x
        self.piece = [(-y-x, x, -y-x)for y, x, z in self.piece]

    def go_up(self):
        self.piece = [(y+1, x, z+1)for y, x, z in self.piece]

    def go_right(self):
        self.piece = [(y, x+1, z)for y, x, z in self.piece]

        # print("go right")

    def is_valid_triangle(self):

        for y, x, z in self.piece:

            if not (0 <= y <= z_base):
                # print("false")
                return False

            max_x, max_y = PYRAMID_LAYERS[y]
            is_valid = (0 <= x < max_x)
            # print(f"y,x,z: {y} {x} {z}")
            if is_valid is False:
                return False

        for y, x, z in self.get_piece_in_pyramid():
            if z not in PYRAMID_LAYERS:
                # print("false")
                return False

            max_x, max_y = PYRAMID_LAYERS[z]
            is_valid = 0 <= x < max_x and 0 <= y < max_y
            # print(f"y,x,z: {y} {x} {z}")
            if not is_valid:
                return False

        return True


def generate_piece_vertical_transformations(piece):
    transformations = set()
    rotations = [0, 90, 180, 270]

    for rotation in rotations:

        transformed_piece = [np.dot(rotation_z(rotation), point)
                             for point in piece_k]

        piece_normalized = normalize(transformed_piece)

        for z_base in range(1, 5):
            positions_with_z_base = generate_base_vertical_transformations(
                z_base=z_base, piece=piece_normalized)

            transformations.update(positions_with_z_base)

        # print(len(transformations))

        for x_base in range(1, 4):
            positions_with_x_base = generate_base_vertical_transformations(piece=piece_normalized,
                                                                           x_base=x_base)
            transformations.update(positions_with_x_base)

    return transformations


def generate_base_vertical_transformations(z_base=0, x_base=0, piece=None):
    positions = set()

    base = 0
    if x_base != 0:
        base = x_base

    if z_base != 0:
        base = z_base

    for y in range(1, base):
        triangle = Triangle(piece, z_base=z_base, x_base=x_base)

        for i in range(y+1):
            triangle.go_up()
            #print("go up")
            if triangle.is_valid_triangle():
                positions.add(tuple(sorted(triangle.get_piece_in_pyramid())))

        for x in range(base):
            triangle.go_right()
            #print("go right")

            if triangle.is_valid_triangle():
                positions.add(tuple(sorted(triangle.get_piece_in_pyramid())))

    return positions


def rotation_z(angle_degrees):

    angle_rad = np.deg2rad(angle_degrees)

    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad), 0],
        [np.sin(angle_rad), np.cos(angle_rad), 0],
        [0, 0, 1],
    ])
    # return rotation_matrix
    return np.round(rotation_matrix, decimals=10)


def normalize(transformed_piece):
    min_y = min(y for y, x, z in transformed_piece)
    min_x = min(x for y, x, z in transformed_piece)
    min_z = min(z for y, x, z in transformed_piece)

    normalized = [(y-min_y, x-min_x, z-min_z)
                  for y, x, z in transformed_piece]

    return normalized


count_squares = 55
width_incidence_row = 67


class VerticalTransformation():

    def generate_incidence_matrix_vertical(pieces):
        for piece_id, piece in pieces.items():

            incidence_matrix = np.empty((0, width_incidence_row), dtype=bool)

            for piece_id, piece in pieces.items():
                for transformation in generate_piece_vertical_transformations(piece):
                    occupied_ids = [cell_id(x, y, z) for x, y, z in transformation]
                    row_incidence = np.zeros(width_incidence_row)

                    for cell in occupied_ids:
                        row_incidence[int(cell)] = 1

                    row_incidence[piece_id] = 1

                    incidence_matrix = np.append(
                        incidence_matrix, [row_incidence], axis=0)

        return incidence_matrix


piece_a = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 2, 0), (1, 2, 0)]
piece_b = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, -1, 0), (1, -2, 0)]
piece_c = [(0, 0, 0), (1, 0, 0), (1, -1, 0), (2, 0, 0), (2, 1, 0)]
piece_d = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, -1, 0)]
piece_e = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, -1, 0), (1, 2, 0)]
piece_f = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (1, -1, 0)]
piece_g = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, -1, 0)]
piece_h = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (2, 0, 0)]
piece_i = [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 2, 0), (2, 2, 0)]
piece_j = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0)]
piece_k = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]
piece_l = [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 2, 0), (2, 2, 0)]


pieces = {count_squares: piece_a,
          count_squares+1: piece_b,
          count_squares+2: piece_c,
          count_squares+3: piece_d,
          count_squares+4: piece_e,
          count_squares+5: piece_f,
          count_squares+6: piece_g,
          count_squares+7: piece_h,
          count_squares+8: piece_i,
          count_squares+9: piece_j,
          count_squares+10: piece_k,
          count_squares+11: piece_l,

          }
#print(len(VerticalTransformation().generate_incidence_matrix_vertical(pieces)))
#print(len(generate_incidence_matrix_vertical(pieces)))



