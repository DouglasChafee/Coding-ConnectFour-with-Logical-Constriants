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

# Ideas of variables to be turned into constraints
# L = Var("Black's turn")
# J = Var("Red's turn")
# Z = Var("This value is true when x is zero")
# W = Var("A winning game")
# P = Var("if either black or red has the option to win in one turn")
BlackWin = Var("Black has Won the Game")
RedWin = Var("Red has Won the Game")
NoWin = Var("No one has Won the Game")

# ConnectFour Game Board Dimestions
rowNum = 6
columnNum = 7

# Creating boards for all the possibilities of each variables 
blackBoard=[]
redBoard=[]
emptyBoard=[]
for i in range(rowNum): 
    blackBoard.append([])
    redBoard.append([])
    emptyBoard.append([])
    for j in range(columnNum):
        blackBoard[i].append(Var(f"Black({i},{j})"))
        redBoard[i].append(Var(f"Red({i},{j})"))
        emptyBoard[i].append(Var(f"Empty({i},{j})"))



blackRow=[]
redRow=[]
for i in range(rowNum): 
    blackRow.append([])
    redRow.append([])
    for j in range(columnNum - 3):
        blackRow[i].append(Var(f"BlackWinningRow({i},{j})"))
        redRow[i].append(Var(f"RedWinningRow({i},{j})"))

def BlackRowWin():
  f = ~true
  for i in range(rowNum): 
      for j in range(columnNum - 3):
        f |= blackRow[i][j]
  return f

def RedRowWin():
  f = ~true
  for i in range(rowNum): 
      for j in range(columnNum - 3):
        f |= redRow[i][j]
  return f 



#Creating red and black diagonal wins boards
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

def leftBlackDiagonalWin():
  f = ~true
  for i in range(rowNum- 3): 
      for j in range(columnNum - 3):
        f |= leftBlackDiagonal[i][j]
  return f

def rightBlackDiagonalWin():
  f = ~true
  for i in range(rowNum- 3): 
      for j in range(columnNum - 3):
        f |= rightBlackDiagonal[i][j]
  return f

def leftRedDiagonalWin():
  f = ~true
  for i in range(rowNum- 3): 
      for j in range(columnNum - 3):
        f |= leftRedDiagonal[i][j]
  return f 

def rightRedDiagonalWin():
  f = ~true
  for i in range(rowNum- 3): 
      for j in range(columnNum - 3):
        f |= rightRedDiagonal[i][j]
  return f 

#Creating red and black column wins boards
blackColumn=[]
redColumn=[]
for i in range(rowNum- 3): 
    blackColumn.append([])
    redColumn.append([])
    for j in range(columnNum):
        blackColumn[i].append(Var(f"BlackWinningColumn({i},{j})"))
        redColumn[i].append(Var(f"RedWinningColumn({i},{j})"))

def BlackColumnWin():
  f = ~true
  for i in range(rowNum- 3): 
      for j in range(columnNum):
        f |= blackColumn[i][j]
  return f 

def RedColumnWin():
  f = ~true
  for i in range(rowNum- 3): 
      for j in range(columnNum):
        f |= redColumn[i][j]
  return f 


# Prints a Connect Four board using .solve dictionary
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
        print("Black has Won the Game!")
      elif (key == "Red has Won the Game") and (value == True):
        print("Red has Won the Game!")
      elif (key == "No one has Won the Game") and (value == True):
        print("No one has Won the Game!")
  for row in board:
    print(row)
        
def rowWin(E):
  for i in range(rowNum):
    for j in range(columnNum - 3):
      #Winning row and its position of either 4 red or 4 black slots within the row. 
      E.add_constraint(iff(blackRow[i][j], (blackBoard[i][j] & blackBoard[i][j + 1] & blackBoard[i][j + 2] & blackBoard[i][j + 3]))) 

      E.add_constraint(iff(redRow[i][j], (redBoard[i][j] & redBoard[i][j + 1] & redBoard[i][j + 2] & redBoard[i][j + 3])))

      #Checks that there is at least one possible route to play in order to win by a row
      if (i > 0):
        E.add_constraint(blackRow[i][j] >> (emptyBoard[i-1][j] | emptyBoard[i-1][j + 1] | emptyBoard[i-1][j + 2] | emptyBoard[i-1][j + 3]))

        E.add_constraint(redRow[i][j] >> (emptyBoard[i-1][j] | emptyBoard[i-1][j + 1] | emptyBoard[i-1][j + 2] | emptyBoard[i-1][j + 3]))


      #Checks that only one column can win
      special1 = blackRow[i][j]
      special2 = redRow[i][j]
      false1 = ~true
      false2 = ~true
      for i2 in range(rowNum):
        for j2 in range(columnNum - 3):
          if (i != i2):
            false1 |= blackRow[i2][j2]
            false2 |= redRow[i2][j2]
      E.add_constraint(special1 >> ~false1)
      E.add_constraint(special2 >> ~false2)
  return E
        

def columnWin(E):
  for i in range(rowNum - 3):
    for j in range(columnNum):
      #Winning column and its position of either 4 red or 4 black slots within the column. 
      E.add_constraint(iff(blackColumn[i][j], (blackBoard[i][j] & blackBoard[i+1][j] & blackBoard[i+2][j] & blackBoard[i+3][j])))

      E.add_constraint(iff(redColumn[i][j], (redBoard[i][j] & redBoard[i+1][j] & redBoard[i+2][j] & redBoard[i+3][j])))

      #Checks that there is a possible route to play in order to win by a column
      if (i > 0):
        E.add_constraint(blackColumn[i][j] >> (emptyBoard[i-1][j]))
        E.add_constraint(redColumn[i][j] >> (emptyBoard[i-1][j]))
      
      #Checks that only one column can win
      special1 = blackColumn[i][j]
      special2 = redColumn[i][j]
      false1 = ~true
      false2 = ~true
      for i2 in range(rowNum - 3):
        for j2 in range(columnNum):
          if (i != i2) | (j != j2):
            false1 |= blackColumn[i2][j2]
            false2 |= redColumn[i2][j2]
      E.add_constraint(special1 >> ~false1)
      E.add_constraint(special2 >> ~false2)
  return E


def leftDiagonalWin(E):
  for i in range(rowNum - 3):
    for j in range(columnNum - 3):
      #Winning diagonal going right and down.
      E.add_constraint(iff(leftBlackDiagonal[i][j], (blackBoard[i][j] & blackBoard[i+1][j+1] & blackBoard[i+2][j+2] & blackBoard[i+3][j+3])))

      E.add_constraint(iff(leftRedDiagonal[i][j], (redBoard[i][j] & redBoard[i+1][j+1] & redBoard[i+2][j+2] & redBoard[i+3][j+3])))

      if (i > 0):
        E.add_constraint(leftBlackDiagonal[i][j] >> (emptyBoard[i-1][j] | emptyBoard[i][j+1] | emptyBoard[i+1][j+2] | emptyBoard[i+2][j+3]))   
        E.add_constraint(leftRedDiagonal[i][j] >> (emptyBoard[i-1][j] | emptyBoard[i][j+1] | emptyBoard[i+1][j+2] | emptyBoard[i+2][j+3]))
      
      #Only one left facing diagonal can be a winning diagonal 
      special1 = leftBlackDiagonal[i][j]
      special2 = leftRedDiagonal[i][j]
      false1 = ~true
      false2 = ~true
      for i2 in range(rowNum - 3):
        for j2 in range(columnNum - 3):
          if (i != i2) | (j != j2):
            if (i + 1 != i2) | (j + 1 != j2):
              if (i + 2 != i2) | (j + 2 != j2):
                 if (i - 1 != i2) | (j - 1 != j2):
                   if (i - 2 != i2) | (j - 2 != j2):
                      false1 |= leftBlackDiagonal[i2][j2]
                      false2 |= leftRedDiagonal[i2][j2]
      E.add_constraint(special1 >> ~false1)
      E.add_constraint(special2 >> ~false2)
  return E


def rightDiagonalWin(E):
  for i in range(rowNum - 3):
    for j in range(columnNum - 4, columnNum):
      #Winning diagonal going left and down.
      E.add_constraint(iff(rightBlackDiagonal[i][j-3], (blackBoard[i][j] & blackBoard[i+1][j-1] & blackBoard[i+2][j-2] & blackBoard[i+3][j-3])))
      
      E.add_constraint(iff(rightRedDiagonal[i][j-3], (redBoard[i][j] & redBoard[i+1][j-1] & redBoard[i+2][j-2] & redBoard[i+3][j-3])))

      if (i > 0):
        E.add_constraint(rightBlackDiagonal[i][j-3] >> (emptyBoard[i-1][j] | emptyBoard[i][j-1] | emptyBoard[i+1][j - 2] | emptyBoard[i+2][j - 3]))
        E.add_constraint(rightRedDiagonal[i][j-3] >> (emptyBoard[i-1][j] | emptyBoard[i][j-1] | emptyBoard[i+1][j - 2] | emptyBoard[i+2][j - 3]))

      #Only one right facing diagonal can be a winning diagonal 
      special1 = rightBlackDiagonal[i][j-3]
      special2 = rightRedDiagonal[i][j-3]
      false1 = ~true
      false2 = ~true
      for i2 in range(rowNum - 3):
        for j2 in range(columnNum - 4, columnNum):
          if (i != i2) | (j != j2):
            if (i - 1 != i2) | (j + 1 != j2):
              if (i - 2 != i2) | (j + 2 != j2):
                 if (i + 1 != i2) | (j - 1 != j2):
                   if (i + 2 != i2) | (j - 2 != j2):
                    false1 |= rightBlackDiagonal[i2][j2-3]
                    false2 |= rightRedDiagonal[i2][j2-3]
      E.add_constraint(special1 >> ~false1)
      E.add_constraint(special2 >> ~false2)
  return E

# Addd constriants to check if all occupied position below current is occupied position
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

      # If position(i, j) is red, then neither black or empty can occupy position(i, j)
      E.add_constraint(redBoard[i][j] >> (~blackBoard[i][j] & ~emptyBoard[i][j] & gravityRule(i, j)))

      # If position(i, j) is black, then neither red or empty can occupy position(i, j)
      E.add_constraint(blackBoard[i][j] >> (~redBoard[i][j] & ~emptyBoard[i][j] & gravityRule(i, j)))

      # Could add constraint so that one side must win!

      # make sure implication works properly above, exactly one has to be true.
      E.add_constraint(emptyBoard[i][j] | redBoard[i][j] | blackBoard[i][j])

  E.add_constraint(iff(BlackWin, (BlackColumnWin() | BlackRowWin() | leftBlackDiagonalWin() | rightBlackDiagonalWin())))

  E.add_constraint(iff(RedWin, (RedColumnWin() | RedRowWin() | leftRedDiagonalWin() | rightRedDiagonalWin())))

  # E.add_constraint(iff(NoWin, ((~BlackColumnWin() | ~BlackRowWin() | ~leftBlackDiagonalWin() | ~rightBlackDiagonalWin()) & (~RedColumnWin() | ~RedRowWin() | ~leftRedDiagonalWin() | ~rightRedDiagonalWin()))))
  

  #All posibilities of Connect Four
  E.add_constraint(iff(BlackWin, (~RedWin & ~NoWin)))
  E.add_constraint(iff(RedWin, (~BlackWin & ~NoWin)))
  E.add_constraint(iff(NoWin, (~RedWin & ~BlackWin)))


    
  return E

def columnRules(E):
  for i in range(rowNum - 3):
    for j in range(columnNum):
      special = blackColumn[i][j]
      false = ~true
      for i2 in range(rowNum):
        for j2 in range(columnNum):
          if (j2 < columnNum - 3):
            if ((i != i2) | ((j - j2) >= 4)):
              false |= blackRow[i2][j2]  
          if (j2 < (columnNum - 3)):
            if (i2 < rowNum - 3):
              if (((i != i2) | (j != j2)) & ((i-1 != i2) | (j-1 != j2)) & ((i-2 != i2) | (j-2 != j2)) & ((i-3 != i2) | (j-3 != j2))):
                false |= leftBlackDiagonal[i2][j2] 

              if (((i != i2) | (j != j2 + 3)) & ((i-1 != i2) | (j+1 != j2 + 3)) & ((i-2 != i2) | (j+2 != j2 + 3)) & ((i-3 != i2) | (j+3 != j2 + 3))):
                false |= rightBlackDiagonal[i2][j2] 
      E.add_constraint(special >> ~false)
  return E


# Build an example full theory for your setting and return it.
def connectFour():
  E = Encoding()
  E = validBoard(E)
  E = rowWin(E)
  E = columnWin(E)
  E = leftDiagonalWin(E)
  E = rightDiagonalWin(E)
  E = columnRules(E)
  # E.add_constraint(BlackWin)
  #E.add_constraint(RedWin)
    #add winning function with constraints like validBoard to see if board is a won state.

    #E.add_constraint(emptyBoard[0][0])
    #E.add_constraint(~emptyBoard[0][0])

  #Checks if functions work/dont condradict each other
  #E.add_constraint(blackBoard[0][0] & blackBoard[1][1] & blackBoard[2][2] & blackBoard[3][3] & blackBoard[4][4] & blackBoard[5][5])
  # E.add_constraint(blackColumn[1][2] & blackRow[1][0])
  # for i in range(6):
  #   for j in range(4):
  #     E.add_constraint(~blackRow[i][j])
  # E.add_constraint(blackColumn[1][2] & rightBlackDiagonal[0][0])
  return E


if __name__ == "__main__":

    E = connectFour()

    print("\nSatisfiable: %s" % E.is_satisfiable())
    #print("# Solutions: %d" % E.count_solutions())
    dic = E.solve()
    print("   Solution: %s" % dic)

    #Tostring function basically that takes dictionary output of E.solve and prints a connect four board
    printBoard(dic)

    


    # print("\nVariable likelihoods:")
    # print(" %s: %.2f" % (BlackWin, E.likelihood(BlackWin)))
    # print()
