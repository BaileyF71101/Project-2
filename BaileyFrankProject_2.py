"""
This file is for the second final project for Comp Sci II at UNO with Dr. Owora (completed by Bailey Frank)
"""
# installed pygame module to project folder

import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

# TODO: move and/or edit above comments to relevant sections

"""
The traditional grid size is 10 x 20 squares, and the shapes are: S, Z, I, O, J, L, T
"""

"""
The below coded line imports a font from the module 'pygame' to use in the program
"""

pygame.font.init()

"""

Below variables are global, and are used to create the size of the individual block pieces, as well as the 
play area of the window

:param s_width: window width
:param S_height: window height
:param play_width: the width of the area in which the game is played within the window
:param play_height: the height of the area in which the game is played within the window
:param block_size: the size of each block within the grid and of each square in a piece
:param top_left_x: in conjunction with top_left_y, is the top left of the play area
:param top_left_y: in conjunction with top_left_x, is the top left of the play area

"""
s_width = 800   # window width
s_height = 700  # window height
play_width = 300  # needs to be half of play_height for traditional tetris ratio of 10 blocks
play_height = 600  # needs to be double that of play_width for traditional tetris ratio of 20 blocks
block_size = 30  # needs to be width floored by 10 OR height floored by 20 for traditional tetris ratio

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

"""
These lists are for each piece in the game, and each nested list is the different orientation each shape can have
(per piece)
"""
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

"""
The two global variables below are the list of available pieces for the randomizer to choose from when selecting
a new piece, as well as the associated color for each piece
"""
pieces = [S, Z, I, O, J, L, T]  # 0-6 index for pieces
piece_colors = [(61, 219, 0), (219, 0, 0), (0, 219, 215), (219, 222, 0), (0, 22, 222), (0, 222, 163), (148, 0, 222)]


class Piece(object):
    # TODO: fill out docstring parameter definitions
    def __init__(self, x, y, shape):
        """

        :param x:
        :param y:
        :param shape:
        :param color:
        :param rotation:

        """
        self.x = x
        self.y = y
        self.shape = shape
        self.color = piece_colors[pieces.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    """

    Creates the grid, aka the playable/intractable area of the window

    :param locked_positions: a dictionary of all the positions that are set in place, and are not open for any pieces to
    move to
    :param grid: the playable/intractable area of the window

    :return: grid

    """
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]  # signifies that the grid is a space made of columns
    # and rows (in that order)

    for y in range(len(grid)):  # 20, the height of the play area in traditional tetris ratio
        for x in range(len(grid[y])):   # 10, the width of the play area in traditional tetris ratio
            if (x, y) in locked_positions:
                key = locked_positions[{x, y}]
                grid[y][x] = key

    return grid


def convert_shape_format(shape):
    pass


def valid_space(shape, grid):
    pass


def check_lost(positions):
    pass


def get_shape():
    """

    provides a random piece from the global pieces list

    :return: Piece

    """
    return Piece(5, 0, random.choice(pieces))   # x pos, y pos, piece


def draw_text_middle(text, size, color, surface):
    pass


def draw_grid(surface, grid):
    """

    Updates the grid as pieces are moved

    :param surface: the area inside the window, not just playable/intractable area
    :param grid: the playable/intractable area of the window

    """

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], top_left_x + x*block_size, top_left_y + y*block_size, block_size,
                             block_size, 0)
            # Loops through every color in grid [y][x], the surface it draws to, and position, and fills shape with
            # color (not just border color); dynamic
            # In top left x position, whatever column you're in, multiply by block size, and that's x position (same
            # for y with rows)

    pygame.draw.rect(surface, (255, 255, 255), (top_left_x, top_left_y, play_width, play_height, 5))
    # draws grid border (where, color, parameters (x-axis start, y-axis start, width, height, thickness))


def clear_rows(grid, locked):
    pass


def draw_next_shape(shape, surface):
    pass


def draw_window(surface, grid):
    """

    Shows the window for the program to display on

    :param surface: the area inside the window, not just playable/intractable area
    :param grid: the playable/intractable area of the window
    :param font: the type of style in which the text is written on screen
    :param label: the text presented on the screen, antialiasing, and its color

    """
    surface.fill((0, 0, 0))   # creates initial black background in window

    font = pygame.font.SysFont('lucidiaconsole', 80)    # provides font style and size of text

    label = font.render('Tetris with Python', 1, (255, 255, 255))   # text to display, antialiasing, and color of font

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 30))    # dynamic to place in center of
    # window (is position and font size)

    draw_grid(surface, grid)    # creates the grid
    pygame.display.update()     # updates screen with changes


def main(win):
    # TODO: fill out fall_time parameter
    """
    provides the main functions of the program (the locked positions, the grid, running, current piece, next piece,
    clock, and fall time)

    :param locked_positions: a dictionary of all the positions that are set in place, and are not open for any pieces to
    :param grid: the playable/intractable area on the window
    :param change_piece: specifies whether the piece should be changed at a given time
    :param next_piece: the next piece that will be available to the user
    :param clock: shows how long a single game has been active
    :param fall_time:

    """
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:  # while game is running
        for event in pygame.event.get():    # while something is happening
            if event.type == pygame.QUIT:   # if player decides to quit
                run = False     # exits loop, stops game, exits window

            if event.type == pygame.KEYDOWN:    # if player pushes a key
                if event.key == pygame.K_LEFT:  # if player pushes left arrow key specifically
                    current_piece.x -= 1    # move piece left one block
                    if not(valid_space(current_piece, grid)):   # if no space to move piece
                        current_piece += 1  # undoes the left motion

                if event.key == pygame.K_RIGHT:     # if player pushes right arrow key specifically
                    current_piece.x += 1    # move piece right one block
                    if not(valid_space(current_piece, grid)):   # if no space to move piece
                        current_piece -= 1  # undoes right motion

                if event.key == pygame.K_DOWN:  # if player pushes down arrow key specifically
                    current_piece.y += 1    # move piece down one block
                    if not(valid_space(current_piece, grid)):  # if no space to move piece
                        current_piece -= 1  # undoes down motion

                if event.key == pygame.K_UP:    # if player pushes up arrow key specifically
                    current_piece.rotation += 1     # rotates the piece to next nested list position
                    if not(valid_space(current_piece, grid)):   # if no space on either side to rotate piece
                        current_piece -= 1  # undoes rotation action

        draw_window(win, grid)  # updates window with player input & according actions


def main_menu(win):
    main()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris with Python')

"""
This function call initializes the program
"""
main_menu(win)
