import time
import pygame
import sys
#https://www.youtube.com/watch?v=zahxNZYvvj8
#https://www.pygame.org/docs/ref/mouse.html
#TO DO:
#add buttons to start over
#add rules
#adjust screen size to board size? probably not.....

    
p1,p2,empty = 1,2,0 

board_colors = [(0,250,154),(119,136,153),(255,0,0)]  
player_colors = [(255,255,255),(0,0,0)]
if len(sys.argv) <3 or (not sys.argv[1].isnumeric()) or int(sys.argv[1]) > 25 or (not sys.argv[2].isnumeric()) or int(sys.argv[2]) > 25:   #max dim = 25
    dim = [6,5]  #if not specified, set default dim to 5


size = (700,500)        #screen width,height
else:
    dim = [int(sys.argv[1]),int(sys.argv[2])]
if dim[0] > dim[1]:
    square_size = size[1] // dim[0]
else: 
    square_size = size[1] // dim[1]

def check_finished(B):
    #check if there are any moves left to make, ie if a black and white cell are on horizontally or vertically adjacent cells
    done = True
    for row in range(dim[0]):
        for col in range(dim[1]):
            if B[row][col] == 1:
                done = check_neighbors(B, row, col, 1)
            elif B[row][col] == 2:
                done = check_neighbors(B, row, col, 2)
            if done == False:
                return done
    return done


def check_neighbors(B, row, col, player):
    #returns False if it has a neighbor that has an opponent's stone on it (veritcal/horizontal neighbors only)
    if player == 1:
        check = 2
    else:
        check = 1
    if row > 0: 
        if B[row-1][col] == check:
            return False
    if row < dim[0]-1:
        if B[row+1][col] == check: 
            return False
    if col > 0:
        if B[row][col-1] == check: 
            return False
    if col < dim[1]-1:
        if B[row][col+1] == check: 
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

def initialBoard(B,players,screen):
    #create intial board to store occupied/empty info, fill entire board with stones for p1,p2
    B = []
    players = [p1,p2]
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

    return B








def main():
    # initialize all pygame modules
    pygame.init()

    # create a pygame display window
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Clobber")
    background_color = (47,79,79)
    screen.fill(background_color)  #background

    
    #create intial board to store occupied/empty info, fill entire board with stones for p1,p2
    B = []
    players = [p1,p2]
    B = initialBoard(B, players, screen)
    displayText(screen, "Moves: ", "0", "top")


    clock = pygame.time.Clock()     # = how fast the screen updates
    player = p1
    square_selected = False
    stop = False
    moves =0
    while not stop:
        if check_finished(B) == True:
            if player == 1:
                winner = 2
            else:
                winner = 1
            displayText(screen, "Game Over", "Player " + str(winner) + " wins", "bottom")
            stop = True
        event = pygame.event.poll()     #look for event
        if event.type == pygame.QUIT:
                stop = True
                pygame.quit()
                sys.exit()
        #mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_posn = pygame.mouse.get_pos()
            if click_posn[0] < square_size * dim[1] and click_posn[1] < square_size * dim[0]: #if click within bounds of board
                idx_col = click_posn[0] // square_size 
                idx_row = click_posn[1] // square_size 
                if player == B[idx_row][idx_col]:   # check if player clicked own stone
                    if square_selected != False:       # selects a different one of his own stones
                        eraseSquare(square_selected, screen, B) # erase background red from previously selected stone
                        placeStone(square_selected, player, screen, B) # then fill again with correct stone 
                    square_selected = (idx_row,idx_col)  #newly selected stone
                    screen.fill(board_colors[2], (idx_col * square_size, idx_row * square_size,square_size,square_size))  #paint red
                    placeStone((idx_row, idx_col), player, screen, B)
                elif B[idx_row][idx_col] != empty and player != B[idx_row][idx_col] and square_selected != False:  #if chose opponent's stone to capture
                    if (idx_row == square_selected[0] and (square_selected[1]-1 <= idx_col <= square_selected[1] +1)) or (idx_col == square_selected[1] and (square_selected[0] -1<= idx_row <= square_selected[0] +1)): #check if legal move, ie verical or horizontal neighbor
                        eraseSquare(square_selected, screen, B) #erase square from which player moved their stone
                        placeStone((idx_row,idx_col), player, screen, B) #replace opponent's stone with own
                        B[idx_row][idx_col] = player #update board 
                        moves += 1
                        screen.fill(background_color, (size[0]-170,0,size[0],170))#                     dim[1]*square_size,0,size[0]-dim[0]*square_size, size[1]))
                        displayText(screen, "Moves: ", str(moves), "top") #update nr of moves


                        if player == p1: 
                            player = p2
                        else: 
                            player = p1
                        square_selected = False
        pygame.display.flip() # display screen
        clock.tick(60) # limit to 60 frames per second
    # play(B, screen)
    # event = pygame.event.poll()     #look for event
    # if event.type == pygame.QUIT:
    #     pygame.quit()
    #     sys.exit()
    

    # Close the window, quit game
    # pygame.quit()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


main()

