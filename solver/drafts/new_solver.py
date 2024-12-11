import numpy as np
from xcover import covers_bool
import sys
import numpy
import math

PYRAMID_LAYERS = {
    0: (5, 5),
    1: (4, 4),
    2: (3, 3),
    3: (2, 2),
    4: (1, 1)
}

pyramid = {0: np.zeros((5, 5)),
           1: np.zeros((4, 4)),
           2: np.zeros((3, 3)),
           3: np.zeros((2, 2)),
           4: np.zeros((1, 1))}


def cell_id(x, y, z):
    offset = sum((5-l)*(5-l) for l in range(int(z)))
    return offset + x * (5-z) + y


def cell_position(id):
    if id > 54 or id < 0:
        raise Exception("id out of boud")

    z = 0

    for i in [5, 4, 3, 2, 1]:
        if id - i*i >= 0:
            id -= i*i
            z += 1
        else:
            break

    layer_width, _ = PYRAMID_LAYERS[z]

    x = id % layer_width
    y = id // layer_width

    return (y, x, z)


def is_valid_coordinate(x, y, z):
    if z not in PYRAMID_LAYERS:
        return False

    max_x, max_y = PYRAMID_LAYERS[z]

    return 0 <= x < max_x and 0 <= y < max_y


def rotation_z(angle_rad):

    return np.array([
        [np.cos(angle_rad), -np.sin(angle_rad), 0],
        [np.sin(angle_rad), np.cos(angle_rad), 0],
        [0, 0, 1],
    ])


def generate_rotations(piece):

    first_axis_rotations = [  # Rotations around First-axis
        np.eye(3),
        [[1, 0, 0], [0, 0, -1], [0, 1, 0]],

    ]


    second_axis_rotations = [  # Rotations around Second-axis
        np.eye(3),
        [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
        [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],
        [[0, 0, -1], [0, 1, 0], [1, 0, 0]],
    ]



    unique_rotations = set()

    angles = [0, 60, 120, 180, 240, 300, 360]

    for first_matrix in first_axis_rotations:
        for second_matrix in second_axis_rotations:
            for z_angle in angles:

                rotation_matrix = rotation_z(
                    z_angle) @ np.array(second_matrix) @ np.array(first_matrix)

                transformed_piece = [np.dot(rotation_matrix, point)
                                     for point in piece]

                min_y = min(y for y, x, z in transformed_piece)
                min_x = min(x for y, x, z in transformed_piece)
                min_z = min(z for y, x, z in transformed_piece)

                normalized = [(y-min_y, x-min_x, z-min_z)
                              for y, x, z in transformed_piece]

                unique_rotations.add(tuple(sorted(normalized)))

    return unique_rotations


def generate_transformations(piece):
    all_transformation = set()
    rotations = generate_rotations(piece)

    for rotation in rotations:
        for z in range(5):
            max_x, max_y = PYRAMID_LAYERS[z]
            for dy in range(max_y):
                for dx in range(max_x):
                    translated = [(y+dy, x+dx, z) for y, x, z in rotation]
                    if all(is_valid_coordinate(x, y, z) for x, y, z in translated):
                        all_transformation.add(tuple(sorted(translated)))

    return all_transformation



def is_within_spherical_boundary(piece, layer_radii):
    """
    Checks if a piece is within the spherical boundary of the pyramid.

    :param piece: List of points (x, y, z) representing the piece.
    :param layer_radii: Dictionary with layer index as key and radius as value.
    :return: True if the piece is valid, False otherwise.
    """
    for x, y, z in piece:
        if z not in layer_radii:
            return False  # Invalid layer
        distance = math.sqrt(x**2 + y**2)
        if distance > layer_radii[z]:
            return False  # Outside the spherical boundary
    return True

# Define the layer radii for the cannonball square pyramid
layer_radii = {
    0: 2.5,  # Base layer (5x5)
    1: 2.0,  # Second layer (4x4)
    2: 1.5,  # Third layer (3x3)
    3: 1.0,  # Fourth layer (2x2)
    4: 0.5   # Topmost layer (1x1)
}

def generate_incidence_matrix(pieces):

    incidence_matrix = np.empty((0, width_incidence_row))

    for piece_id, piece in pieces.items():
        for transformation in generate_transformations(piece):
            occupied_ids = [cell_id(x, y, z) for x, y, z in transformation]
            row_incidence = np.zeros(width_incidence_row)

            for cell in occupied_ids:
                row_incidence[int(cell)] = 1

            row_incidence[piece_id] = 1

            incidence_matrix = np.append(
                incidence_matrix, [row_incidence], axis=0)

    return incidence_matrix


def convert_incidence_to_pieces(solusion, incidences):
    pieces = {}

    for incidence_row_index in solusion:
        incidence = incidences[incidence_row_index]
        piece_cell_ids = np.where(incidence[0:55] == 1)[0]
        piece_id = np.where(incidence[55:] == 1)[0][0]+count_squares

        piece_points = []
        for cell_id in piece_cell_ids:
            point = cell_position(cell_id)
            piece_points.append(point)

        pieces[piece_id] = piece_points

    return pieces


def draw_pyramid(pieces):
    pyramid = {0: np.zeros((5, 5)),
               1: np.zeros((4, 4)),
               2: np.zeros((3, 3)),
               3: np.zeros((2, 2)),
               4: np.zeros((1, 1))}

    for piece_id in pieces:
        for y, x, z in pieces[piece_id]:
            pyramid[z][y][x] = piece_id

    for layer in pyramid:
        print(pyramid[layer])


count_squares = 55
width_incidence_row = 67
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


pieces_k = {
    count_squares+10: piece_k,
}


# def can_fill_topmost_point(transformations):
#     # Coordinates of the topmost point in the pyramid
#     topmost_point = (0, 0, 4)
#     for transformation in transformations:
#         if topmost_point in transformation:
#             return True
#     return False


# for piece_id, piece in pieces.items():
#     transformations = generate_transformations(piece)

#     if can_fill_topmost_point(transformations):
#         print("This piece can fill the topmost point.")

# piece = [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 2, 0), (2, 2, 0)]


# print(len(generate_rotations(piece)))
# incidence_matrix = generate_incidence_matrix(pieces)

# # print(len(list(covers_bool(incidence_matrix))))
# for solusion in covers_bool(incidence_matrix):
#     print(solusion)
# print(len(incidence_matrix))
# print(cell_position(0))   # (0, 0, 0) (Base layer)
# print(cell_position(41))  # (4, 4, 0) (Last cell in base layer)
# print(cell_position(25))  # (0, 0, 1) (First cell in second layer)
# print(cell_position(54))

# before unstaging

# print(cell_id(0, 0, 4))


# for i in range(67):

#     rows = np.where(incidence_matrix[:, i] == 1)[0]
#     if (len(rows) == 0):
#         print(f"ith:{i}")
#         print("errrorrr ")

# numpy.set_printoptions(threshold=sys.maxsize)
# print(generate_incidence_matrix(pieces))

# print(len(list(covers_bool(incidence_matrix))))

# def pyramid(x, y, z):
#     return pyramid[z][y][x]

# def find_all_positions():
#     pass

# def is_valid_position():
#     pass
# [8904, 3806, 7008, 5897, 8103, 4444, 9782, 826, 1731, 315, 3161, 10640]
incidence_matrix = generate_incidence_matrix(pieces)
for solusion in covers_bool(incidence_matrix):
    pieces = convert_incidence_to_pieces(solusion, incidence_matrix)
    draw_pyramid(pieces)
# pyramid[4][0][0] = 1
# print(pyramid)
# pyramid[0][0][0]=1
# print(pyramid[0][0][0])
