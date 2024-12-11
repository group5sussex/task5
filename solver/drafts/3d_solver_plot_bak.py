import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def rotate_z(points, theta):
    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])
    return [tuple(np.dot(rotation_matrix, point)) for point in points]


def plot_polyomino1(points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for x, y, z in points:
        # Draw each cube as a set of faces
        ax.bar3d(x, y, z, 1, 1, 1, shade=True)  # A cube of size 1
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


# Example usage
piece_k = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]
# piece_k = [(0, 0, 0), (0, 1, 0), (1, 1, 0)]


# Rotate 90 degrees around z-axis
# rotated_polyomino = rotate_z(np.array(piece_k), 0)


# plot_polyomino(piece_k)


def rotate(points, matrix):
    """Apply a rotation matrix to a list of points."""
    return [tuple(np.dot(matrix, point)) for point in points]


def get_rotation_matrices():
    """Generate rotation matrices for 90-degree increments about x, y, and z axes."""
    angles = [0, math.pi / 2, math.pi, 3 * math.pi / 2]
    matrices = []
    for theta_x in angles:
        R_x = np.array([
            [1, 0, 0],
            [0, math.cos(theta_x), -math.sin(theta_x)],
            [0, math.sin(theta_x), math.cos(theta_x)],
        ])
        for theta_y in angles:
            R_y = np.array([
                [math.cos(theta_y), 0, math.sin(theta_y)],
                [0, 1, 0],
                [-math.sin(theta_y), 0, math.cos(theta_y)],
            ])
            for theta_z in angles:
                R_z = np.array([
                    [math.cos(theta_z), -math.sin(theta_z), 0],
                    [math.sin(theta_z), math.cos(theta_z), 0],
                    [0, 0, 1],
                ])
                matrices.append(R_z @ R_y @ R_x)
    return matrices


def get_all_rotations(points):
    """Get all unique rotations of the shape."""
    rotation_matrices = get_rotation_matrices()
    rotations = set()
    for matrix in rotation_matrices:
        rotated = rotate(points, matrix)
        # Convert to a sorted tuple to ensure uniqueness
        rotations.add(tuple(sorted(rotated)))
    return rotations


def plot_polyomino_3d(polyomino, ax, title=""):
    """Plot a single polyomino configuration in 3D."""
    for x, y, z in polyomino:
        # Draw each cube as a rectangular prism
        ax.bar3d(x, y, z, 1, 1, 1, shade=True,
                 color='skyblue', edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio


def visualize_all_rotations(rotations):
    """Visualize all rotations in a grid."""
    fig = plt.figure(figsize=(16, 16))
    num_rotations = len(rotations)
    cols = 4  # Number of columns in the grid
    # Compute rows to fit all rotations
    rows = (num_rotations + cols - 1) // cols

    for i, rotation in enumerate(rotations):
        ax = fig.add_subplot(rows, cols, i + 1, projection='3d')
        plot_polyomino_3d(rotation, ax, title=f"Rotation {i+1}")

    plt.tight_layout()
    plt.show()


# Example 3D polyomino: A T-shape lying flat on the XY plane
polyomino = [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 2, 0), (2, 2, 0)]

# Compute all unique rotations
all_rotations = get_all_rotations(polyomino)

# Convert set of unique rotations back to lists of tuples
all_rotations_list = [list(rotation) for rotation in all_rotations]

# Visualize all unique rotations
visualize_all_rotations(all_rotations_list)
