import pygame

#https://www.youtube.com/watch?v=zahxNZYvvj8
#https://www.pygame.org/docs/ref/mouse.html
#TO DO:
# draws grid, populates with stones, have B which stores if black/white/empty/guard...WRONG! whne creating board, i only put all black in the B which stores the state of teh cell....change that..........


#if clicks wrong cell, tell them that
#add buttons to start over
# add sth tocheck if any possible moves left, if not end game
#use space under board to say who's turn it is
#make dim a user input



p1,p2,empty = 1,2,0 #-1
dim = 10
size = (700,500)        #screen width,height
square_size = size[1] // dim
board_colors = [(0,250,154),(119,136,153),(255,0,0)]
player_colors = [(255,255,255),(0,0,0)]



def main():
    # initialize all pygame modules
    pygame.init()


    # create a pygame display window
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Clobber")
    screen.fill((47,79,79))  #background


    #create board to store occupied/empty info
    #fill entire board with stones for p1,p2
    B = []
    players = [p1,p2]
    for row in range(dim):
        B.append([]) 
        for col in range(dim):
            B[row].append(players[(row+col)%2])  #B = [[1, 2, 1, 2, 1], [2, 1, 2, 1, 2], ...]
    # B.insert(0,[guard]*dim)   guard cells
    # B.append([guard] * (dim+1)) # now with guards [[-1, -1, -1, -1, -1], [-1, 1, 2, 1, 2, 1], ...,[-1, -1, -1, -1, -1, -1]]  guard cells


    #draw grid on screen, fill with stones
    for row in range(dim):
        for col in range(dim):
            if B[row][col] == 1 or B[row][col] == 2:
                idx = (B[row][col]-1)   #for colors
                square_coords = (col * square_size, row * square_size, square_size, square_size) 
                screen.fill(board_colors[idx], (square_coords))
                pygame.draw.circle(screen,player_colors[idx], (square_coords[0]+square_size//2, square_coords[1]+square_size//2),square_size//2 - square_size//10 )

    clock = pygame.time.Clock()     # = how fast the screen updates
 
    player = p1
    stone_select = False
    stop = False
    while not stop:
        event = pygame.event.poll()     #look for event
        if event.type == pygame.QUIT:
                stop = True
                break 
        #mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_posn = pygame.mouse.get_pos()
            if click_posn[0] < square_size * dim and click_posn[1] < square_size * dim: #if click within bounds of board
                idx_col = click_posn[0] // square_size 
                idx_row = click_posn[1] // square_size 
                square_coords = (idx_col * square_size, idx_row * square_size, square_size, square_size) 
                if player == B[idx_row][idx_col] and stone_select == False:       # check if player clicked own stone
                    stone_select = (idx_row,idx_col)
                    
                    screen.fill(board_colors[2], (square_coords[0], square_coords[1],square_size,square_size))  #mark field with red
                    pygame.draw.circle(screen,player_colors[player-1], (square_coords[0]+square_size//2, square_coords[1]+square_size//2),square_size//2 - square_size//10 )
                elif B[idx_row][idx_col] != empty and player != B[idx_row][idx_col] and stone_select != False:  #chose opponent's stone
                    if (idx_row == stone_select[0] and (stone_select[1]-1 <= idx_col <= stone_select[1] +1)) or (idx_col == stone_select[1] and (stone_select[0] -1<= idx_row <= stone_select[0] +1)): #check if legal move
                        pygame.draw.circle(screen,player_colors[player-1], (square_coords[0]+square_size//2, square_coords[1]+square_size//2),square_size//2 - square_size//10 ) #draw own color in where opponent's was
                        B[idx_row][idx_col] = player #update board that stores players' colors
                        
                        # erase stone  --> works
                        if (idx_row % 2 == 0 and idx_col % 2 == 0) or (idx_row % 2 == 1 and idx_col % 2 == 1):  #if board color 1 field
                            square_color = board_colors[1]
                        else:                                                                                   #if board color 2 field
                            square_color = board_colors[0]
                        
                        screen.fill(square_color, (stone_select[1] * square_size, stone_select[0] * square_size,square_size,square_size))   # erase stone that was just moved
                        B[stone_select[0]][stone_select[1]] = empty 
                        if player == p1: 
                            player = p2
                        else: 
                            player = p1
                        stone_select = False
                        print(B)
             






        # --- Game logic should go here

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.


        # --- Drawing code should go here

        # display screen
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

        # Close the window and quit.
    pygame.quit()



main()

