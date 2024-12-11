import numpy as np


def rotation_x(angle_degrees):
    angle_rad = np.deg2rad(angle_degrees)
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(angle_rad), -np.sin(angle_rad)],
        [0, np.sin(angle_rad), np.cos(angle_rad)]
    ])
    return rotation_matrix


def rotation_y(angle_degrees):
    angle_rad = np.deg2rad(angle_degrees)
    rotation_matrix = np.array([
        [np.cos(angle_rad), 0, np.sin(angle_rad)],
        [0, 1, 0],
        [-np.sin(angle_rad), 0, np.cos(angle_rad)]
    ])
    return rotation_matrix


def rotation_z(angle_degrees):

    angle_rad = np.deg2rad(angle_degrees)

    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad), 0],
        [np.sin(angle_rad), np.cos(angle_rad), 0],
        [0, 0, 1],
    ])
    # return rotation_matrix
    return np.round(rotation_matrix, decimals=10)


def stretch_matrix():
    return np.array([
        [2, 0, 0],
        [0, 2, 0],
        [0, 0, np.sqrt(2)]
    ])


def generate_rotations_3d(piece):
    unique_rotations = set()

    # Define rotation matrices
    rot_x_90 = rotation_x(90)
    rot_y_45 = rotation_y(45)
    rot_z_45p = rotation_z(45)
    rot_z_45m = rotation_z(-45)
    stretch = stretch_matrix()

    # Create orientations in z=0 plane by appending z-coordinates to 2D-orientations
    piece_3d = [np.array([x, y, 0]) for x, y, _ in piece]

    # Generate orientations parallel to x=y plane and x=-y plane
    orientations = [
        piece_3d,
        [np.dot(rot_x_90 @ rot_y_45 @ rot_z_45p @ stretch, point)
         for point in piece_3d],
        [np.dot(rot_x_90 @ rot_y_45 @ rot_z_45m @ stretch, point)
         for point in piece_3d]
    ]

    # Convert to integer and shift operations
    for orientation in orientations:
        orientation = np.array(orientation, dtype=int)
        orientation[:, 0] -= np.min(orientation[:, 0])
        orientation[:, 1] -= np.min(orientation[:, 1])
        orientation[:, 2] -= np.min(orientation[:, 2])

        # Shift into even coordinates at z=0
        el0 = np.where(orientation[:, 2] == 0)[0][0]
        if orientation[el0, 0] % 2 != 0:
            orientation[:, 0] += 1
        if orientation[el0, 1] % 2 != 0:
            orientation[:, 1] += 1

        # Add to unique rotations
        unique_rotations.add(tuple(map(tuple, orientation)))

    return unique_rotations


def generate_transformations(piece):
    all_transformation = set()
    rotations = generate_rotations_3d(piece)

    for rotation in rotations:
        for z in range(5):
            max_x, max_y = PYRAMID_LAYERS[z]
            for dy in range(max_y):
                for dx in range(max_x):
                    translated = [(y+dy, x+dx, z) for y, x, z in rotation]
                    if all(is_valid_coordinate(x, y, z) for x, y, z in translated):
                        all_transformation.add(tuple(sorted(translated)))

    return all_transformation


# Example usage
piece_a = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]
rotations = generate_rotations_3d(piece_a)
for rotation in rotations:
    print(rotation)
