import pygame
import math
import pygame.gfxdraw
from board import Board
from game import Game

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
BROWN = (210, 180, 140)
PENGUIN = (255, 165, 0)

# Hexagon properties
HEX_SIZE = 30  # Size of a hexagon side
WIDTH, HEIGHT = 1000, 600  # Screen dimensions

def hex_to_pixel(q, r, s, size):
    x = size * (3/2 * q)
    y = size * (math.sqrt(3)/2 * q + math.sqrt(3) * r)
    return x, y

def draw_board(surface, board):
    surface.fill(BROWN)

    # Draw each hexagon in gamepieces
    for piece in board.gamepieces:
        q, r, s = piece.q, piece.r, piece.s
        hextype = piece.hextype

        # Determine color based on hextype
        if hextype == 'white':
            color = WHITE
        elif hextype == 'blue':
            color = LIGHT_BLUE
        elif hextype == 'support':
            color = DARK_BLUE
        elif hextype == 'penguin':
            color = PENGUIN
        else:
            continue  # Skip if hextype is unrecognized

        # Convert hex coordinates to pixel coordinates
        pixel_x, pixel_y = hex_to_pixel(q, r, s, HEX_SIZE)

        # Center hexes in the screen
        pixel_x += WIDTH / 2
        pixel_y += HEIGHT / 2

        # Draw the hexagon
        draw_hex(surface, color, (pixel_x, pixel_y), HEX_SIZE)
    pygame.display.flip()

# Function to draw a hexagon at a given pixel position

def draw_hex(surface, color, position, size):
    x, y = position
    points = []
    for i in range(6):
        angle = 2 * math.pi / 6 * i
        px = x + size * math.cos(angle)
        py = y + size * math.sin(angle)
        points.append((px, py))    

    # Use gfxdraw to draw filled polygon and anti-aliased polygon
    pygame.gfxdraw.filled_polygon(surface, points, color)
    pygame.gfxdraw.aapolygon(surface, points, BLACK)

def return_selected_hex(surface, mouse_pos):
    mx, my = mouse_pos
    mx -= WIDTH / 2
    my -= HEIGHT / 2

    size = HEX_SIZE
    q = (2/3 * mx) / size
    r = (-1/3 * mx + math.sqrt(3)/3 * my) / size

    # Round q and r to the nearest hexagon
    q_rounded, r_rounded = round(q), round(r)

    return(q_rounded, r_rounded)

def start_penguins(surface):
    board = Board()
    # Fill background
    draw_board(surface, board)
    
    return board

'''def displayText(surface):
    fontObj = pygame.font.Font(None, 32)
    textSufaceObj = fontObj.render('Blue turn', True, (0, 0, 0), None)
    surface.blit(textSufaceObj, (100, 100))
    pygame.display.flip()'''

def run_loop(screen, board):
    # Main loop to keep the window open
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                '''displayText(screen);'''


                if event.button == 1:  # Left mouse button
                    
                    mouse_pos = pygame.mouse.get_pos()
                    selected_hex = return_selected_hex(screen, mouse_pos)
                    
                    if selected_hex:
                        hexagon = board.find_hex_from_coordinates(selected_hex[0], selected_hex[1], -selected_hex[0]-selected_hex[1])
                        if hexagon:
                            print("Hexagon type:", hexagon.hextype)
                            board.remove_hex(selected_hex[0], selected_hex[1], -selected_hex[0]-selected_hex[1])
                            draw_board(screen, board)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    
                    start_penguins(screen)
    pygame.quit()


def start_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Hexagonal Grid')

    gameBoard = start_penguins(screen)
    gameLogic = Game(gameBoard)

    run_loop(screen, gameBoard)