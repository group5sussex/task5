import numpy as np
from xcover import covers_bool

import sys
import numpy

pyramid = [
    np.zeros((5, 5), dtype=int),
    np.zeros((4, 4), dtype=int),
    np.zeros((3, 3), dtype=int),
    np.zeros((2, 2), dtype=int),
    np.zeros((1, 1), dtype=int)

]

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


def reflection_matrix(plane):
    """Generate a reflection matrix for a given plane ('xy', 'xz', 'yz')."""
    if plane == 'xy':
        return np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])
    elif plane == 'xz':
        return np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    elif plane == 'yz':
        return np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])


def generate_rotations(piece):

    first_axis_rotations = [  # Rotations around First-axis
        np.eye(3),
        [[1, 0, 0], [0, 0, -1], [0, 1, 0]],
        [[1, 0, 0], [0, -1, 0], [0, 0, -1]],
        [[1, 0, 0], [0, 0, 1], [0, -1, 0]],
    ]

    second_axis_rotations = [  # Rotations around Second-axis
        np.eye(3),
        [[0, 0, 1], [0, 1, 0], [-1, 0, 0]],
        [[-1, 0, 0], [0, 1, 0], [0, 0, -1]],
        [[0, 0, -1], [0, 1, 0], [1, 0, 0]],
    ]

    third_axis_rotations = [  # Rotations around Z-axis
        np.eye(3),
        [[0, -1, 0], [1, 0, 0], [0, 0, 1]],
        [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
        [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]
    ]

    unique_rotations = set()

    angles = [0, 60, 120, 180, 240, 300, 360]
    planes = ['xy', 'xz', 'yz']

    for reflection in planes:
        for first_matrix in first_axis_rotations:
            for second_matrix in second_axis_rotations:
                for z_angle in angles:

                    reflection_mat = reflection_matrix(reflection)

                    rotation_matrix = rotation_z(
                        z_angle) @ np.array(second_matrix) @ np.array(first_matrix)

                    transformed_piece = [np.dot(rotation_matrix, point)
                                         for point in piece]

                    # full_transform = rotation_matrix @ reflection_mat

                   # transformed_piece = [
                   #     tuple(np.round(np.dot(full_transform, [x, y, z])).astype(int)) for x, y, z in piece
                    # ]
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


pyramid_layers = {
    z: [(x, y, z) for x in range(5 - z)
        for y in range(5 - z)]  # Add z to each tuple
    for z in range(5)
}


def generate_transformations2(piece):
    all_transformation = set()
    rotations = generate_rotations(piece)

    # Consider all valid positions within the pyramid layers

    # Consider all valid positions within the pyramid layers
    for layer in pyramid_layers.values():  # Iterate over all layers
        for dx, dy, dz in layer:
            positioned_piece = [
                (x + dx, y + dy, z + dz) for x, y, z in piece
            ]

            # Check if all cells are within the bounds of the pyramid
            if all((px, py, pz) in pyramid_layers[pz] for px, py, pz in positioned_piece):
                all_transformation.add(tuple(sorted(positioned_piece)))

    return all_transformation


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


# def reflection_matrix(plane):
#     """Generate a reflection matrix for a given plane ('xy', 'xz', 'yz')."""
#     if plane == 'xy':
#         return np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])
#     elif plane == 'xz':
#         return np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
#     elif plane == 'yz':
#         return np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])


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
incidence_matrix = generate_incidence_matrix(pieces)
for solusion in covers_bool(incidence_matrix):
    print(solusion)

print(len(incidence_matrix))
# print(len(list(covers_bool(incidence_matrix))))


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
