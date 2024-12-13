import numpy as np
from xcover import covers_bool
import copy
from django.http import JsonResponse
import json
# from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
    def is_in_lower_left(y, x, z):
        return y + x <= 4

    @staticmethod
    def is_in_second_diagonal(y, x, z):  # is_in_lower_left
        # return 0 <= (y - x) <= 4
        return y >= x and 0 <= y < 5 and 0 <= x < 5

    @staticmethod
    def Pieces(piece_id):
        return Board.PIECES.get(piece_id, None)

    @staticmethod
    def list_pieces():
        return Board.PIECES

    @staticmethod
    def cell_position(cell_id):

        pyramid_size = 5  # Base layer size (5x5)

        # Step 1: Determine the layer (z) where the cell belongs
        cumulative_cells = 0
        for z in range(pyramid_size):
            layer_size = (pyramid_size - z) ** 2  # Number of cells in layer z
            if cumulative_cells + layer_size > cell_id:
                break
            cumulative_cells += layer_size

        # Step 2: Find local index within the layer
        local_index = cell_id - cumulative_cells

        # Step 3: Map local index to (x, y) within the layer
        layer_width = pyramid_size - z
        x = local_index % layer_width
        y = local_index // layer_width

        return (y, x, z)

    @staticmethod
    def convert_incidence_to_pieces(solusion, incidences):

        pieces = {}

        for incidence_row_index in solusion:
            incidence = incidences[incidence_row_index]
            piece_cell_ids = np.where(incidence[0:55] == 1)[0]
            piece_id = int(np.where(incidence[55:] == 1)[
                           0][0])+Board.COUNT_SQUARES

            piece_points = []
            for cell_id in piece_cell_ids:
                point = Board.cell_position(int(cell_id))
                piece_points.append(tuple(map(int, point)))

            pieces[piece_id] = piece_points

        return pieces


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
                    if diagonal_check == Board.is_in_upper_left:
                        translated_piece = [(y, x, 4-x-y)
                                            for y, x, z in translated_piece]
                    elif diagonal_check == Board.is_in_second_diagonal:
                        translated_piece = [(x, x, y-x)
                                            for y, x, z in translated_piece]

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
            first_diagonal_transformations = generate_3d_transformations(
                piece, Board.is_in_upper_left)

            second_diagonal_transformations = generate_3d_transformations(
                piece, Board.is_in_second_diagonal)

            transformations_3d = set()
            transformations_3d.update(first_diagonal_transformations)
            transformations_3d.update(second_diagonal_transformations)

            for transformation in transformations_3d:
                occupied_ids = [cell_id(x, y, z) for x, y, z in transformation]
                row_incidence = np.zeros(Board.WIDTH_INCIDENCE)

                for cell in occupied_ids:
                    row_incidence[int(cell)] = 1

                row_incidence[piece_id] = 1

                incidence_matrix = np.append(
                    incidence_matrix, [row_incidence], axis=0)

    return incidence_matrix


def generate_incidence_matrix(pieces, initial_state={}):

    new_pieces = copy.deepcopy(Board.list_pieces())

    for key in initial_state.keys():
        if key in new_pieces:
            del new_pieces[key]

    incidences_2d = generate_2d_incidence_matrix(new_pieces)
    incidences_3d = generate_3d_incidence_matrix(new_pieces)

    incidence_matrix = np.vstack((incidences_2d, incidences_3d))

    for piece_id, piece in initial_state.items():

        occupied_ids = [cell_id(x, y, z) for x, y, z in piece]

        row_incidence = np.zeros(Board.WIDTH_INCIDENCE)

        for cell in occupied_ids:
            row_incidence[int(cell)] = 1

        row_incidence[piece_id] = 1

        incidence_matrix = np.append(
            incidence_matrix, [row_incidence], axis=0)

    return incidence_matrix


@csrf_exempt
def submit(request):
    # initial_state = {56: [(0, 1, 0), (0, 1, 1), (1, 2, 1), (0, 1, 2), (1, 2, 2)]}
    # data = request.GET.get('positions', '{}')
    data = json.loads(request.body)
    # initial_state = data.get('initial_state', [])

    initial_state = {}
    initial_state_list = data.get('initial_state', [])
    for state in initial_state_list:
        for key, value in state.items():
            # Convert string keys to integers if necessary
            key = int(key)
            # Convert lists of lists to lists of tuples
            initial_state[key] = [tuple(coords) for coords in value]

    print(initial_state)

    incidence_matrix = generate_incidence_matrix(
        pieces=Board.list_pieces(), initial_state=initial_state)

    result = []

    for solution in covers_bool(incidence_matrix):
        solution_board = Board.convert_incidence_to_pieces(
            solution, incidence_matrix)
        result.append(solution_board)

    print("solusions: ", result)
    print("len solusions: ", len(result))

    response = JsonResponse(result, safe=False)
    # print("solusions: " ,response)
    return response


# initial_state = {
#     56: [(0, 1, 0), (0, 1, 1), (1, 2, 1), (0, 1, 2), (1, 2, 2)],
#     57: [(2, 1, 1), (1, 1, 2), (0, 2, 2), (0, 1, 3), (1, 0, 3)],
#     65: [(0, 0, 3), (0, 0, 4), (1, 1, 3)]}
