## Clobber

### Here is a video that shows this project in action:
https://share.vidyard.com/watch/Ba4bUrfeM5YP23MvQ2ko9J?

### Rules:
Clobber is a two-player game, typically played on a 5x5 checkerboard. Initially, the entire board is occupied by black and white pieces. White pieces are placed on dark squares, and black pieces on white squares. White starts. A legal move is one where a piece is moved to an orthogonally adjacent square that is occupied by an opponent’s piece. The opponent’s piece is captured (“clobbered”) and removed from the board. The last player to move wins. No draws are possible, diagonal moves are not allowed. 

### How to run the program: 
for example: **python clobber.py 3 5 2** will open a 3x5 board with algorithm option number 2  
Note: All parameters are optional. If none are provided, the program will use a 5x5 board with algorithm option number 1.   

Optional Parameters:   
- board size:
  - the first number will be the number of rows, the second will be the number of columns.    
  - for example, **python clobber.py 5 6** will open a 5x6 board
  - number of rows must be >= 2 and <= 25
  - number of columns must be >= 1 and <= 25
- algorithm to use - There are 3 algorithms to choose from: 
  - if you choose option 1, the computer will always choose to capture a stone from the largest connected component of your color.  
  - if you choose option 2, the computer will always choose to capture a stone from the smallest connected component of your color. 
  - if you choose option 3, the computer will randomly choose a stone to capture. 
  - for example, **python clobber.py 2** will use algorithm 2 as described above  
  
When combining the parameters, please put the dimensions first, then the algorithm option you wish to select. 
