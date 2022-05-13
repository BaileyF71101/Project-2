"""
This file is for the second final project for Comp Sci II at UNO with Dr. Owora (completed by Bailey Frank)
source code provided from: https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1/
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
s_width = 1000   # window width
s_height = 900  # window height
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

        :return: none
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


def convert_shape_format(piece):
    """

    Provides the correct positioning after a piece is rotated

    :param piece: the colored, movable block set that is in play in any rotational format
    :param positions: list of positions for each piece to check & draw
    :param form: gives only the nested piece rotation

    :return: None
    """

    positions = []
    form = piece.shape[piece.rotation % len(piece.shape)]

    for y, line in enumerate(form):     # gets shape & its rotation
        row = list(line)
        for x, column in enumerate(row):    # each item in the nested list
            if column == '0':   # checks if 0 exists in item
                positions.append((piece.x + x, piece.y + y))
                # add to position (via x+column & y+row)

    for i, pos in enumerate(positions):     # gives each position an offset with a constant
        positions[i] = (pos[0]-2, pos[1]-4)     # moves everything left & up


def valid_space(piece, grid):
    """

    This function checks the grid to see if the piece can move into a valid & open space

    :param piece: the colored, movable block set that is in play in any rotational format
    :param grid: the playable/intractable area on the window
    :param accepted_pos: the positions that the piece can move into
    :param formatted: the rotational position of the piece

    :return: boolean value of acceptable move
    """

    accepted_pos = [[(x, y) for x in range(10) if grid[y][x] == (0, 0, 0)] for y in range(20)]     # gets all possible
                                                                        # positions for 10x20 grid in a tuple form;
                                                                        # only if space is empty, aka black

    accepted_pos = [x for sub in accepted_pos for x in sub]     # takes all positions in tuple and adds into one
                                                                # dimentional list by overriding (removes embedding)

    formatted = convert_shape_format(piece)

    for pos in formatted:   # checks to make sure position exists in accepted positions
        if pos not in accepted_pos:
            if pos[1] > -1:     # when offset by 4, piece spawns above screen; want piece to start falling before
                                # it's seen; y starts at negative value
                return False
    return True


def check_lost(parts):
    """

    Checks to see if any parts of a piece are above the screen, indicating the game is over

    :param parts: one block of a piece

    :return: boolean value of game continuation status
    """

    for pos in parts:
        x, y = pos  # splits tuple of position
        if y < 1:   # if any piece part position is above grid
            return True     # ends game

    return False    # continues game


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

    This function creates the gray lines that define each block space on the board (both occupied or not)

    :param surface: the area inside the window, not just playable/intractable area
    :param grid: the playable/intractable area of the window
    :param sx: shorthand local variable for global variable top_left_x
    :param sy: shorthand local variable for global variable top_left_y

    :return: None
    """

    sx = top_left_x
    sy = top_left_y

    for y in range(len(grid)):
        pygame.draw.line(surface, (200, 200, 200), (sx, sy + y * block_size), (sx + play_width, sy + y * block_size))
        # draws 10 vertical lines to show grid; x value static
        for x in range(len(grid[y])):
            pygame.draw.line(surface, (200, 200, 200), (sx + x*block_size, sy), (sx + x*block_size, sy + play_height))
            # draws 20 horizontal lines to show grid; y value static


def clear_rows(grid, locked):
    pass


def draw_next_shape(shape, surface):
    pass


def draw_window(surface, grid):
    """

    Shows the window for the program to display on & updates the grid as pieces are moved

    :param surface: the area inside the window, not just playable/intractable area
    :param grid: the playable/intractable area of the window
    :param font: the type of style in which the text is written on screen
    :param label: the text presented on the screen, antialiasing, and its color

    :return: None
    """

    surface.fill((0, 0, 0))   # creates initial black background in window

    font = pygame.font.SysFont('lucidiaconsole', 80)    # provides font style and size of text

    label = font.render('Tetris with Python', 1, (255, 255, 255))   # text to display, antialiasing, and color of font

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 30))    # dynamic to place in center of
    # window (is position and font size)

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

    draw_grid(surface, grid)    # creates the grid
    pygame.display.update()     # updates screen with changes


def main(win):
    """

    provides the main functions of the program (the locked positions, the grid, running, current piece, next piece,
    clock, and fall time)

    :param locked_positions: a dictionary of all the positions that are set in place, and are not open for any pieces to
    :param grid: the playable/intractable area on the window
    :param change_piece: specifies whether the piece should be changed at a given time
    :param next_piece: the next piece that will be available to the user
    :param clock: shows how long a single game has been active
    :param fall_time: tracks how long since last run loop ran (in milliseconds)
    :param fall_speed: the time it takes before each shape starts falling (in seconds)
    :param piece_pos: checks all positions of piece movement downwards to see if piece needs to move down or be locked

    :return: None
    """

    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27

    while run:  # while game is running
        grid = create_grid(locked_positions)    # every time you move, chance to add to locked_positions, so update grid
        fall_time += clock.get_rawtime()    # gets amount of time since last clock.tick()
        clock.tick()    # adds a tick to a timer/clock - makes it uniform to every OS

        if fall_time/1000 > fall_speed:     # if the piece has been in a stationary position longer than the fall speed
            fall_time = 0   # resets fall_time
            current_piece.y += 1    # moves piece down 1 y increment
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1    # undoes previous movement if not valid
                change_piece = True     # stops current piece movement & gets next one in play (& active)

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

        piece_pos = convert_shape_format(current_piece)

        for i in range(len(piece_pos)):    # draws colored piece and shows movement
            x, y = piece_pos[i]   # current iteration
            if y > -1:      # if piece is not above screen
                grid[y][x] = current_piece.color

        if change_piece:    # check change piece variable
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color   # updates grid to show locked piece
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

        draw_window(win, grid)  # updates window with player input & according actions

        if check_lost(locked_positions):    # checks to see if game is lost; if so, breaks running while loop
            run = False

    pygame.display.quit()

def main_menu(win):
    main()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris with Python')

"""
This function call initializes the program
"""
main_menu(win)
