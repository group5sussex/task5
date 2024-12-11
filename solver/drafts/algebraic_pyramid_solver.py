

import copy
import numpy as np


"""
- in this diagonal traverser we start from point we imagine this piece is rotated 60 degrees
- any other point when goes right add 1 to its z, 1 to it's y or x

we have
each diagonal has base_length: from 1 to 5
each diagonal has a lowest left point x position and y position


we have to set of diagonal one from upside to downside one from down side to upside
the difference in them is how they change




"""
# base_x x of leftmost position of triangle in pyramid
# base_y y of lowest position of triangle in pyramid
# diagonal 1 or  2
# for i in range(base_length, base_x, base_y, diagonal):
#     pass
"""


    first sort points by lowest x or maybe normalize the x


    in diagonal 1
    for x
    - when in triangle x point = x+1 => in pyramid x,z point =base_x+1 and z+1
    - when in triangle x point = x-1 => in pyramid x,z point =base_x-1 and z-1

    - when in triangle y point = y+1 => in pyramid y,z point =base_y+1 and z-1
    - when in triangle y point = y-1 => in pyramid y,z point =base_y-1 and z+1


    """


"""
for us

    first sort points by lowest x or maybe normalize the x


    in diagonal 1
    for x
    - when in triangle x point = x+1 => in pyramid x,z point =base_x+1 and z+1
    - when in triangle x point = x-1 => in pyramid x,z point =base_x-1 and z-1

    - when in triangle y point = y+1 => in pyramid y,z point =base_y+1 and z-1
    - when in triangle y point = y-1 => in pyramid y,z point =base_y-1 and z+1


    """


# piece_k = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]
# piece = piece_k
# diagonal = 1
# length_diagonal = 5
# # z = length_diagonal-4

# z = 0
# base_y = 4


# def move_up():
#     piece = [(y-1, x, z+1)for y, x, z in piece]


# """
# --new--
# """


# def move_down():
#     piece = [(y+1, x, z-c1)for y, x, z in piece]


# """
# end
# """


# def move_right():
#     piece = [(y-1, x+1, z)for y, x, z in piece]


# def get_pyramid_coordinates():
#     return piece


# def is_valid_coordinate():
#     # or maybe is valid operation
#     pass


# print(piece)
# move_down()
# print(piece)


# diagonal = 2
# length_diagonal = 5
# z = length_diagonal-4


# def move_up():
#     piece = [(y-1, x-1, z+1)for y, x, z in piece]


# def move_right():
#     piece = [(y-1, x-1, z)for y, x, z in piece]


# def get_pyramid_coordinates():
#     return piece


# def is_valid_coordinate():
#     # or maybe is valid operation
#     pass


# piece_k = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, -1, 0)]

# print(piece_k)


'''
'''


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

        if not (1 <= z_base <= 4 and 0 <= x_base <= 3):
            raise ValueError(
                f"Invalid x_base:{x_base}  or z_base: {z_base}")

        if x_base > 0 and x_base+z_base != 4:
            raise ValueError(
                f"Invalid x_base+z_base : x_base:{x_base}  or z_base: {z_base}")

        self.piece = piece
        self.z_base = z_base
        self.x_base = x_base
        self.piece_in_pyramid = []

        self.initiate_piece_in_triangle()

    def get_piece_in_pyramid(self):
        return self.piece_in_pyramid

    def get_triangle_piece(self):
        return self.piece

    def initiate_piece_in_triangle(self):

        # problem:every piece needs to be normalized
        if self.x_base > 0:
            for y, x, z in self.piece:
                z = self.z_base-y-x
                x = x+self.x_base
                y=y+self.x_base
                self.piece_in_pyramid.append((y, x, z))
        else:
            self.piece_in_pyramid = [(y, x, self.z_base-y-x)
                                     for y, x, z in self.piece]

        self.piece = [(y+x, x, z)for y, x, z in self.piece]

    def go_down(self):
        self.piece = [(y+1, x, z)for y, x, z in self.piece]
        self.piece_in_pyramid = [(y+1, x, z-1)
                                 for y, x, z in self.piece_in_pyramid]
        print("go down")
        # add_piece

    def go_right(self):
        # y in pyramid -- but y does not change in the piece
        # x in pyramid ++
        # add_piece()
        self.piece = [(y, x+1, z)for y, x, z in self.piece]
        self.piece_in_pyramid = [(y-1, x+1, z)
                                 for y, x, z in self.piece_in_pyramid]

        print("go right")

    def is_valid_triangle(self):

        for y, x, z in self.piece:

            if y > z_base or y < 0:
                return False

            if self.z_base - y in PYRAMID_LAYERS:
                max_x, max_y = PYRAMID_LAYERS[self.z_base - y]
            else:
                return False
                raise ValueError(
                    f"Invalid pyramid layer: z_base: {self.z_base} - {y}")

            max_x, max_y = PYRAMID_LAYERS[self.z_base-y]

            if not (0 <= x < max_x) or not (0 <= y < max_y):
                return False

        return True


# piece_k = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]


positions = set()

piece_k = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]
# piece_k = [(1, 1, 0)]


triangle = Triangle(piece_k, z_base=3, x_base=0)
#triangle.go_down()
# triangle.go_down()

print(triangle.get_piece_in_pyramid())


# triangle = Triangle(piece=piece_k, z_base=4, x_base=0)
# print(triangle.get_piece_in_pyramid())
# if triangle.is_valid_triangle():
#     positions.append(triangle.get_piece_in_pyramid())


# z_base from 1 to 4

# x_base from 1 to 4


def find_in_diagonal(x_base=0, z_base=4):
    for y in range(z_base):
        triangle = Triangle(piece=piece_k, z_base=z_base, x_base=x_base)

        for i in range(y):

            if triangle.is_valid_triangle():
                positions.add(tuple(sorted(triangle.get_piece_in_pyramid())))

            print(triangle.get_piece_in_pyramid())

            triangle.go_down()

        for x in range(y):
            triangle.go_right()
            if triangle.is_valid_triangle():
                positions.add(tuple(sorted(triangle.get_piece_in_pyramid())))


# for z_base in range(1,5):
#     find_in_diagonal(x_base=0,z_base=z_base)

# for z_base in range(4,0,-1):
#         x_base=5-z_base
#         print(f"x_base: {x_base}")
#         print(f"z_base: {z_base}")
#         find_in_diagonal(x_base=x_base,z_base=z_base)

# find_in_diagonal(x_base=1, z_base=3)
# find_in_diagonal(x_base=2, z_base=2)
# print(len(positions))
# print(positions)

# z_base from 1 to 4
# x_base from 1 to 4
# x_base = 2
# z_base = 2
# # initiate_piece_in_triangle(piece_k)
# triangle = Triangle(piece_k)
# triangle.initiate_piece_in_triangle()

# # triangle.go_right()
# # triangle.go_down()

# # triangle.go_right()
# # triangle.go_right()

# # triangle.go_down()
# # triangle.go_right()
# # triangle.go_down()
# # triangle.go_right()

# # print(triangle)
# print(triangle.is_valid_triangle())
# print(triangle.get_triangle_piece())
# print(triangle.get_piece_in_pyramid())
