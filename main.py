from colors import *
from images import *
from levels import *
from configuration import *
import pygame
import random


#initialise pygame
pygame.init()

################################################# SCREEN SETTINGS ######################################################

window_width = WINDOW_WIDTH
window_height = WINDOW_HEIGHT
game_disp = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()

selected_theme = 0
# Selected theme = 0 -> Invalid Theme
# Selected theme = 1 -> Tom & Jerry Theme
# Selected theme = 2 -> Christmas Theme
# Selected theme = 3 -> Halloween Theme

# To draw a images on menu screen.
def draw_menuImg(menuImg_x, menuImg_y):
    game_disp.blit(menu_img, (menuImg_x, menuImg_y))

# for writing text on the screen
def write_text(text, scr, pos, fsize, fcol, fname, center=True):
    font = pygame.font.Font(fname, fsize)
    scrtext = font.render(text, False, fcol)
    textsize = scrtext.get_size()  #to get pixels of the text
    if center:
        pos[0] -= textsize[0] // 2
        pos[1] -= textsize[1] // 2
    scr.blit(scrtext, pos)


################################################## MENU SCREEN #########################################################

def menu_scr():
    global next_scr,selected_theme
    menuImg_x = (window_width * 0.45)
    menuImg_y = (window_height * 0.30)
    change_menu_x = 5
    end = False

    while not end:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    next_scr = "Tom & Jerry"
                    selected_theme = 1
                    end = True
                elif event.key == pygame.K_2:
                    next_scr = "Christmas"
                    selected_theme = 2
                    end = True
                elif event.key == pygame.K_3:
                    next_scr = "Halloween"
                    selected_theme = 3
                    end = True

        game_disp.fill(navy_blue)
        draw_menuImg(menuImg_x, menuImg_y)
        menuImg_x += change_menu_x
        if menuImg_x > window_width - MENU_IMG_WIDTH:
            change_menu_x = -5
        if menuImg_x < 0:
            change_menu_x = 5
        write_text("TRIPLE PAC(K)", game_disp, [window_width // 2, window_height // 6], HEADING_FONT_SIZE_MAINSCREEN, white, './Fonts/Sunday Morning.ttf')
        write_text("Tom & Jerry (PRESS 1)", game_disp, [window_width // 2, window_height // 2], THEMES_FONT_SIZE_MAINSCREEN, white, './Fonts/Bright Orchid.ttf')
        write_text("Christmas (PRESS 2)", game_disp, [window_width // 2, window_height // 2 + 70], THEMES_FONT_SIZE_MAINSCREEN, black, './Fonts/Bright Orchid.ttf')
        write_text("Halloween (PRESS 3)", game_disp, [window_width // 2, window_height // 2 + 140], THEMES_FONT_SIZE_MAINSCREEN, white,
                   './Fonts/Bright Orchid.ttf')
        write_text("How to Play ?", game_disp, [window_width // 2, window_height // 2 + 210], HOW_TO_PLAY_FONT_SIZE_MAINSCREEN, black,
                   './Fonts/Bright Orchid.ttf')
        write_text(DEVELOPERS, game_disp, [50, window_height - 30],
                   25, black, './Fonts/Almond Nougat.ttf', False)
        pygame.display.update()
        clock.tick(30)
    return next_scr


################################################## INTRO SCREEN #######################################################


def intro_screen():
    global next_scr, selected_theme
    print(selected_theme)
    end = False
    while not end:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    next_scr = "ghosts_3"
                    end = True
                elif event.key == pygame.K_2:
                    next_scr = "ghosts_4"
                    end = True

        if selected_theme == 1:
            game_disp.fill(grey)
            write_text("Tom & Jerry", game_disp, [window_width // 2, window_height // 6], HEADING_FONT_SIZE_THEMESCREEN, navy_blue,
                       './Fonts/Sunday Morning.ttf')

        elif selected_theme == 2:
            game_disp.fill(salmon)
            write_text("Christmas", game_disp, [window_width // 2, window_height // 6], HEADING_FONT_SIZE_THEMESCREEN, white,
                       './Fonts/Sunday Morning.ttf')

        elif selected_theme == 3:
            game_disp.fill(halloween_bg)
            write_text("Halloween", game_disp, [window_width // 2, window_height // 6], HEADING_FONT_SIZE_MAINSCREEN, salmon,
                       './Fonts/Sunday Morning.ttf')

        write_text("3 Ghosts (PRESS 1)", game_disp, [window_width // 2, window_height // 2], CHOOSE_GHOSTS_FONT_SIZE_THEMESCREEN, black,
                   './Fonts/Bright Orchid.ttf')
        write_text("4 Ghosts (PRESS 2)", game_disp, [window_width // 2, window_height // 2 + 140], CHOOSE_GHOSTS_FONT_SIZE_THEMESCREEN, black,
                   './Fonts/Bright Orchid.ttf')
        pygame.display.update()
        clock.tick(30)
    return next_scr

pixel_size = PIXEL_SIZE
img_pixel = IMG_PIXEL

# to draw a character
def draw_character(name, coor):
    game_disp.blit(name, coor)

# to get coordinates in pixel
def get_dimensional_coordinates(x, y):
    x = x * pixel_size + int((pixel_size - img_pixel) / 2)
    y = y * pixel_size + int((pixel_size - img_pixel) / 2)
    return (x, y)

def draw_maze(wall_img,maze_matrix,maze_row,maze_col):
    for i in range(maze_row):
        for j in range(maze_col):
            if maze_matrix[i][j] == 1:
                game_disp.blit(wall_img, (j * pixel_size, i * pixel_size))

def draw_corners(corner_img,maze_matrix,maze_row,maze_col):
    for i in range(maze_row):
        for j in range(maze_col):
            if maze_matrix[i][j] == 3:
                game_disp.blit(corner_img, (j * pixel_size, i * pixel_size))

def draw_item(item_img,maze_matrix,maze_row,maze_col):
    for i in range(maze_row):
        for j in range(maze_col):
            if maze_matrix[i][j] == 0:
                game_disp.blit(item_img, (get_dimensional_coordinates(j, i)))

def calculate_score(maze_matrix, score, x, y):
    if maze_matrix[y][x] == 0:
        score = score + 10
        maze_matrix[y][x] = 2
    return score

def isObstacle(maze_matrix, x, y):
    if maze_matrix[y][x] == 0 or maze_matrix[y][x] == 2:
        return False
    return True

def position_valid(maze_matrix,maze_row,maze_col,x, y):
    if isObstacle(maze_matrix,x, y):
        return False
    elif x < 1 or x > maze_col:
        return False
    elif y < 1 or y > maze_row:
        return False
    return True

def print_score(score):
    score_font = pygame.font.Font("./Fonts/Bright Orchid.ttf", SCORE_FONT_SIZE)
    scorecard = score_font.render("Score : " + str(score), True, white)
    game_disp.blit(scorecard, (0, 0))

def kill(ghost1_x, ghost1_y, player_x, player_y):
    if ghost1_x == player_x and ghost1_y == player_y:
        return True
    else:
        return False

def win_condition(maze_matrix, maze_row, maze_col):
    global result
    flag = 0
    for i in range(maze_row):
        for j in range(maze_col):
            if maze_matrix[i][j] == 0:
                flag = 1
                result = False
                break
    if flag == 0:
        result = True
    return result

def ghost_move(maze_matrix, maze_row, maze_col, ghost1_x, ghost1_y, kill=False):
    global ghost1_x_change, ghost1_y_change
    if kill:
        return ghost1_x, ghost1_y
    move = random.randint(1, 4)

    if move == 1:
        ghost1_y_change = 0
        ghost1_x_change = -1
    elif move == 2:
        ghost1_y_change = 0
        ghost1_x_change = 1
    elif move == 3:
        ghost1_x_change = 0
        ghost1_y_change = -1
    elif move == 4:
        ghost1_x_change = 0
        ghost1_y_change = 1

    if not position_valid(maze_matrix, maze_row, maze_col, ghost1_x + ghost1_x_change, ghost1_y + ghost1_y_change):
        ghost1_x_change = 0
        ghost1_y_change = 0

    ghost1_x += ghost1_x_change
    ghost1_y += ghost1_y_change

    return ghost1_x, ghost1_y

############################################ T&J 3GHOST PLAY SCREEN ####################################################

def game(selected_theme,ghost_status):
    maze_matrix = [[1] * MAZE_COL] * MAZE_ROW
    maze_row = MAZE_ROW
    maze_col = MAZE_COL

    score = INITIAL_SCORE - COIN_COLLECT_POINT  #Initially player lands on a coin!
    player_x = PLAYER_X
    player_y = PLAYER_Y
    change_x = 0
    change_y = 0

    if(selected_theme == 1):

        if ghost_status==0:
            ghost1_x = data["level1"]["GHOST1_X"]
            ghost1_y = data["level1"]["GHOST1_Y"]
            ghost2_x = data["level1"]["GHOST2_X"]
            ghost2_y = data["level1"]["GHOST2_Y"]
            ghost3_x = data["level1"]["GHOST3_X"]
            ghost3_y = data["level1"]["GHOST3_Y"]
            # 3 Ghosts Case - Put invalid coordinates for ghost 4
            ghost4_x = -5
            ghost4_y = -5
            # 3 for corners, 0 for items, 1 for walls and 2 for void positions
            maze_matrix = data["level1"]["maze_matrix"]
        else:
            ghost1_x = data["level2"]["GHOST1_X"]
            ghost1_y = data["level2"]["GHOST1_Y"]
            ghost2_x = data["level2"]["GHOST2_X"]
            ghost2_y = data["level2"]["GHOST2_Y"]
            ghost3_x = data["level2"]["GHOST3_X"]
            ghost3_y = data["level2"]["GHOST3_Y"]
            # 4 Ghosts Case
            ghost4_x = data["level2"]["GHOST4_X"]
            ghost4_y = data["level2"]["GHOST4_Y"]
            # 3 for corners, 0 for items, 1 for walls and 2 for void positions
            maze_matrix = data["level2"]["maze_matrix"]


        player_img = player_tj
        ghost1_img = ghost1_img_tj
        ghost2_img = ghost2_img_tj
        ghost3_img = ghost3_img_tj
        ghost4_img = ghost4_img_tj
        wall_img = wall_tj
        corner_img = corner_tj
        item_img = item_tj

    elif (selected_theme == 2):
        if ghost_status == 0:
            ghost1_x = data["level3"]["GHOST1_X"]
            ghost1_y = data["level3"]["GHOST1_Y"]
            ghost2_x = data["level3"]["GHOST2_X"]
            ghost2_y = data["level3"]["GHOST2_Y"]
            ghost3_x = data["level3"]["GHOST3_X"]
            ghost3_y = data["level3"]["GHOST3_Y"]
            # 3 Ghosts Case - Put invalid coordinates for ghost 4
            ghost4_x = -5
            ghost4_y = -5
            # 3 for corners, 0 for items, 1 for walls and 2 for void positions
            maze_matrix = data["level3"]["maze_matrix"]
        else:
            ghost1_x = data["level4"]["GHOST1_X"]
            ghost1_y = data["level4"]["GHOST1_Y"]
            ghost2_x = data["level4"]["GHOST2_X"]
            ghost2_y = data["level4"]["GHOST2_Y"]
            ghost3_x = data["level4"]["GHOST3_X"]
            ghost3_y = data["level4"]["GHOST3_Y"]
            # 4 Ghosts Case
            ghost4_x = data["level4"]["GHOST4_X"]
            ghost4_y = data["level4"]["GHOST4_Y"]
            # 3 for corners, 0 for items, 1 for walls and 2 for void positions
            maze_matrix = data["level4"]["maze_matrix"]


        player_img = player_christmas
        ghost1_img = ghost1_img_christmas
        ghost2_img = ghost2_img_christmas
        ghost3_img = ghost3_img_christmas
        ghost4_img = ghost4_img_christmas
        wall_img = wall_christmas
        corner_img = corner_christmas
        item_img = item_christmas

    elif (selected_theme == 3):
        if ghost_status == 0:
            ghost1_x = data["level5"]["GHOST1_X"]
            ghost1_y = data["level5"]["GHOST1_Y"]
            ghost2_x = data["level5"]["GHOST2_X"]
            ghost2_y = data["level5"]["GHOST2_Y"]
            ghost3_x = data["level5"]["GHOST3_X"]
            ghost3_y = data["level5"]["GHOST3_Y"]
            # 3 Ghosts Case - Put invalid coordinates for ghost 4
            ghost4_x = -5
            ghost4_y = -5
            # 3 for corners, 0 for items, 1 for walls and 2 for void positions
            maze_matrix = data["level5"]["maze_matrix"]
        else:
            ghost1_x = data["level6"]["GHOST1_X"]
            ghost1_y = data["level6"]["GHOST1_Y"]
            ghost2_x = data["level6"]["GHOST2_X"]
            ghost2_y = data["level6"]["GHOST2_Y"]
            ghost3_x = data["level6"]["GHOST3_X"]
            ghost3_y = data["level6"]["GHOST3_Y"]
            # 4 Ghosts Case
            ghost4_x = data["level6"]["GHOST4_X"]
            ghost4_y = data["level6"]["GHOST4_Y"]
            # 3 for corners, 0 for items, 1 for walls and 2 for void positions
            maze_matrix = data["level6"]["maze_matrix"]

        player_img = player_halloween
        ghost1_img = ghost1_img_halloween
        ghost2_img = ghost2_img_halloween
        ghost3_img = ghost3_img_halloween
        ghost4_img = ghost4_img_halloween
        wall_img = wall_halloween
        corner_img = corner_halloween
        item_img = item_halloween

    ######################################## GAME LOOP ########################################

    end = False
    while not end:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_x = -1
                    change_y = 0
                elif event.key == pygame.K_RIGHT:
                    change_x = 1
                    change_y = 0
                elif event.key == pygame.K_UP:
                    change_x = 0
                    change_y = -1
                elif event.key == pygame.K_DOWN:
                    change_x = 0
                    change_y = 1
        if(selected_theme==1):
            game_disp.fill(green)
        elif(selected_theme==2):
            game_disp.fill(black)
        elif(selected_theme==3):
            game_disp.fill(black)
        draw_maze(wall_img,maze_matrix, maze_row, maze_col)
        draw_item(item_img,maze_matrix, maze_row, maze_col)
        draw_corners(corner_img,maze_matrix, maze_row, maze_col)
        draw_character(player_img, get_dimensional_coordinates(player_x, player_y))
        draw_character(ghost1_img, get_dimensional_coordinates(ghost1_x, ghost1_y))
        draw_character(ghost2_img, get_dimensional_coordinates(ghost2_x, ghost2_y))
        draw_character(ghost3_img, get_dimensional_coordinates(ghost3_x, ghost3_y))
        draw_character(ghost4_img, get_dimensional_coordinates(ghost4_x, ghost4_y))
        ghost1_x, ghost1_y = ghost_move(maze_matrix, maze_row, maze_col, ghost1_x, ghost1_y, kill(ghost1_x, ghost1_y, player_x, player_y))
        ghost2_x, ghost2_y = ghost_move(maze_matrix, maze_row, maze_col, ghost2_x, ghost2_y, kill(ghost2_x, ghost2_y, player_x, player_y))
        ghost3_x, ghost3_y = ghost_move(maze_matrix, maze_row, maze_col, ghost3_x, ghost3_y, kill(ghost3_x, ghost3_y, player_x, player_y))
        ghost4_x, ghost4_y = ghost_move(maze_matrix, maze_row, maze_col, ghost4_x, ghost4_y, kill(ghost4_x, ghost4_y, player_x, player_y))

        if not position_valid(maze_matrix, maze_row,maze_col, player_x + change_x, player_y + change_y):
            change_x = 0
            change_y = 0
        player_x += change_x
        player_y += change_y

        if (kill(ghost1_x, ghost1_y, player_x, player_y)
            or kill(ghost2_x, ghost2_y, player_x, player_y)
            or kill(ghost3_x, ghost3_y, player_x, player_y)
            or kill(ghost4_x, ghost4_y, player_x, player_y)):
            write_text("GAME OVER", game_disp, [window_width // 2, window_height // 2], 90, black, './Fonts/Sunday Morning.ttf')
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            change_x = 0
            change_y = 0

        if win_condition(maze_matrix, maze_row, maze_col):
            write_text("YOU WIN !", game_disp, [window_width // 2, window_height // 2], 90, red, './Fonts/Bright Orchid.ttf')

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            change_x = 0
            change_y = 0

        score = calculate_score(maze_matrix, score, player_x, player_y)
        print_score(score)
        pygame.display.update()
        clock.tick(10)

################################################## MAIN BODY ###########################################################

next_scr = menu_scr()
if next_scr == "Tom & Jerry":
    next_scr = intro_screen()
    if next_scr == "ghosts_3":
        game(1,0)
    elif next_scr == "ghosts_4":
        game(1,1)
elif next_scr == "Christmas":
    next_scr = intro_screen()
    if next_scr == "ghosts_3":
        game(2,0)
    elif next_scr == "ghosts_4":
        game(2,1)
elif next_scr == "Halloween":
    next_scr = intro_screen()
    if next_scr == "ghosts_3":
        game(3,0)
    elif next_scr == "ghosts_4":
        game(3,1)

