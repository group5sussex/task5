import numpy as np

# Define the diagonal check function for the 5×5 board


def is_in_upper_left(y, x, z):
    """Check if a cell is in the upper-left triangular half."""
    return y + x <= 4


def is_in_lower_right(y, x, z):
    """Check if a cell is in the lower-right triangular half."""
    return y + x > 4

# Rotation matrices for (y, x, z)


def rotation_matrix_z(angle_degrees):
    """Generate a 2D rotation matrix for rotation around the z-axis."""
    angle_rad = np.deg2rad(angle_degrees)
    return np.array([
        [np.cos(angle_rad), -np.sin(angle_rad), 0],
        [np.sin(angle_rad), np.cos(angle_rad), 0],
        [0, 0, 1]
    ]).round(decimals=10)


def generate_rotations(piece):
    """Generate all rotations of a piece."""
    angles = [0, 90, 180, 270]
    rotations = []
    for angle in angles:
        rotation = rotation_matrix_z(angle)
        rotated_piece = [tuple(np.dot(rotation, [y, x, z]))
                         for y, x, z in piece]
        # Normalize to avoid duplicates
        rotations.append(normalize(rotated_piece))
    return rotations


def normalize(piece):
    min_y = min(y for y, x, z in piece)
    min_x = min(x for y, x, z in piece)
    min_z = min(z for y, x, z in piece)

    return [(int(y - min_y), int(x - min_x), int(z - min_z)) for y, x, z in piece]

# Translation function


def translate_piece(piece, dy, dx):
    """Translate a piece by (dy, dx)."""
    return [(y + dy, x + dx, z) for y, x, z in piece]


def is_valid_in_diagonal(piece, check_function):
    """Check if a piece is valid within the diagonal region."""
    return all(check_function(y, x, z) for y, x, z in piece)

# Generate transformations


def generate_diagonal_transformations(piece, diagonal_check):
    """
    Generate all valid transformations of a piece within the diagonal half.

    Args:
        piece: List of (y, x, z) tuples representing the piece.
        diagonal_check: Function to check if a cell is within the diagonal half.

    Returns:
        Set of unique valid transformations.
    """
    valid_transformations = set()
    rotations = generate_rotations(piece)

    # Translate each rotation within the board
    piece_height = max(y for y, x, z in piece) + 1
    piece_width = max(x for y, x, z in piece) + 1

    for dy in range(5 - piece_height + 1):  # Restrict translation to board height
        for dx in range(5 - piece_width + 1):  # Restrict translation to board width
            translated_piece = translate_piece(piece, dy, dx)
            if is_valid_in_diagonal(translated_piece, diagonal_check):
                valid_transformations.add(tuple(sorted(translated_piece)))

    return valid_transformations


# Example piece
# initiate
# z =-x
# after finishing transformations z=4-(x+z) or mayber 4-z
piece_k = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]  # Example: L-shape with z = 0

# Generate valid transformations for the upper-left half
upper_left_transformations = generate_diagonal_transformations(
    piece_k, is_in_upper_left)
print(
    f"Total transformations in upper-left half: {len(upper_left_transformations)}")
for transformation in upper_left_transformations:
    transformation = [(y, x, 4-x-y) for y, x, z in transformation]

    print(transformation)

# Generate valid transformations for the lower-right half
# lower_right_transformations = generate_diagonal_transformations(
#     piece_k, is_in_upper_left)
# print(
#     f"Total transformations in lower-left half: {len(lower_right_transformations)}")
# for transformation in lower_right_transformations:


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
