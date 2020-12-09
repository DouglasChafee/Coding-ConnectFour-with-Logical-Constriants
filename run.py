from nnf import Var,true
from lib204 import Encoding

from nnf import NNF
from nnf.operators import iff

def implication(l, r):
    return l.negate() | r

def neg(f):
    return f.negate()

NNF.__rshift__ = implication
NNF.__invert__ = neg

def iff(left, right):
    return (left.negate() | right) & (right.negate() | left)

# Variable Declerations of the three possible outcomes in a model of Connect Four
BlackWin = Var("Black has Won the Game")
RedWin = Var("Red has Won the Game")
NoWin = Var("No one has Won the Game")

# ConnectFour Game Board Dimestions
rowNum = 6
columnNum = 7

# Creating variable boards for each color peice, empty peice, and partialCount variables. 
blackBoard=[]
redBoard=[]
emptyBoard=[]
blackPartialCount=[]
redPartialCount=[]
for i in range(rowNum): 
    blackBoard.append([])
    redBoard.append([])
    emptyBoard.append([])
    blackPartialCount.append([])
    redPartialCount.append([])
    for j in range(columnNum):
        blackBoard[i].append(Var(f"Black({i},{j})"))
        redBoard[i].append(Var(f"Red({i},{j})"))
        emptyBoard[i].append(Var(f"Empty({i},{j})"))
        blackPartialCount[i].append([])
        redPartialCount[i].append([])
        for k in range(rowNum * columnNum + 1):
          blackPartialCount[i][j].append(Var(f"Black Count at({i},{j}) is {k}"))
          redPartialCount[i][j].append(Var(f"Red Count at({i},{j}) is {k}"))

# Creating total piece count varaiable board
totalCount=[]          
for i in range(rowNum * columnNum + 1):
  totalCount.append(Var(f"Total Black Count is {i}"))

# Creating red and black row wins varaiable boards
blackRow=[]
redRow=[]
for i in range(rowNum): 
    blackRow.append([])
    redRow.append([])
    for j in range(columnNum - 3):
        blackRow[i].append(Var(f"BlackWinningRow({i},{j})"))
        redRow[i].append(Var(f"RedWinningRow({i},{j})"))


# Creating red and black diagonal wins varaiable boards
leftBlackDiagonal=[]
rightBlackDiagonal=[]
leftRedDiagonal=[]
rightRedDiagonal=[]
for i in range(rowNum- 3): 
    leftBlackDiagonal.append([])
    rightBlackDiagonal.append([])
    leftRedDiagonal.append([])
    rightRedDiagonal.append([])
    for j in range(columnNum - 3):
        leftBlackDiagonal[i].append(Var(f"LeftBlackWinningDiagonal({i},{j})"))
        rightBlackDiagonal[i].append(Var(f"RightBlackWinningDiagonal({i},{j})"))
        leftRedDiagonal[i].append(Var(f"LeftRedWinningDiagonal({i},{j})"))
        rightRedDiagonal[i].append(Var(f"RightRedWinningDiagonal({i},{j})"))

# Creating red and black column wins varaiable boards
blackColumn=[]
redColumn=[]
for i in range(rowNum- 3): 
    blackColumn.append([])
    redColumn.append([])
    for j in range(columnNum):
        blackColumn[i].append(Var(f"BlackWinningColumn({i},{j})"))
        redColumn[i].append(Var(f"RedWinningColumn({i},{j})"))

# Adds/creates constriants for a row of color, boardColor        
def rowWin(E, winRowColor, boardColor):
  for i in range(rowNum):
    for j in range(columnNum - 3):
      #Winning row and its position of either 4 red or 4 black slots within the row. 
      E.add_constraint(iff(winRowColor[i][j], (boardColor[i][j] & boardColor[i][j + 1] & boardColor[i][j + 2] & boardColor[i][j + 3]))) 

      #Checks that there is at least one possible route to play in order to win by a row unless top row
      if (i > 0):
        E.add_constraint(winRowColor[i][j] >> (emptyBoard[i-1][j] | emptyBoard[i-1][j + 1] | emptyBoard[i-1][j + 2] | emptyBoard[i-1][j + 3]))


      #Checks that only a single row channel can be a winning row channel
      special = winRowColor[i][j]
      false = ~true
      for i2 in range(rowNum):
        for j2 in range(columnNum - 3):
          if (i != i2):
            false |= winRowColor[i2][j2]
      E.add_constraint(special >> ~false)
  return E
        
# Adds/creates constriants for a column of color, boardColor
def columnWin(E, winColumnColor, boardColor):
  for i in range(rowNum - 3):
    for j in range(columnNum):
      # Winning column and its position of either 4 red or 4 black slots within the column. 
      E.add_constraint(iff(winColumnColor[i][j], (boardColor[i][j] & boardColor[i+1][j] & boardColor[i+2][j] & boardColor[i+3][j])))

      # Checks that there is a possible route to play in order to win by a column unless top row
      if (i > 0):
        E.add_constraint(winColumnColor[i][j] >> (emptyBoard[i-1][j]))
      
      #Checks that only one column can win
      special = winColumnColor[i][j]
      false = ~true
      for i2 in range(rowNum - 3):
        for j2 in range(columnNum):
          if (i != i2) | (j != j2):
            false |= winColumnColor[i2][j2]
      E.add_constraint(special >> ~false)
  return E

# Adds/creates contraints that limits the position where a color's column can be, 
# if other rows or diagonals are also true for that same color. 
def columnRules(E, winColumnColor, winRowColor, leftWinDiagonalColor, rightWinDiagonalColor):
  for i in range(rowNum - 3):
    for j in range(columnNum):
      special = winColumnColor[i][j]
      false = ~true
      for i2 in range(rowNum):
        for j2 in range(columnNum):
          if (j2 < columnNum - 3):
            if ((i != i2) | ((j - j2) >= 4)):
              false |= winRowColor[i2][j2]  # Last piece of color's column must be somewhere in color's row
          if (j2 < (columnNum - 3)):
            if (i2 < rowNum - 3):
              if (((i != i2) | (j != j2)) & ((i-1 != i2) | (j-1 != j2)) & ((i-2 != i2) | (j-2 != j2)) & ((i-3 != i2) | (j-3 != j2))):
                false |= leftWinDiagonalColor[i2][j2]  # Last piece of color's column must be somewhere in color's left diagonal

              if (((i != i2) | (j != j2 + 3)) & ((i-1 != i2) | (j+1 != j2 + 3)) & ((i-2 != i2) | (j+2 != j2 + 3)) & ((i-3 != i2) | (j+3 != j2 + 3))):
                false |= rightWinDiagonalColor[i2][j2] # Last piece of color's column must be somewhere in color's right diagonal
      E.add_constraint(special >> ~false)
  return E

# Adds/creates constriants for a right facing diagonal of color, boardColor
def leftDiagonalWin(E, leftWinDiagonalColor, boardColor):
  for i in range(rowNum - 3):
    for j in range(columnNum - 3):

      #Winning diagonal going right and down.
      E.add_constraint(iff(leftWinDiagonalColor[i][j], (boardColor[i][j] & boardColor[i+1][j+1] & boardColor[i+2][j+2] & boardColor[i+3][j+3])))

      # Checks that there is a possible route to play in order to win by a left diagonal unless top row
      if (i > 0):
        E.add_constraint(leftWinDiagonalColor[i][j] >> (emptyBoard[i-1][j] | emptyBoard[i][j+1] | emptyBoard[i+1][j+2] | emptyBoard[i+2][j+3]))   
      
      #Only one left facing diagonal channel can be a winning diagonal channel
      special = leftWinDiagonalColor[i][j]
      false = ~true
      for i2 in range(rowNum - 3):
        for j2 in range(columnNum - 3):
          if (i != i2) | (j != j2):
            if (i + 1 != i2) | (j + 1 != j2):
              if (i + 2 != i2) | (j + 2 != j2):
                 if (i - 1 != i2) | (j - 1 != j2):
                   if (i - 2 != i2) | (j - 2 != j2):
                      false |= leftWinDiagonalColor[i2][j2]
      E.add_constraint(special >> ~false)
  return E

# Adds/creates constriants for a right facing diagonal of color, boardColor
def rightDiagonalWin(E, rightWinDiagonalColor, boardColor):
  for i in range(rowNum - 3):
    for j in range(columnNum - 4, columnNum):
      #Winning diagonal going left and down.
      E.add_constraint(iff(rightWinDiagonalColor[i][j-3], (boardColor[i][j] & boardColor[i+1][j-1] & boardColor[i+2][j-2] & boardColor[i+3][j-3])))

      # Checks that there is a possible route to play in order to win by a right diagonal unless top row
      if (i > 0):
        E.add_constraint(rightWinDiagonalColor[i][j-3] >> (emptyBoard[i-1][j] | emptyBoard[i][j-1] | emptyBoard[i+1][j - 2] | emptyBoard[i+2][j - 3]))

      # Only one right facing diagonal channel can be a winning diagonal channel
      special = rightWinDiagonalColor[i][j-3]
      false = ~true
      for i2 in range(rowNum - 3):
        for j2 in range(columnNum - 4, columnNum):
          if (i != i2) | (j != j2):
            if (i - 1 != i2) | (j + 1 != j2):
              if (i - 2 != i2) | (j + 2 != j2):
                 if (i + 1 != i2) | (j - 1 != j2):
                   if (i + 2 != i2) | (j - 2 != j2):
                    false |= rightWinDiagonalColor[i2][j2-3]
      E.add_constraint(special >> ~false)
  return E

# Add constriants to check if all occupied position below current is occupied position
def gravityRule(i, j):
  f = true
  for slot in range(i + 1, rowNum):
    f &= ~emptyBoard[slot][j]
  return f

# Holds constraints/rules that make up a valid connect four board.
def validBoard(E):
  for i in range(rowNum):
    for j in range(columnNum): 

      # If position(i, j) is empty, then neither black or red can occupy position(i, j).
      E.add_constraint(emptyBoard[i][j] >> (~redBoard[i][j] & ~blackBoard[i][j]))

      # If position(i, j) is red, then neither black and empty can occupy position(i, j)
      # Calls gravity constraint
      E.add_constraint(redBoard[i][j] >> (~blackBoard[i][j] & ~emptyBoard[i][j] & gravityRule(i, j)))

      # If position(i, j) is black, then neither red and empty can occupy position(i, j)
      # Calls gravity constraint
      E.add_constraint(blackBoard[i][j] >> (~redBoard[i][j] & ~emptyBoard[i][j] & gravityRule(i, j)))

      # Here to make sure implication works properly above, exactly one has to be true.
      E.add_constraint(emptyBoard[i][j] | redBoard[i][j] | blackBoard[i][j])

  # General: ColorWin if and only if there is ColorRowWin, or  
  # ColorColumnWin, or ColorDiagonalWin.
  E.add_constraint(iff(BlackWin, (BlackColumnWin() | BlackRowWin() | leftBlackDiagonalWin() | rightBlackDiagonalWin())))
  E.add_constraint(iff(RedWin, (RedColumnWin() | RedRowWin() | leftRedDiagonalWin() | rightRedDiagonalWin())))

  # General: NoWin if and only if there is notColorRowWin, and 
  # notColorColumnWin, and notColorDiagonalWin.
  E.add_constraint(iff(NoWin, ((~BlackColumnWin() & ~BlackRowWin() & ~leftBlackDiagonalWin() & ~rightBlackDiagonalWin()) & (~RedColumnWin() & ~RedRowWin() & ~leftRedDiagonalWin() & ~rightRedDiagonalWin()))))
  
  #All posibilities of Connect Four Game outcome
  E.add_constraint(iff(BlackWin, (~RedWin & ~NoWin)))
  E.add_constraint(iff(RedWin, (~BlackWin & ~NoWin)))
  E.add_constraint(iff(NoWin, (~RedWin & ~BlackWin)))

  return E

# Checks if any black row is true, return false if one is not found
def BlackRowWin():
  f = ~true
  for i in range(rowNum): 
      for j in range(columnNum - 3):
        f |= blackRow[i][j]
  return f

# Checks if any red row is true, return false if one is not found
def RedRowWin():
  f = ~true
  for i in range(rowNum): 
      for j in range(columnNum - 3):
        f |= redRow[i][j]
  return f 

# Checks if any black column is true, return false if one is not found
def BlackColumnWin():
  f = ~true
  for i in range(rowNum- 3): 
      for j in range(columnNum):
        f |= blackColumn[i][j]
  return f 

# Checks if any red column is true, return false if one is not found
def RedColumnWin():
  f = ~true
  for i in range(rowNum- 3): 
      for j in range(columnNum):
        f |= redColumn[i][j]
  return f 

# Checks if any left black diagonal is true, return false if one is not found
def leftBlackDiagonalWin():
  f = ~true
  for i in range(rowNum- 3): 
      for j in range(columnNum - 3):
        f |= leftBlackDiagonal[i][j]
  return f

# Checks if any right black diagonal is true, return false if one is not found
def rightBlackDiagonalWin():
  f = ~true
  for i in range(rowNum- 3): 
      for j in range(columnNum - 3):
        f |= rightBlackDiagonal[i][j]
  return f

# Checks if any left red diagonal is true, return false if one is not found
def leftRedDiagonalWin():
  f = ~true
  for i in range(rowNum- 3): 
      for j in range(columnNum - 3):
        f |= leftRedDiagonal[i][j]
  return f 

# Checks if any right red diagonal is true, return false if one is not found
def rightRedDiagonalWin():
  f = ~true
  for i in range(rowNum- 3): 
      for j in range(columnNum - 3):
        f |= rightRedDiagonal[i][j]
  return f 


# Prints a Connect Four board using computer assigned values from .solve dictionary
def printBoard(dic):
  board=[]
  for i in range(rowNum): 
    board.append([])
    for j in range(columnNum):
      board[i].append("-")
  if dic == None:
    print("NonSatisfiable Board")
    return []
  else:
    for key, value in dic.items():
      if (key[:6] == "Black(") and (value == True):
        xVal = int(key[-4])
        yVal = int(key[-2])
        board[xVal][yVal] = "B"
      elif (key[:4] == "Red(") and (value == True):
        xVal = int(key[-4])
        yVal = int(key[-2])
        board[xVal][yVal] = "R"
      elif (key == "Black has Won the Game") and (value == True):
        print("Black has Won the Game with:")
      elif (key == "Red has Won the Game") and (value == True):
        print("Red has Won the Game with:")
      elif (key == "No one has Won the Game") and (value == True):
        print("No one has Won the Game!")
  for row in board:
    print(row)

# Builds an example full theory of Connect Four for our setting and returns it.
def connectFour():
  E = Encoding()
  E = validBoard(E)
  E = rowWin(E, blackRow, blackBoard)
  E = rowWin(E, redRow, redBoard)
  E = columnWin(E, blackColumn, blackBoard)
  E = columnWin(E, redColumn, redBoard)
  E = leftDiagonalWin(E, leftBlackDiagonal, blackBoard)
  E = leftDiagonalWin(E, leftRedDiagonal, redBoard)
  E = rightDiagonalWin(E, rightBlackDiagonal, blackBoard)
  E = rightDiagonalWin(E, rightRedDiagonal, redBoard)
  E = columnRules(E, blackColumn, blackRow, leftBlackDiagonal, rightBlackDiagonal)
  E = columnRules(E, redColumn, redRow, leftRedDiagonal, rightRedDiagonal)
  E = sameCount(E, blackPartialCount, blackBoard)
  E = sameCount(E, redPartialCount, redBoard)
  return E

# Counting the number of peices of a single color,
# and making the number of black peices equal to the number of red peices on the board.
def sameCount(E, partialCount, boardColor):

  # Final partial counts should be equal to the full count
  for c in range(rowNum * columnNum + 1):
      E.add_constraint(iff(totalCount[c], partialCount[rowNum- 1][columnNum - 1][c]))

  # You can't have more pieces than you've already seen
  for i in range(rowNum):
      for j in range(columnNum):
        for c in range((i * 7) + j + 2,rowNum * columnNum + 1):
          E.add_constraint(~partialCount[i][j][c])

  # First index: only black piece or red piece could possibly be true
  E.add_constraint(iff(partialCount[0][0][0], ~boardColor[0][0]))
  E.add_constraint(iff(partialCount[0][0][1], boardColor[0][0]))

  #General pattern: Looks at the other color pieces to decide the current color piece.
  for x in range(1, rowNum * columnNum):
      i = x // columnNum
      j = x % columnNum
      E.add_constraint(iff(partialCount[i][j][0], partialCount[(i-1) if (j==0) else i][(columnNum-1) if (j==0) else (j-1)][0] & ~boardColor[i][j]))
      for c in range(1,x+2):
          increased = partialCount[(i-1) if (j==0) else i][(columnNum-1) if (j==0) else (j-1)][c-1] & boardColor[i][j]
          stay_same = partialCount[(i-1) if (j==0) else i][(columnNum-1) if (j==0) else (j-1)][c] & ~boardColor[i][j]
          E.add_constraint(iff(partialCount[i][j][c], increased | stay_same))
  return E

# Function exploring Black wins in our model of Connect Four.
def numBlackWins(E):
  E.add_constraint(BlackWin)
  return E.count_solutions()

# Function exploring Red wins in our model of Connect Four.
def numRedWins(E):
  E.add_constraint(RedWin)
  return E.count_solutions()

# Function exploring No wins in our model of Connect Four.
def numNoWins(E):
  E.add_constraint(NoWin)
  return E.count_solutions()

if __name__ == "__main__":

    E = connectFour()

    print("\nSatisfiable: %s" % E.is_satisfiable())

    # Uncomment if wanting to explore number of Black wins in our model of ConnectFour
    #print("# Solutions: %d" % numBlackWins())

    # Uncomment if wanting to explore number of Red wins in our model of ConnectFour
    #print("# Solutions: %d" % numRedWins())

    # Uncomment if wanting to explore number of No wins in our model of ConnectFour
    #print("# Solutions: %d" % numNoWins())

    dic = E.solve()
    print("   Solution: %s \n" % dic)
    printBoard(dic)
    
    # print("\nVariable likelihoods:")
    # print(" %s: %.2f" % (BlackWin, E.likelihood(BlackWin)))
    # print()
