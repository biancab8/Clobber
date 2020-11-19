## Clobber

### Here is a video that shows this project in action:
https://share.vidyard.com/watch/Ba4bUrfeM5YP23MvQ2ko9J?

### Rules:
Clobber is best played with two players and takes an average of 15 minutes to play. It is suggested for ages 8 and up. It is typically played on a rectangular white and black checkerboard. Players take turns to move one of their own pieces onto an orthogonally adjacent opposing piece, removing it from the game. The winner of the game is the player who makes the last move (i.e. whose opponent cannot move).

To start the game, each of the squares on the checkerboard is occupied by a stone. White stones are placed on the white squares and black stones on the black squares. To move, the player must pick up one of his or her own stones and "clobber" an opponent's stone on an adjacent square, either horizontally or vertically. Once the opponent's stone is clobbered, it must then be removed from the board and replaced by the stone that was moved. The player who, on their turn, is unable to move, loses the game.
https://en.wikipedia.org/wiki/Clobber

### How to run the program: 
for example: **python clobber.py 3 5 2** will open a 3x5 board with algorithm option number 2  
Note: All parameters are optional. If none are provided, the program will use a 5x5 board with algorithm option number 2.   

Optional Parameters:   
- board size:
  - the first number will be the number of rows, the second will be the number of columns.    
  - for example, **python clobber.py 5 6** will open a 5x6 board
  - number of rows must be >= 2 and <= 25
  - number of columns must be >= 1 and <= 25
- algorithm to use. There are 3 algorithms to choose from: 
  - if you choose option 1, the computer will always choose to capture a stone from the largest connected component of your color.  
  - if you choose option 2, the computer will always choose to capture a stone from the smallest connected component of your color. 
  - if you choose option 3, the computer will randomly choose a stone to capture. 
  - for example, **python clobber.py 1** will use algorithm one as described above  
  
When combining the parameters, please put the dimensions first, then the algorithm option. 
