import numpy as np

class Solver:
    PYRAMID_LAYERS = {
        0: (5, 5),
        1: (4, 4),
        2: (3, 3),
        3: (2, 2),
        4: (1, 1)
    }

    def __init__(self, count_squares, width_incidence_row, pieces, vertical_pieces):
        self.count_squares = count_squares
        self.width_incidence_row = width_incidence_row
        self.pieces = pieces
        self.vertical_pieces = vertical_pieces

    @staticmethod
    def cell_id(x, y, z):
        offset = sum((5-l)*(5-l) for l in range(int(z)))
        return offset + x * (5-z) + y

    @staticmethod
    def cell_position(cell_id):
        pyramid_size = 5
        cumulative_cells = 0
        for z in range(pyramid_size):
            layer_size = (pyramid_size - z) ** 2
            if cumulative_cells + layer_size > cell_id:
                break
            cumulative_cells += layer_size
        local_index = cell_id - cumulative_cells
        layer_width = pyramid_size - z
        x = local_index % layer_width
        y = local_index // layer_width
        return (y, x, z)

    @staticmethod
    def is_valid_coordinate(x, y, z):
        if z not in Solver.PYRAMID_LAYERS:
            return False
        max_x, max_y = Solver.PYRAMID_LAYERS[z]
        return 0 <= x < max_x and 0 <= y < max_y

    @staticmethod
    def rotation_z(angle_degrees):
        angle_rad = np.deg2rad(angle_degrees)
        rotation_matrix = np.array([
            [np.cos(angle_rad), -np.sin(angle_rad), 0],
            [np.sin(angle_rad), np.cos(angle_rad), 0],
            [0, 0, 1]
        ])
        return np.round(rotation_matrix, decimals=10)

    @staticmethod
    def rotation_first_axis(angle_degrees):
        angle_rad = np.deg2rad(angle_degrees)
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle_rad), -np.sin(angle_rad)],
            [0, np.sin(angle_rad), np.cos(angle_rad)]
        ])
        return np.round(rotation_matrix, decimals=10)

    @staticmethod
    def rotation_second_axis(angle_degrees):
        angle_rad = np.deg2rad(angle_degrees)
        rotation_matrix = np.array([
            [np.cos(angle_rad), 0, np.sin(angle_rad)],
            [0, 1, 0],
            [-np.sin(angle_rad), 0, np.cos(angle_rad)]
        ])
        return np.round(rotation_matrix, decimals=10)

    @staticmethod
    def reflection_matrix(plane):
        if plane == '':
            return np.eye(3)
        elif plane == 'xz':
            return np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
        elif plane == 'yz':
            return np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])

    @staticmethod
    def normalize(transformed_piece):
        min_y = min(y for y, x, z in transformed_piece)
        min_x = min(x for y, x, z in transformed_piece)
        min_z = min(z for y, x, z in transformed_piece)
        normalized = [(y-min_y, x-min_x, z-min_z)
                      for y, x, z in transformed_piece]
        return normalized

    def generate_rotations(self, piece):
        unique_rotations = set()
        square_angles = [0, 90, 180, 270]
        reflections = ['', 'xz', 'yz']
        for reflection in reflections:
            for angle in square_angles:
                rotation_matrix = self.reflection_matrix(
                    reflection) @ self.rotation_z(angle)
                transformed_piece = [np.dot(rotation_matrix, point)
                                     for point in piece]
                normalized = self.normalize(transformed_piece)
                unique_rotations.add(tuple(sorted(normalized)))
        return unique_rotations

    def generate_transformations(self, piece):
        all_transformations = set()
        rotations = self.generate_rotations(piece)
        for rotation in rotations:
            for dz in range(5):
                max_x, max_y = self.PYRAMID_LAYERS[dz]
                for dy in range(max_y):
                    for dx in range(max_x):
                        translated = [(y+dy, x+dx, dz)
                                      for y, x, _ in rotation]
                        if all(self.is_valid_coordinate(x, y, z) for x, y, z in translated):
                            all_transformations.add(
                                tuple(sorted(translated)))
        return all_transformations

    def generate_incidence_matrix(self):
        incidence_matrix = np.empty((0, self.width_incidence_row), dtype=bool)
        for piece_id, piece in self.pieces.items():
            for transformation in self.generate_transformations(piece):
                occupied_ids = [self.cell_id(x, y, z)
                                for x, y, z in transformation]
                row_incidence = np.zeros(self.width_incidence_row)
                for cell in occupied_ids:
                    row_incidence[int(cell)] = 1
                row_incidence[piece_id] = 1
                incidence_matrix = np.append(
                    incidence_matrix, [row_incidence], axis=0)
        for piece_id, vertical_piece in self.vertical_pieces.items():
            occupied_ids = [self.cell_id(x, y, z)
                            for x, y, z in vertical_piece]
            row_incidence = np.zeros(self.width_incidence_row)
            for cell in occupied_ids:
                row_incidence[int(cell)] = 1
            row_incidence[piece_id] = 1
            incidence_matrix = np.append(
                incidence_matrix, [row_incidence], axis=0)
        return incidence_matrix


# Example Usage:
pieces = {55: [(0, 0, 0), (1, 0, 0), (0, 1, 0)], 56: [(0, 0, 0), (1, 1, 0)]}
vertical_pieces = {57: [(0, 1, 0), (0, 1, 1)]}
solver = Solver(count_squares=55, width_incidence_row=67,
                pieces=pieces, vertical_pieces=vertical_pieces)
incidence_matrix = solver.generate_incidence_matrix()
print(incidence_matrix)
