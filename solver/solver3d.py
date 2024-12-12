import numpy as np
from xcover import covers_bool


class Board:
    COUNT_SQUARES = 55
    WIDTH_INCIDENCE = 67

    PIECES = {
        55: [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 2, 0), (1, 2, 0)],  # piece_a
        56: [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, -1, 0), (1, -2, 0)],  # piece_b
        57: [(0, 0, 0), (1, 0, 0), (1, -1, 0), (2, 0, 0), (2, 1, 0)],  # piece_c
        58: [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, -1, 0)],  # piece_d
        59: [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, -1, 0), (1, 2, 0)],  # piece_e
        60: [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (1, -1, 0)],  # piece_f
        61: [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, -1, 0)],  # piece_g
        62: [(0, 0, 0), (0, 1, 0), (1, 0, 0), (2, 0, 0)],  # piece_h
        63: [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 2, 0), (2, 2, 0)],  # piece_i
        64: [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0), (1, 3, 0)],  # piece_j
        65: [(0, 0, 0), (1, 0, 0), (1, 1, 0)],  # piece_k
        66: [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 2, 0), (2, 2, 0)]   # piece_l

    }
    @staticmethod
    def is_in_upper_left(y, x, z):
        return y + x <= 4

    @staticmethod
    def Pieces(piece_id):
        return Board.PIECES.get(piece_id, None)

    @staticmethod
    def list_pieces():
        return Board.PIECES


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


def reflection_matrix(plane):
    if plane == '':
        return np.eye(3)
    elif plane == 'xz':
        return np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    elif plane == 'yz':
        return np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])


def normalize(transformed_piece):
    min_y = min(y for y, x, z in transformed_piece)
    min_x = min(x for y, x, z in transformed_piece)
    min_z = min(z for y, x, z in transformed_piece)

    normalized = [(y-min_y, x-min_x, z-min_z)
                  for y, x, z in transformed_piece]

    return normalized


def rotation_z(angle_degrees):

    angle_rad = np.deg2rad(angle_degrees)

    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad), 0],
        [np.sin(angle_rad), np.cos(angle_rad), 0],
        [0, 0, 1],
    ])
    # return rotation_matrix
    return np.round(rotation_matrix, decimals=10)


def generate_rotations(piece):

    unique_rotations = set()

    square_angles = [0, 90, 180, 270]
    reflections = ['', 'xz', 'yz']

    for reflection in reflections:

        for angle in square_angles:
            rotation_matrix = reflection_matrix(reflection) @ rotation_z(angle)
            transformed_piece = [np.dot(rotation_matrix, point)
                                 for point in piece]

            normalized = normalize(transformed_piece)

            unique_rotations.add(tuple(sorted(normalized)))

    return unique_rotations


def generate_2d_transformations(piece):
    all_transformation = set()
    rotations = generate_rotations(piece)

    for rotation in rotations:
        for dz in range(5):
            max_x, max_y = PYRAMID_LAYERS[dz]
            for dy in range(max_y):
                for dx in range(max_x):

                    translated = [(y+dy, x+dx, dz) for y, x, _ in rotation]
                    if all(is_valid_coordinate(x, y, z) for x, y, z in translated):
                        all_transformation.add(tuple(sorted(translated)))

    # print(f"len all transformations:  {len(all_transformation)}")

    return all_transformation


def generate_2d_incidence_matrix(pieces):

    incidence_matrix = np.empty((0, Board.WIDTH_INCIDENCE), dtype=bool)

    for piece_id, piece in pieces.items():
        for transformation in generate_2d_transformations(piece):
            occupied_ids = [cell_id(x, y, z) for x, y, z in transformation]
            row_incidence = np.zeros(Board.WIDTH_INCIDENCE)

            for cell in occupied_ids:
                row_incidence[int(cell)] = 1

            row_incidence[piece_id] = 1

            incidence_matrix = np.append(
                incidence_matrix, [row_incidence], axis=0)

    return incidence_matrix

def generate_3d_transformations(piece, diagonal_check):

    valid_transformations = set()
    rotations = generate_rotations(piece)

    # Translate each rotation within the board
    for rotation in rotations:

        piece_height = max(y for y, x, z in piece) + 1
        piece_width = max(x for y, x, z in piece) + 1

        for dy in range(5 - piece_height + 1):  # Restrict translation to board height
            for dx in range(5 - piece_width + 1):  # Restrict translation to board width
                translated_piece = translate_piece(rotation, dy, dx)
                if is_valid_in_diagonal(translated_piece, diagonal_check):
                    translated_piece=[(y, x, 4-x-y) for y, x, z in translated_piece]
                    valid_transformations.add(tuple(sorted(translated_piece)))

    return valid_transformations


def translate_piece(piece, dy, dx):
    return [(y + dy, x + dx, z) for y, x, z in piece]

def is_valid_in_diagonal(piece, check_function):
    return all(check_function(y, x, z) for y, x, z in piece)


def generate_3d_incidence_matrix(pieces):
    for piece_id, piece in pieces.items():

        incidence_matrix = np.empty((0, Board.WIDTH_INCIDENCE), dtype=bool)

        for piece_id, piece in pieces.items():
            upper_left_transformations = generate_3d_transformations(piece, Board.is_in_upper_left)
            for transformation in upper_left_transformations:
                occupied_ids = [cell_id(x, y, z) for x, y, z in transformation]
                row_incidence = np.zeros(Board.WIDTH_INCIDENCE)

                for cell in occupied_ids:
                    row_incidence[int(cell)] = 1

                row_incidence[piece_id] = 1

                incidence_matrix = np.append(
                    incidence_matrix, [row_incidence], axis=0)

    return incidence_matrix


def generate_incidence_matrix(pieces):

    incidences_2d = generate_2d_incidence_matrix(pieces)
    incidences_3d = generate_3d_incidence_matrix(pieces)



    vertical_pieces = {Board.COUNT_SQUARES+1: [(0, 1, 0), (0, 1, 1), (1, 2, 1), (0, 1, 2), (1, 2, 2)],
                   Board.COUNT_SQUARES+2: [(2, 1, 1), (1, 1, 2), (0, 2, 2), (0, 1, 3), (1, 0, 3)],
                   Board.COUNT_SQUARES+10: [(0, 0, 3), (0, 0, 4), (1, 1, 3)]}


    for piece_id, vertical_piece in vertical_pieces.items():
        

        occupied_ids = [cell_id(x, y, z) for x, y, z in vertical_piece]
        row_incidence = np.zeros(Board.WIDTH_INCIDENCE)

        for cell in occupied_ids:
            row_incidence[int(cell)] = 1

        row_incidence[piece_id] = 1

        incidences_3d = np.append(
            incidences_3d, [row_incidence], axis=0)



    incidence_matrix = np.vstack((incidences_2d, incidences_3d))

    return incidence_matrix


def run():
    incidence_matrix=generate_incidence_matrix(Board.list_pieces())
    result = []

    for solution in covers_bool(incidence_matrix):
        print("solusion: ",solution)
    
    print("len: ",len(incidence_matrix))



run()

