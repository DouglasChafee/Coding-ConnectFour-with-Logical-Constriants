
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

# #variables to be turned into constraints
# C = Var('A winning column')
# L = Var("Black's turn")
# J = Var("Red's turn")
# Z = Var("This value is true when x is zero")
# W = Var("A winning game")
# U = Var("An occupied slot")
# P = Var("if either black or red has the option to win in one turn")
# D = Var("A winning diagonal")

# Creating ConnectFour Game Board
rowNum = 6
columnNum = 7

# Creating boards for all possibilities starting bottom left (5,0) of that a single position could be, black, red, or empty
blackBoard=[]
redBoard=[]
emptyBoard=[]
winRow=[]
winColumn=[]
winDiagonal=[]
for i in range(rowNum): 
    blackBoard.append([])
    redBoard.append([])
    emptyBoard.append([])
    winRow.append([])
    for j in range(columnNum):
        blackBoard[i].append(Var(f"Black({i},{j})"))
        redBoard[i].append(Var(f"Red({i},{j})"))
        emptyBoard[i].append(Var(f"Empty({i},{j})"))
        if (j < columnNum - 3):
          winRow[i].append(Var(f"WinningRow({i},{j})"))
# # Printing example of Black connect four Game Board
# for row in winRow:
#   print(row)

for i in range(rowNum- 3): 
    winDiagonal.append([])
    for j in range(columnNum - 3):
        winDiagonal[i].append(Var(f"WinningDiagonal({i},{j})"))

for i in range(rowNum- 3): 
    winColumn.append([])
    for j in range(columnNum):
        winColumn[i].append(Var(f"WinningColumn({i},{j})"))

for row in winColumn:
  print(row)

# Prints a Connect Four board
def printBoard(dic):
  board=[]
  for i in range(rowNum): 
    board.append([])
    for j in range(columnNum):
      board[i].append("N")
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
  for row in board:
    print(row)
        
def rowWin(E):
  for i in range(rowNum):
    for j in range(columnNum - 3):
      #Winning row and its position of the 4 slots within the row. 
      E.add_constraint(iff(winRow[i][j], (blackBoard[i][j] & blackBoard[i][j + 1] & blackBoard[i][j + 2] & blackBoard[i][j + 3])))

      # E.add_constraint(iff(winRow[i][j], (redBoard[i][j] & redBoard[i][j + 1] & redBoard[i][j + 2] & redBoard[i][j + 3])))

      #Checks that there is at least one possible route to play in order to win by a row
      if (i > 0):
        E.add_constraint(winRow[i][j] >> (emptyBoard[i-1][j] | emptyBoard[i-1][j + 1] | emptyBoard[i-1][j + 2] | emptyBoard[i-1][j + 3]))
        
        
  #blackBoard.clear()
  #redBoard.clear()

  #for i in range(len(blackBoard)):
 #   blackBoard.append([])
 #   for j in range(len(blackBoard[i])):
 #     blackBoard[i][j] = "N"
   
 # for i in range(len(redBoard)):
 #   redBoard.append([])
 #   for j in range(len(redBoard[i])):
 #     redBoard[i][j] = "N" 
      
  return E

def columnWin(E):
  for i in range(rowNum - 3):
    for j in range(columnNum):
      #Winning row and its position of the 4 slots within the row. 
      E.add_constraint(iff(winColumn[i][j], (blackBoard[i][j] & blackBoard[i+1][j] & blackBoard[i+2][j] & blackBoard[i+3][j])))

      # E.add_constraint(iff(winRow[i][j], (redBoard[i][j] & redBoard[i][j + 1] & redBoard[i][j + 2] & redBoard[i][j + 3])))

      #Checks that there is at least one possible route to play in order to win by a row
      if (i > 0):
        E.add_constraint(winColumn[i][j] >> (emptyBoard[i-1][j]))
      special = winColumn[i][j]
      f = true.negate()
      for i2 in range(rowNum - 3):
        for j2 in range(columnNum):
          if (i != i2) | (j != j2):
            print(i, i2, j, j2)
            f |= winColumn[i][j]
      E.add_constraint(special >> ~f)
  return E
def diagonalWin(E):
  for i in range(rowNum - 3):
    for j in range(columnNum):
      #Winning row and its position of the 4 slots within the row.
      if ((i == 5) & (j < 4)): 
        E.add_constraint(iff(winDiagonal[i][j], (blackBoard[i][j] & blackBoard[i+1][j+1] & blackBoard[i+2][j+2] & blackBoard[i+3][j+3])))
      elif ((1 < i < 4) & (1 < j < 5)):
        E.add_constraint(iff(winDiagonal[i][j], (blackBoard[i-1][j-1] & blackBoard[i][j] & blackBoard[i+1][j+1] & blackBoard[i+2][j+2])))
      elif ((0 < i < 3) & (2 < j < 6)):
        E.add_constraint(iff(winDiagonal[i][j], (blackBoard[i-2][j-2] & blackBoard[i-1][j-1] & blackBoard[i][j] & blackBoard[i+1][j+1])))
      elif ((i == 0) & (j > 2)):
        E.add_constraint(iff(winDiagonal[i][j], (blackBoard[i-3][j-3] & blackBoard[i-2][j-2] & blackBoard[i-1][j-1] & blackBoard[i][j])))
# ------------------------------------------------------------------------------------------------------------------------------------------------
      elif ((i == 5) & (j < 4)): 
        E.add_constraint(iff(winDiagonal[i][j], (blackBoard[i][j] & blackBoard[i-1][j+1] & blackBoard[i-2][j+2] & blackBoard[i-3][j+3])))
      elif ((1 < i < 4) & (1 < j < 5)):
        E.add_constraint(iff(winDiagonal[i][j], (blackBoard[i+1][j-1] & blackBoard[i][j] & blackBoard[i-1][j+1] & blackBoard[i-2][j+2])))
      elif ((0 < i < 3) & (2 < j < 6)):
        E.add_constraint(iff(winDiagonal[i][j], (blackBoard[i+2][j-2] & blackBoard[i+1][j-1] & blackBoard[i][j] & blackBoard[i-1][j+1])))
      elif ((i == 0) & (j > 2)):
        E.add_constraint(iff(winDiagonal[i][j], (blackBoard[i+3][j-3] & blackBoard[i+2][j-2] & blackBoard[i+1][j-1] & blackBoard[i][j])))
      # E.add_constraint(iff(winRow[i][j], (redBoard[i][j] & redBoard[i][j + 1] & redBoard[i][j + 2] & redBoard[i][j + 3])))

      #Checks that there is at least one possible route to play in order to win by a row
      if (i > 0):
        E.add_constraint(winColumn[i][j] >> (emptyBoard[i-1][j]))
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
      E.add_constraint(blackBoard[i][j] >> (~redBoard[i][j] & ~emptyBoard[i][j] & gravityRule(i, j)))

      # there must be non # empy positions below position(i,j) (gravity).
      #E.add_constraint(~emptyBoard[i][j] >> gravityRule(i, j))

      # make sure implication works properly above, exactly one has to be true.
      E.add_constraint(emptyBoard[i][j] | redBoard[i][j] | blackBoard[i][j])
    
  return E

#if [i][j] = black
#for x < 4
# if [i-x][j] = black
#   x += 1
#   if x = 3
#     black wins
# elif [i][j-x] = black
#   x += 1
#   if x = 3
#     black wins
# elif [i-x][j=x] = black
#   x += 1
#   if x = 3
#     black wins
# else
#   continue
#elif [i][j] = red
#for x < 4
# if [i-x][j] = red
#   x += 1
#   if x = 3
#     red wins
# elif [i][j-x] = red
#   x += 1
#   if x = 3
#     red wins
# elif [i-x][j=x] = red
#   x += 1
#   if x = 3
#     red wins
#else 
# # continue

#def blackWins(E):
  #for(int i=0;i<10;i++):
    #connectFour()
      
  

# def redWins(E):
  
  # return true
#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.

def connectFour():
  E = Encoding()
  E = validBoard(E)
  E = rowWin(E)
  E = columnWin(E)
    #add winning function with constraints like validBoard to see if board is a won state.

    #E.add_constraint(emptyBoard[0][0])
    #E.add_constraint(~emptyBoard[0][0])

  E.add_constraint(winColumn[0][0])
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
    # for v,vn in zip([P,W,H,C,D], 'PWHCD'):
    #     print(" %s: %.2f" % (v, T.likelihood(vn)))
    # print()
