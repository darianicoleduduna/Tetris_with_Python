import pygame
from tetris import Tetris
from shape import colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BACKGROUND = (73, 69, 106)
LIGHT_BACKGROUND=(203, 207, 234)
HOTPINK = (248, 24, 148)
BUTTON_HOVER_COLOR = (254, 127, 156)
BUTTON_TEXT_COLOR = (25, 255, 255)

def init_game():
    game = Tetris(20, 10)
    return game
def toggle_dark_mode(dark_mode):
    return not dark_mode
def play_again(game,high_score):
    game.grid = [[0] * game.width for _ in range(game.height)]  # Reset the game grid
    game.shape = None  # Remove any existing piece
    game.state = "start"  # Reset game state
    game.score = 0  # Reset score
    game.new_shape()  # Initialize a new shape
    game.high_score = high_score 

def toggle_hard_mode(hard_mode):
    return not hard_mode



def main():
    pygame.init()

    # Set the size of the screen
    size = (600, 900)
    screen = pygame.display.set_mode(size)

    # Set the title of the window
    pygame.display.set_caption("Tetris")

    # Initialize game variables
    done = False
    clock = pygame.time.Clock()
    fps = 60  # Updates screen 60 times per second
    game = init_game()
    pressing_down = False
    high_score = 0
    dark_mode = True
    hard_mode = False
    fall_speed=300 #300 ms

    # Calculate the x and y positions for centering the grid
    grid_width = game.width * game.zoom
    grid_height = game.height * game.zoom
    game.x = (size[0] - grid_width) // 2
    game.y = (size[1] - grid_height) // 2

    # Define button dimensions and position
    button_width = 150
    button_height = 50
    button_x = (size[0] - button_width) // 2
    button_y = size[1] - button_height - 60
    hard_mode_button_x = size[0] - 100
    hard_mode_button_y = 70
    hard_mode_button_width = 80
    hard_mode_button_height = 50

    # Initialize the timer for automatic downward movement
    last_move_down_time = pygame.time.get_ticks()

    while not done:
        current_time = pygame.time.get_ticks()

        if game.shape is None:
            game.new_shape()

        # Check if it's time to move the shape down
        if current_time - last_move_down_time >= fall_speed:
            if game.state == "start":
                game.go_down()
            last_move_down_time = current_time

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if game.state != "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.rotate()
                    if event.key == pygame.K_DOWN:
                        game.go_down()
                    if event.key == pygame.K_LEFT:
                        game.go_side(-1)
                    if event.key == pygame.K_RIGHT:
                        game.go_side(1)
                    if event.key == pygame.K_SPACE:
                        game.go_fast()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                    play_again(game,high_score)
                elif size[0] - 100 <= mouse_pos[0] <= size[0] - 20 and 10 <= mouse_pos[1] <= 60:
                    dark_mode = toggle_dark_mode(dark_mode)
                elif hard_mode_button_x <= mouse_pos[0] <= hard_mode_button_x + hard_mode_button_width and hard_mode_button_y <= mouse_pos[1] <= hard_mode_button_y + hard_mode_button_height:
                    hard_mode = toggle_hard_mode(hard_mode)
                    fall_speed = 150 if hard_mode else 300


        # these 2 functions are handling the dark or light color scheme preference of the user:
        
        mouse_pos = pygame.mouse.get_pos()
        dark_mode_hover = size[0] - 100 <= mouse_pos[0] <= size[0] - 20 and 10 <= mouse_pos[1] <= 60
        if dark_mode:
            
            screen.fill(DARK_BACKGROUND)
            grid_color=WHITE
            button_color2=LIGHT_BACKGROUND if not dark_mode_hover else BUTTON_HOVER_COLOR
            
            hard_mode_button_color = BUTTON_HOVER_COLOR if hard_mode_button_x <= mouse_pos[0] <= hard_mode_button_x + hard_mode_button_width and hard_mode_button_y <= mouse_pos[1] <= hard_mode_button_y + hard_mode_button_height else LIGHT_BACKGROUND
            text_b="Light"
            
        else:
            
            screen.fill(LIGHT_BACKGROUND)
            grid_color=HOTPINK
            button_color2=DARK_BACKGROUND if not dark_mode_hover else BUTTON_HOVER_COLOR
            hard_mode_button_color = BUTTON_HOVER_COLOR if hard_mode_button_x <= mouse_pos[0] <= hard_mode_button_x + hard_mode_button_width and hard_mode_button_y <= mouse_pos[1] <= hard_mode_button_y + hard_mode_button_height else DARK_BACKGROUND
            text_b="Dark"


        # Draw the grid
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, grid_color, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.grid[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.grid[i][j]], [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

        # Draw the current shape
        if game.shape is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.shape.image():
                        pygame.draw.rect(screen, colors[game.shape.color], 
                                        [game.x + game.zoom * (j + game.shape.x) + 1,
                                        game.y + game.zoom * (i + game.shape.y) + 1,
                                        game.zoom - 2, game.zoom - 2])

        # Draw the score
        font = pygame.font.SysFont('Calibri', 22, True, False)
        text = font.render("Current score: " + str(game.score), True, BLACK)
        text_high_score = font.render("High score: " + str(high_score), True, BLACK)
        screen.blit(text, [10, 10])
        screen.blit(text_high_score, [10, 30])

        if game.state == "game_over":
            
            if game.score > high_score:
                high_score = game.score
            font1 = pygame.font.SysFont('Calibri', 35, True, False)
            text_game_over = font1.render("Game Over", True, HOTPINK)
            text_quit = font.render("Press Esc to quit", True, HOTPINK)
            
            # Center the game over text above the grid
            game_over_x = game.x + (grid_width - text_game_over.get_width()) // 2
            quit_x = game.x + (grid_width - text_quit.get_width()) // 2
            screen.blit(text_game_over, [game_over_x, game.y - 100])
            screen.blit(text_quit, [quit_x, game.y - 50])

            # Draw the Play Again button
            mouse_pos = pygame.mouse.get_pos()
            button_color = HOTPINK if not (button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height) else BUTTON_HOVER_COLOR
            pygame.draw.rect(screen, button_color, [button_x, button_y, button_width, button_height])
            button_font = pygame.font.SysFont('Calibri', 25, True, False)
            button_text = button_font.render("Play Again", True, DARK_BACKGROUND)
            screen.blit(button_text, [button_x + (button_width - button_text.get_width()) // 2, button_y + (button_height - button_text.get_height()) // 2])
             
        # Draw the dark mode button
        pygame.draw.rect(screen, button_color2, [size[0] - 100, 10, 80, 50])
        font = pygame.font.SysFont('Calibri', 22, True, False)
        button_text = font.render(text_b, True, HOTPINK)
        screen.blit(button_text, [size[0] - 90, 20])
        

       
        pygame.draw.rect(screen, hard_mode_button_color, [hard_mode_button_x, hard_mode_button_y, hard_mode_button_width, hard_mode_button_height])
        hard_mode_text = "Hard" if not hard_mode else "Easy"
        button_text = font.render(hard_mode_text, True, HOTPINK)
        screen.blit(button_text, [hard_mode_button_x + 10, hard_mode_button_y + 15])
        
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

main()
