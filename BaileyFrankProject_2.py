"""
This file is for the second final project for Comp Sci II at UNO with Dr. Owora (completed by Bailey Frank)
source code provided from: https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1/
"""
# installed pygame module to project folder

import pygame
import random

# TODO: make exponential leveling

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
s_width = 800  # window width
s_height = 750  # window height
play_width = 300  # needs to be half of play_height for traditional tetris ratio of 10 blocks
play_height = 600  # needs to be double that of play_width for traditional tetris ratio of 20 blocks
block_size = 30  # needs to be width floored by 10 OR height floored by 20 for traditional tetris ratio

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

lvl_cleared_rows = 0  # number of rows to clear until next level is reached
total_cleared_rows = 0  # total number of rows cleared in a single game
level = 1   # the level at which the player is at; indicates how many fall speed changes they've gone through
score: int = 0

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
piece_colors = [(61, 219, 0), (219, 0, 0), (0, 219, 215), (219, 222, 0), (0, 22, 222), (222, 163, 0), (148, 0, 222)]


class Piece(object):
    def __init__(self, x, y, shape):
        """

        :param x:
        :param y:
        :param shape:
        :color:
        :rotation:

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
    :grid: the playable/intractable area of the window

    :return: grid
    """

    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]  # signifies that the grid is a space made of columns
    # and rows (in that order)

    for y in range(len(grid)):  # 20, the height of the play area in traditional tetris ratio
        for x in range(len(grid[y])):  # 10, the width of the play area in traditional tetris ratio
            if (x, y) in locked_positions:
                key = locked_positions[(x, y)]
                grid[y][x] = key

    return grid


def convert_shape_format(piece):
    """

    Provides the correct positioning after a piece is rotated

    :param piece: the colored, movable block set that is in play in any rotational format
    :positions: list of positions for each piece to check & draw
    :form: gives only the nested piece rotation

    :return: positions
    """

    positions = []
    form = piece.shape[piece.rotation % len(piece.shape)]

    for y, line in enumerate(form):  # gets piece & its nested lists
        row = list(line)
        for x, column in enumerate(row):  # each item in the nested list
            if column == '0':  # checks if 0 exists in item
                positions.append((piece.x + x, piece.y + y))
                # add to position (via x+column & y+row)

    for i, pos in enumerate(positions):  # gives each position an offset with a constant
        positions[i] = (pos[0] - 2, pos[1] - 4)  # moves everything left & up

    return positions


def valid_space(piece, grid):
    """

    This function checks the grid to see if the piece can move into a valid & open space

    :param piece: the colored, movable block set that is in play in any rotational format
    :param grid: the playable/intractable area on the window
    :accepted_pos: the positions that the piece can move into
    :formatted: the rotational position of the piece

    :return: boolean value of acceptable move
    """

    accepted_pos = [[(x, y) for x in range(10) if grid[y][x] == (0, 0, 0)] for y in range(20)]
    # gets all possible positions for 10x20 grid in a tuple form; only if space is empty, aka black

    accepted_pos = [x for sub in accepted_pos for x in sub]
    # takes all positions in tuple and adds into one dimensional list by overriding (removes embedding)

    formatted = convert_shape_format(piece)

    for pos in formatted:  # checks to make sure position exists in accepted positions
        if pos not in accepted_pos:
            if pos[1] > -1:
                # when offset by 4, piece spawns above screen; want piece to start falling before it's seen; y starts at
                # negative value
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
        if y < 1:  # if any piece part position is above grid
            return True  # ends game

    return False  # continues game


def get_shape():
    """

    provides a random piece from the global pieces list

    :return: Piece
    """

    global pieces, piece_colors

    return Piece(5, 0, random.choice(pieces))  # x pos, y pos, piece


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('lucidiaconsole', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - (label.get_height() / 2)))


def draw_grid(surface, grid):
    """

    This function creates the gray lines that define each block space on the board (both occupied or not)

    :param surface: the area inside the window, not just playable/intractable area
    :param grid: the playable/intractable area of the window
    :sx: provides x-axis center of window
    :sy: provides y-axis center of window

    :return: None
    """

    sx = top_left_x
    sy = top_left_y

    for y in range(len(grid)):
        pygame.draw.line(surface, (200, 200, 200), (sx, sy + y * block_size), (sx + (play_width - 1), sy + y * block_size))
        # draws 10 vertical lines to show grid; x value static
        for x in range(len(grid[y])):
            pygame.draw.line(surface, (200, 200, 200), (sx + x * block_size, sy), (sx + x * block_size, sy + play_height))
            # draws 20 horizontal lines to show grid; y value static


def clear_rows(grid, locked):
    """

    This function will clear any full rows that are filled with any part of the pieces

    :param grid: the playable/intractable area of the window
    :param locked: a dictionary of all the positions that are set in place, and are not open for any pieces to
    move to
    :inc: shorthand for increment; the number of shifts that need to occur
    :ind: shorthand for index; the row identification number(s)

    :return: inc
    """
    global lvl_cleared_rows, total_cleared_rows, score

    inc = 0
    ind = 0
    for y in range(len(grid) - 1, -1, -1):  # loops through grid backwards
        row = grid[y]
        if (0, 0, 0) not in row:  # if the row doesn't contain the color black
            inc += 1
            ind = y
            for x in range(len(row)):  # get every position in row
                try:
                    del locked[(x, y)]  # removes row
                except:
                    continue

    # shift necessary row(s) down to remove 'floating' parts & adds row(s) on top to replace deleted row(s)

    if inc > 0:  # if removed row is more than 0
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            # for every key in sorted locked list based on y value
            x, y = key  # gets position
            if y < ind:  # if y is above current index of row removed
                new_key = (x, y + inc)  # increments by certain value to shift down
                locked[new_key] = locked.pop(key)
                # creates new key in locked (can have same color) in new position

        lvl_cleared_rows += inc  # decreases next level counter by inc
        total_cleared_rows += inc  # increases total rows cleared by inc

        if inc == 1:
            score += inc * 1000
        elif inc == 2:
            score += inc * 2000
        elif inc == 3:
            score += inc * 3000
        elif inc == 4:
            score += inc * 4000


def draw_next_shape(piece, surface):
    """

    This function shows the upcoming piece that will be played after the current piece is locked into position

    :param piece: the colored, movable block set that is in play in any rotational format
    :param surface: the area inside the window, not just playable/intractable area
    :font: The style of text and its size
    :label: the text 'Next Piece: ' and the piece itself presented on the screen
    :sx: provides x-axis center of window
    :sy: provides y-axis center of window
    :form: provides the image of the next piece

    :return: None
    """

    font = pygame.font.SysFont('lucidiaconsole', 30)  # provides font style and size of text
    label = font.render('Next Piece:', 1, (255, 255, 255))  # text to display, antialiasing, and color of font

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    form = piece.shape[piece.rotation % len(piece.shape)]  # gets the next piece

    for y, line in enumerate(form):  # gets piece & its nested lists
        row = list(line)
        for x, column in enumerate(row):  # for each item in nested list
            if column == '0':  # if 0 appears in item
                pygame.draw.rect(surface, piece.color, (sx + x * block_size, sy + y * block_size, block_size, block_size), 0)
                # draw the part

    surface.blit(label, (sx + 10, sy - 30))


def cleared_rows(surface):
    """

    This function shows the total number of rows cleared and the number of rows to clear until the next level is reached

    :param surface:
    :font: The style of text and its size
    :label: the text 'Rows Cleared: ' and the total cleared rows presented on the screen
    :label2: the text 'Rows until next level: 'and the number of rows that need to be cleared until the next level is reached
    :label3: the text 'Current Level: ' and the level that the player is currently on
    :sx: provides x-axis center of window
    :sy: provides y-axis center of window

    :return: None
    """

    global lvl_cleared_rows, total_cleared_rows

    font = pygame.font.SysFont('lucidiaconsole', 30)
    label = font.render('Rows Cleared: {}'.format(total_cleared_rows), 1, (255, 255, 255))
    label2 = font.render('Rows until next level: {}'.format(5 - lvl_cleared_rows), 1, (255, 255, 255))
    label3 = font.render('Current Level: {}'.format(level), 1, (255, 255, 255))
    # text to display, antialiasing, and color of font

    sx = play_width - 50
    sy = play_width / 2 + 100

    surface.blit(label, (sx - 235, sy + 50))
    surface.blit(label2, (sx - 235, sy + 150))
    surface.blit(label3, (sx - 235, sy + 200))


def update_score(nscore):
    """

    This function is to keep track of the current game's score

    :param nscore: the new score, or the present game's score

    :return: None
    """

    global score

    score = highscore()

    with open('scores.txt', 'w', ) as f:
        if int(score) > int(nscore):
            f.write(str(score))
        else:
            f.write(str(nscore))


def highscore():
    """

    This function is to keep track of the overall best score throughout every game played

    :return: score
    """

    try:
        with open('scores.txt', 'r', ) as f:
            lines = f.readlines()
            score = lines[0].strip()

    except:
        score = 10000

    return score


def draw_window(surface, grid, score=0, last_score=0):
    """

    Shows the window for the program to display on & updates the grid as pieces are moved

    :param surface: the area inside the window, not just playable/intractable area
    :param grid: the playable/intractable area of the window
    :param score: the number of points the player has made in a single game session
    :param last_score: the overall highscore
    :font: the type of style in which the game title is written on screen
    :label: the text 'Tetris with Python'
    :font2: the type of style in which the game score is written on screen
    :label2: the text 'score:' presented on the screen
    :label3: the numeric score presented on the screen
    :label4: the text 'High Score:' presented on the screen
    :label5: the numeric high score presented on the screen
    :sx:provides x-axis center of window
    :sy: provides y-axis center of window

    :return: None
    """

    surface.fill((0, 0, 0))  # creates initial black background in window

    font = pygame.font.SysFont('lucidiaconsole', 80)  # provides font style and size of text
    label = font.render('Tetris with Python', 1, (255, 255, 255))  # text to display, antialiasing, and color of font
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))  # dynamic to place in center of window (is position and font size)

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    font2 = pygame.font.SysFont('lucidiaconsole', 35)
    label2 = font2.render('Score: ', 1, (255, 255, 255))
    label3 = font2.render('{}'.format(str(score)), 1, (255, 255, 255))
    label4 = font2.render('High Score: ', 1, (255, 255, 255))
    label5 = font2.render('{}'.format(last_score), 1, (255, 255, 255))

    surface.blit(label2, (sx, sy - 200))
    surface.blit(label3, (sx, sy - 160))
    surface.blit(label4, (sx - 585, sy - 200))
    surface.blit(label5, (sx - 585, sy - 160))

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (top_left_x + x * block_size, top_left_y + y * block_size, block_size,
                                                   block_size), 0)
            # Loops through every color in grid [y][x], the surface it draws to, and position, and fills shape with
            # color (not just border color); dynamic
            # In top left x position, whatever column you're in, multiply by block size, and that's x position (same
            # for y with rows)

    draw_grid(surface, grid)  # creates the grid
    pygame.draw.rect(surface, (255, 255, 255), (top_left_x, top_left_y, play_width, play_height), 4)
    # draws grid border (where, color, parameters (x-axis start, y-axis start, width, height, thickness))


def main(win):
    """

    provides the main functions of the program (the locked positions, the grid, running, current piece, next piece,
    clock, and fall time)

    :param win: shorthand for window
    :locked_positions: a dictionary of all the positions that are set in place, and are not open for any pieces to
    :grid: the playable/intractable area on the window
    :change_piece: specifies whether the piece should be changed at a given time
    :next_piece: the next piece that will be available to the user
    :clock: shows how long a single game has been active
    :fall_time: tracks how long since last run loop ran (in milliseconds)
    :fall_speed: the time it takes before each shape starts falling (in seconds)
    :piece_pos: checks all positions of piece movement downwards to see if piece needs to move down or be locked

    :return: None
    """

    global grid, lvl_cleared_rows, total_cleared_rows, level

    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5

    while run:  # while game is running
        last_score = highscore()
        grid = create_grid(locked_positions)  # every time you move, change to add to locked_positions, so update grid
        fall_time += clock.get_rawtime()  # gets amount of time since last clock.tick()
        clock.tick()  # adds a tick to a timer/clock - makes it uniform to every OS

        if lvl_cleared_rows >= 5:  # after 5 or more rows have been cleared
            fall_speed -= 0.75  # increase fall speed
            lvl_cleared_rows = 0  # resets number of cleared rows for level
            level += 1  # shows the player has advanced to the next level

        if fall_time / 1000 >= fall_speed:  # if the piece has been in a stationary position longer than the fall speed
            fall_time = 0  # resets fall_time
            current_piece.y += 1  # moves piece down 1 y increment
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1  # undoes previous movement if not valid
                change_piece = True  # stops current piece movement & gets next one in play (& active)

        for event in pygame.event.get():  # while something is happening
            if event.type == pygame.QUIT:  # if player decides to quit via X key
                run = False  # exits loop
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:  # if player pushes a key
                if event.key == pygame.K_LEFT:  # if player pushes left arrow key specifically
                    current_piece.x -= 1  # move piece left one block
                    if not (valid_space(current_piece, grid)):  # if no space to move piece
                        current_piece.x += 1  # undoes the left motion

                elif event.key == pygame.K_RIGHT:  # if player pushes right arrow key specifically
                    current_piece.x += 1  # move piece right one block
                    if not (valid_space(current_piece, grid)):  # if no space to move piece
                        current_piece.x -= 1  # undoes right motion

                elif event.key == pygame.K_DOWN:  # if player pushes down arrow key specifically
                    current_piece.y += 1  # move piece down one block
                    if not (valid_space(current_piece, grid)):  # if no space to move piece
                        current_piece.y -= 1  # undoes down motion

                elif event.key == pygame.K_UP:  # if player pushes up arrow key specifically
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    # rotates the piece to next nested list position
                    if not (valid_space(current_piece, grid)):  # if no space on either side to rotate piece
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                        # undoes rotation action

        piece_pos = convert_shape_format(current_piece)

        for i in range(len(piece_pos)):  # draws colored piece and shows movement
            x, y = piece_pos[i]  # current iteration
            if y > -1:  # if piece is not above screen
                grid[y][x] = current_piece.color

        if change_piece:  # check change piece variable
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color  # updates grid to show locked piece
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            clear_rows(grid, locked_positions)  # only checks to remove row AFTER piece has become stationary

        if check_lost(locked_positions):  # checks to see if game is lost; if so, breaks running while loop
            win.fill((0, 0, 0))
            draw_text_middle(win, "You Lost - Try Again!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)
            main_menu(win)

        draw_window(win, grid, score, last_score)  # updates window with player input & according actions done thus far
        draw_next_shape(next_piece, win)  # updates window with next piece
        cleared_rows(win)
        pygame.display.update()  # displays window updates


def main_menu(win):
    """

    :param win: shorthand for 'window'
    :return: None
    """

    global lvl_cleared_rows, total_cleared_rows, score

    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, "Press Any Key To Start", 80, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                update_score(score)
                run = False
            if event.type == pygame.KEYDOWN:
                lvl_cleared_rows = 0
                total_cleared_rows = 0
                score = 0
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris with Python')

"""
This function call initializes the program
"""
main_menu(win)
