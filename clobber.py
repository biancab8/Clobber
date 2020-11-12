import time, pygame, sys
from collections import deque
#https://www.youtube.com/watch?v=zahxNZYvvj8
#https://www.pygame.org/docs/ref/mouse.html
#command line: clobber.py dim1 dim2 opt
    #dim1 = nr of rows, dim2 = nr of cols
    #opt = 1: comp will choose a stone from the largest connected component of white stones
    #opt = 2: comp will choose a stone from the smallest connected component of white stones

p1,comp,empty = 1,2,0 
board_colors = [(0,250,154),(119,136,153),(255,0,0)]  # squares colors
player_colors = [(255,255,255),(0,0,0)]  # white, black

#check for input of dimensions
if len(sys.argv) <3 or (not sys.argv[1].isnumeric()) or int(sys.argv[1]) > 25 or (not sys.argv[2].isnumeric()) or int(sys.argv[2]) > 25 or int(sys.argv[2]) < 2:  #max dim = 25
    dim = [5,5]  #if not specified, set default dim to 5
else: 
    dim = [int(sys.argv[1]),int(sys.argv[2])]
size = (700,500)        #screen width,height
if dim[0] > dim[1]:
    square_size = size[1] // dim[0]
else: 
    square_size = size[1] // dim[1]
if len(sys.argv) > 3 and sys.argv[3].isnumeric() and int(sys.argv[3]) > 0 and int(sys.argv[3]) < 3:
    opt = int(sys.argv[3])
else:
    opt = 1 #default: longest connected component algo 

def check_finished(B):
    #check if there are any moves left to make, ie if a black and white cell are on horizontally or vertically adjacent cells
    done = True
    for row in range(dim[0]):
        for col in range(dim[1]):
            if B[row][col] == 1:
                done = check_neighbors(B, row, col, 1, 0)
            elif B[row][col] == 2:
                done = check_neighbors(B, row, col, 2, 0)
            if done == False:
                return done
    return done


def check_neighbors(B, row, col, player, opt):
    #returns False if it has a neighbor that has an opponent's stone on it (veritcal/horizontal neighbors only)
    #if opt = 1: return the cell where neighbor is
    if player == 1:
        check = 2
    else:
        check = 1
    if row > 0: 
        if B[row-1][col] == check:
            if opt == 1: 
                return [row-1, col]
            else: 
                return False
    if row < dim[0]-1:
        if B[row+1][col] == check: 
            if opt == 1:
                return [row+1, col]
            else:
                return False
    if col > 0:
        if B[row][col-1] == check: 
            if opt == 1: 
                return [row, col-1]
            else: 
                return False
    if col < dim[1]-1:
        if B[row][col+1] == check: 
            if opt == 1: 
                return [row, col+1]
            else: 
                return False
    return True

def displayText(screen, txt1, txt2, position):
    if position == "top":
        div1 = 5
        div2 = 3.5
    else: 
        div1 = 2.25
        div2 = 1.75
    offset = 170
    font = pygame.font.SysFont('Times New Roman', 25)
    text = font.render(txt1, False, (255,255,255))
    text_location = ((dim[1]*square_size + (size[0] - dim[1]*square_size) - offset), size[1] //div1)
    screen.blit(text, text_location)
    text = font.render(txt2, False, (255,255,255))
    text_location = ((dim[1]*square_size + (size[0] - dim[1]*square_size) - offset), size[1] //div2)
    screen.blit(text, text_location)
    font = pygame.font.SysFont('Times New Roman', 17)
    text = font.render("hit space to start over", False, (255,255,255))
    text_location = ((dim[1]*square_size + (size[0] - dim[1]*square_size) - offset), size[1] //1.25)
    screen.blit(text, text_location)

def eraseSquare(selected_square, screen, B):
    if (selected_square[0] % 2 == 0 and selected_square[1] % 2 == 0) or (selected_square[0] % 2 == 1 and selected_square[1] % 2 == 1):  #if board color 1 field
        color = board_colors[0]
    else:                                                                   #if board color 2 field
        color = board_colors[1]
    screen.fill(color, (selected_square[1] * square_size, selected_square[0] * square_size,square_size,square_size))   # erase stone that was just moved
    B[selected_square[0]][selected_square[1]] = empty 

def placeStone(square, player, screen, B):
    pygame.draw.circle(screen,player_colors[player-1], (square[1]*square_size+square_size//2, square[0]*square_size+square_size//2),square_size//2 - square_size//10 )
    B[square[0]][square[1]] = player

def setInitialBoard(B,players,screen):
    #create intial board to store occupied/empty info, fill entire board with stones for p1,comp
    B = []
    players = [p1,comp]
    for row in range(dim[0]):
        B.append([]) 
        for col in range(dim[1]):
            B[row].append(players[(row+col)%2])  #B = [[1, 2, 1, 2, 1], [2, 1, 2, 1, 2], ...]
    #draw inital grid on screen, fill with stones
    for row in range(dim[0]):
        for col in range(dim[1]):
            if B[row][col] == 1 or B[row][col] == 2:
                idx = (B[row][col]-1)   #for colors
                screen.fill(board_colors[idx], (col * square_size, row * square_size, square_size, square_size) )
                pygame.draw.circle(screen,player_colors[idx], (col * square_size+square_size//2, row * square_size+square_size//2),square_size//2 - square_size//10 )
    displayText(screen, "Moves: ", "0", "top")
    return B


def get_path_length(B, row, col):
    # from cell (row,col) get the longest path of connected stones of own color
    offsets = [[0,-1], [0,1], [1,0], [-1,0]]
    seen = []
    length = 1
    fringe = deque() 
    fringe.append([row,col])
    add = False
    while len(fringe) > 0:
        cell_coords = fringe.popleft()
        seen.append(cell_coords)
        for offset in offsets: 
            if cell_coords[0] + offset[0] >= 0 and cell_coords[0] + offset[0] < dim[0] and cell_coords[1] + offset[1] >= 0 and cell_coords[1] + offset[1] < dim[1]:
                new_cell = [cell_coords[0]+offset[0],cell_coords[1]+offset[1]]
                if new_cell not in seen: 
                    if B[new_cell[0]][new_cell[1]] == 1 and new_cell not in fringe:
                        fringe.append(new_cell)
                        add = True
        if add == True: 
            length += 1
            add = False 
    return length
     

def find_best_move(B):
    #find best move for comp based on:
    #if opt == 1: longest connected component of opponent's stones
    #if opt == 2: shortest connected component of opponent's stones
    if opt == 1:    #largest connected component
        best_len_so_far = 0
    else:           #shortest connected component  
        best_len_so_far = float("inf")
    best_cell_so_far = []
    best_move_from = []
    for row in range(dim[0]): 
        for col in range(dim[1]):
            #if white (human's) stone and has black nbr:  (note: check_neighbors returns false if there is a black nbr)
            if B[row][col] == 1 and check_neighbors(B, row, col, p1, 0) == False:
                #find max nr of white stones in a row
                length = get_path_length(B,row,col)
                if opt == 1 and length > best_len_so_far: 
                    best_len_so_far = length 
                    best_cell_so_far = [row,col]
                elif opt == 2 and length < best_len_so_far:
                    best_len_so_far = length 
                    best_cell_so_far = [row,col]
    best_move_from = check_neighbors(B, best_cell_so_far[0], best_cell_so_far[1], p1, 1)
    return [best_move_from, best_cell_so_far]


def displayWinner(player, screen):
    if player == 1:
        winner = "Black"
    else:
        winner = "White"
    displayText(screen, "Game Over", winner + " wins", "bottom")


def main():
    # initialize all pygame modules, create pygame display window
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()     # = how fast the screen updates
    pygame.display.set_caption("Clobber")
    background_color = (47,79,79)
    screen.fill(background_color)  #background

    #create and display intial board, fill entire board with stones for p1, p2
    players = [p1,comp]
    B = setInitialBoard([], players, screen)

    player = p1
    square_selected = False
    cont = True
    moves =0
    while cont:
        if check_finished(B) == True:  # check if win
            displayWinner(player, screen)
        pygame.display.flip() # display screen
        clock.tick(60) # limit to 60 frames per second
        play = False
        while not play:  # pause game while wait for p1 event to happen
            event = pygame.event.wait()
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit() 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # start over
                screen.fill(background_color)
                B = setInitialBoard([], players, screen)
                player = p1
                square_selected = False
                moves =0
                pygame.display.flip() # display screen
            elif player == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                play = True
            
        #human to move
        if player == 1 and play == True: 
                click_posn = pygame.mouse.get_pos()
                if click_posn[0] < square_size * dim[1] and click_posn[1] < square_size * dim[0]: #if click within bounds of board
                    idx_col = click_posn[0] // square_size 
                    idx_row = click_posn[1] // square_size 
                    if player == B[idx_row][idx_col]:   # check if player clicked own stone
                        if square_selected != False:       # picks different (own) stone
                            eraseSquare(square_selected, screen, B) # erase red background from previously selected stone
                            placeStone(square_selected, player, screen, B) # fill again with correct stone 
                        square_selected = (idx_row,idx_col)  #newly selected stone
                        screen.fill(board_colors[2], (idx_col * square_size, idx_row * square_size,square_size,square_size))  #paint red
                        placeStone((idx_row, idx_col), player, screen, B)
                    elif B[idx_row][idx_col] != empty and player != B[idx_row][idx_col] and square_selected != False:  #if chose opponent's stone to capture
                        if (idx_row == square_selected[0] and (square_selected[1]-1 <= idx_col <= square_selected[1] +1)) or (idx_col == square_selected[1] and (square_selected[0] -1<= idx_row <= square_selected[0] +1)): #check if legal move, ie verical or horizontal neighbor
                            eraseSquare(square_selected, screen, B) #erase square from which player moved their stone
                            placeStone((idx_row,idx_col), player, screen, B) #replace opponent's stone with own
                            B[idx_row][idx_col] = player #update board state
                            moves += 1
                            screen.fill(background_color, (size[0]-170,0,size[0],170))
                            displayText(screen, "Moves: ", str(moves), "top") #update nr of moves
                            if player == p1: 
                                player = comp
                            else: 
                                player = p1
                            square_selected = False
        # computer to move
        if check_finished(B) == False and player == comp and play == True:
            move = find_best_move(B)
            move_from = move[0]
            move_to = move[1]
            screen.fill(board_colors[2], (move_from[1] * square_size, move_from[0] * square_size,square_size,square_size))
            placeStone((move_to[0], move_to[1]), player, screen, B)
            eraseSquare(move_from, screen, B) #erase square from which player moved their stone
            play = False
            player = 1

    # Close game if click x
    if event.type == pygame.QUIT:
        pygame.quit()


main()

