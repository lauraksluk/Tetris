#################################################
# 15-112-m19 hw7
# Your Name: Laura (Kai Sze) Luk
# Your Andrew ID: kluk
# Collaborated with: cataylor
# Your Section: C
#################################################

from tkinter import *
import random

####################################

#Initializing variables
def init(data):
    #initializing board
    data.margin = 25
    data.rows = 15
    data.cols = 10
    data.cellSize = 20
    data.emptyColor = 'blue'
    data.isGameOver = False
    data.score = 0
    #creating board
    board = []
    for i in range(data.rows):
        board += [[data.emptyColor]*data.cols]
    data.board = board
    #seven standard pieces (tetrominoes)
    data.iPiece=[[True,True,True,True]]
    data.jPiece=[[True,False,False],[True,True,True]]
    data.lPiece=[[False,False,True],[True,True,True]]
    data.oPiece=[[True,True],[True,True]]
    data.sPiece=[[False,True,True],[True,True,False]]
    data.tPiece=[[False,True,False],[True,True,True]]
    data.zPiece=[[True,True,False],[False,True,True]]
    data.tetrisPieces = [data.iPiece,data.jPiece,data.lPiece,data.oPiece,
        data.sPiece,data.tPiece,data.zPiece]
    data.tetrisPieceColors = ['red','yellow','magenta','pink','cyan','green',
        'orange']
    #create random new falling piece
    newFallingPiece(data)

#Initializing board with 2d list of 'blue'
#Draws board by calling drawCell iteratively
def drawBoard(canvas,data):
    for i in range(data.rows):
        for j in range(data.cols):
            color = data.board[i][j]
            drawCell(canvas,data,i,j,color)

#Draws each cell in board, with color designated by row/col of cell
def drawCell(canvas,data,row,col,color):
    x0 = data.margin + col*data.cellSize
    y0 = data.margin + row*data.cellSize
    x1 = data.margin + (col+1)*data.cellSize
    y1 = data.margin + (row+1)*data.cellSize
    #extra thick width of lines
    thickness = 3
    canvas.create_rectangle(x0,y0,x1,y1,width=thickness,fill=color)

#Chooses terominoes randomly and displays centered, on top row
def newFallingPiece(data):
    #randomly choosing a piece from list of 7 Tetris pieces
    randomIndex = random.randint(0,len(data.tetrisPieces)-1)
    #setting data values to randomly chosen piece
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    #set row of falling piece to top of board
    data.fallingPieceRow = 0
    #set column of falling piece in center
    data.fallingPieceCol = (data.cols//2) - (len(data.fallingPiece[0])//2)

#Draws falling piece over current board
def drawFallingPiece(canvas,data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[i])):
            if data.fallingPiece[i][j]:
                color = data.fallingPieceColor
                #add offset to top row and left column of falling piece
                row = data.fallingPieceRow + i
                col = data.fallingPieceCol + j
                #calls drawCell to draw in falling piece
                drawCell(canvas,data,row,col,color)

#Moves falling tetrominoe by given change in row/col (legal moves)
def moveFallingPiece(data,drow,dcol):
    #new positions
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    #check if new position is legal
    if fallingPieceIsLegal(data) == False:
        #reset to original if not legal
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    else:
        return True

#Returns Boolean value depending on if all cells in falling piece is legal
def fallingPieceIsLegal(data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[i])):
            if data.fallingPiece[i][j]:
                #adding offset to top row and left col
                fallingRow = data.fallingPieceRow + i
                fallingCol = data.fallingPieceCol + j
                #false if piece goes off board or collided with non-empty cell
                if ((fallingRow < 0) or
                    (fallingCol < 0) or
                    (fallingRow > data.rows-1) or
                    (fallingCol > data.cols-1) or
                    (data.board[fallingRow][fallingCol] != data.emptyColor)):
                    return False
    return True

#Rotates falling Tetris piece 90 degrees counterclockwise
def rotateFallingPiece(data):
    #store data associated with old piece: dimension,location,piece
    oldPiece = data.fallingPiece
    oldNumRows,oldNumCols = len(data.fallingPiece),len(data.fallingPiece[0])
    oldCenterRow = data.fallingPieceRow + oldNumRows//2
    oldCenterCol = data.fallingPieceCol + oldNumCols//2
    #initializing 2d list for new piece with new dimensions
    newPiece = []
    for i in range(oldNumCols):
        newPiece += [[None]*oldNumRows]
    #move each value from original piece to new location in new piece
    for row in range(oldNumRows):
        for col in range(oldNumCols):
            newPiece[col][row] = oldPiece[row][oldNumCols-1-col]
    data.fallingPiece = newPiece
    #new number of rows/cols
    newNumRows,newNumCols = oldNumCols,oldNumRows
    #new location
    data.fallingPieceRow = oldCenterRow - newNumRows//2
    data.fallingPieceCol = oldCenterCol - newNumCols//2
    #if rotating it results in not legal piece, set values back to original
    if fallingPieceIsLegal(data) == False:
        data.fallingPiece = oldPiece
        data.fallingPieceRow = oldCenterRow - oldNumRows//2
        data.fallingPieceCol = oldCenterCol - oldNumCols//2

#Designates player keys
def keyPressed(event, data):
    #check that game is not over
    if data.isGameOver == False:
        #r key restarts game at any time
        if event.keysym == 'r':
            init(data)
        #down arrow key to move piece down
        if event.keysym == 'Down':
            moveFallingPiece(data,1,0)
        #left/right arrow keys to move tetrominoes
        if event.keysym == 'Left':
            moveFallingPiece(data,0,-1)
        if event.keysym == 'Right':
            moveFallingPiece(data,0,1)
        #up arrow key to rotate current piece
        if event.keysym == 'Up':
            rotateFallingPiece(data)
    else:
        #resets game/stops all game interaction except restart at game over
        if event.keysym == 'r':
            init(data)

#Sends new falling piece every 400 milliseconds
def timerFired(data):
    #check that game is not over
    if data.isGameOver == False:
        if moveFallingPiece(data,1,0) == False:
            #place piece at lowest available row
            placeFallingPiece(data)
            #starts new falling piece
            newFallingPiece(data)
            #game is over when falling piece is immediately illegal
            if fallingPieceIsLegal(data) == False:
                data.isGameOver = True

#Place falling piece on board by loading colors into cells
def placeFallingPiece(data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[i])):
            if data.fallingPiece[i][j]:
                #adding offset to top row/left col
                row = data.fallingPieceRow + i
                col = data.fallingPieceCol + j
                #setting color of board at indices to color of falling piece
                data.board[row][col] = data.fallingPieceColor
    removeFullRows(data)

#Clear any full rows during game
def removeFullRows(data):
    fullRows = 0
    newRow = data.rows - 1
    #copy over rows from bottom up
    for prevRow in range(data.rows-1,-1,-1):
        #copy over non-full rows
        if data.emptyColor in data.board[prevRow]:
            for col in range(0,data.cols):
                data.board[newRow][col] = data.board[prevRow][col]
            #shift rows down on board
            newRow -= 1
        else:
            #increment number of cleared rows
            fullRows += 1
    #update score by squared of cleared rows
    data.score += fullRows**2

#Displays score on top of screen, above board
def drawScore(canvas,data):
    scoreX = data.width//2
    scoreY = 12
    score = 'Score: ' + str(data.score)
    canvas.create_text(scoreX,scoreY,text=score,font="Helvetica 15 bold")

#Displays game over message when user loses game
def drawGameOver(canvas,data):
    w = data.width//2
    h1 = data.height//2
    canvas.create_text(w,h1,text="GAME OVER",font="Helvetica 26 bold")
    spacing1 = 20
    h2 = h1 + spacing1
    score = 'Final Score: ' + str(data.score)
    canvas.create_text(w,h2,text=score,font="Helvetica 15 bold")
    spacing2 = 40
    h3 = h2+ spacing2
    canvas.create_text(w,h3,text="Press 'r' to play again!",
                                                font="Helvetica 13 bold")

#Draws on canvas for game
def redrawAll(canvas, data):
    if data.isGameOver == False:
        #drawing backgroud, board, score, falling piece
        canvas.create_rectangle(0,0,data.width,data.height,fill='orange')
        drawBoard(canvas,data)
        drawScore(canvas,data)
        drawFallingPiece(canvas,data)
    #when game is over, display game over message on background
    else:
        canvas.create_rectangle(0,0,data.width,data.height,fill='orange')
        drawGameOver(canvas,data)

####################################
# use the run function as-is
####################################

#Time based Tkinter animation run function
#Reference- http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 400 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

#Defines dimensions for board/game
def playTetris(rows = 15,cols = 10):
    margin = 25
    cellSize = 20
    width = (cellSize*cols) + (2*margin)
    height = (cellSize*rows) + (2*margin)
    run(width,height)

#Runs program to begin game
playTetris()