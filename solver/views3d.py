import numpy as np
from xcover import covers_bool
import sys
import numpy
# import exact_cover as ec


from django.http import HttpResponse
from django.http import StreamingHttpResponse
import numpy as np
from xcover import covers_bool
import matplotlib.pyplot as plt
import json
import copy
from django.http import JsonResponse



def submit(request):
    # data = json.loads(request.body.decode('utf-8'))

    incidence_matrix = generate_incidence_matrixx(
        pieces, vertical_pieces)

    result = []

    for solution in covers_bool(incidence_matrix):
        result.append(convert_incidence_to_pieces(solution,incidence_matrix))

    #print(len(result))
    response = JsonResponse(result,safe=False)
    return response


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


def is_valid_coordinate(x, y, z):
    if z not in PYRAMID_LAYERS:
        return False

    max_x, max_y = PYRAMID_LAYERS[z]

    return 0 <= x < max_x and 0 <= y < max_y


def rotation_z(angle_degrees):

    angle_rad = np.deg2rad(angle_degrees)

    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad), 0],
        [np.sin(angle_rad), np.cos(angle_rad), 0],
        [0, 0, 1],
    ])
    # return rotation_matrix
    return np.round(rotation_matrix, decimals=10)


def rotation_first_axis(angle_degrees):
    angle_rad = np.deg2rad(angle_degrees)

    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(angle_rad), -np.sin(angle_rad)],
        [0, np.sin(angle_rad), np.cos(angle_rad)]
    ])

    # return rotation_matrix
    return np.round(rotation_matrix, decimals=10)


def rotation_second_axis(angle_degrees):
    angle_rad = np.deg2rad(angle_degrees)

    rotation_matrix = np.array([
        [np.cos(angle_rad), 0, np.sin(angle_rad)],
        [0, 1, 0],
        [-np.sin(angle_rad), 0, np.cos(angle_rad)]
    ])
    # return rotation_matrix
    return np.round(rotation_matrix, decimals=10)


def reflection_matrix(plane):
    if plane == '':
        return np.eye(3)
    elif plane == 'xz':
        return np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    elif plane == 'yz':
        return np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])


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


def normalize(transformed_piece):
    min_y = min(y for y, x, z in transformed_piece)
    min_x = min(x for y, x, z in transformed_piece)
    min_z = min(z for y, x, z in transformed_piece)

    normalized = [(y-min_y, x-min_x, z-min_z)
                  for y, x, z in transformed_piece]

    return normalized


def generate_transformations(piece):
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


def generate_incidence_matrix(pieces):

    incidence_matrix = np.empty((0, width_incidence_row), dtype=bool)

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


def generate_incidence_matrixx(pieces, vertical_pieces):

    incidence_matrix = generate_incidence_matrix(pieces)

    for piece_id, vertical_piece in vertical_pieces.items():

        occupied_ids = [cell_id(x, y, z) for x, y, z in vertical_piece]
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
        piece_id = int(np.where(incidence[55:] == 1)[0][0])+count_squares

        piece_points = []
        for cell_id in piece_cell_ids:
            point = cell_position(int(cell_id))  # Ensure cell_id is a Python int
            piece_points.append(tuple(map(int, point))) 

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


vertical_pieces = {count_squares+1: [(0, 1, 0), (0, 1, 1), (1, 2, 1), (0, 1, 2), (1, 2, 2)],
                   count_squares+2: [(2, 1, 1), (1, 1, 2), (0, 2, 2), (0, 1, 3), (1, 0, 3)],
                   count_squares+10: [(0, 0, 3), (0, 0, 4), (1, 1, 3)]}
