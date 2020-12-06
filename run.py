
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

#variables to be turned into constraints
C = Var('A winning column')
L = Var("Black's turn")
J = Var("Red's turn")
H = Var("A winning row")
Z = Var("This value is true when x is zero")
W = Var("A winning game")
U = Var("An occupied slot")
P = Var("if either black or red has the option to win in one turn")
D = Var("A winning diagonal")

# Creating ConnectFour Game Board
rowNum = 6
columnNum = 7

# Creating boards for all possibilities of that a single position could be, black, red, or empty
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
# Printing example of Black connect four Game Board
for row in blackBoard:
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
        


def gravityRule(i, j):
  f = true
  for slot in range(i + 1, rowNum):
    f &= ~emptyBoard[slot][j]
  return f
  # return ~emptyboard
  



# Holds constraints/rules that make up a valid connect four board.
def validBoard(E):
  for i in range(rowNum):
    for j in range(columnNum): 
      # If position(i, j) is empty, then neither black or red can occupy position(i, j).
      E.add_constraint(emptyBoard[i][j] >> (~redBoard[i][j] & ~blackBoard[i][j]))

      # If position(i, j) is red, then neither black or empty can occupy position(i, j) and 
      # there must be non # empy positions below position(i,j) (gravity).
      E.add_constraint(redBoard[i][j] >> (~blackBoard[i][j] & ~emptyBoard[i][j] & gravityRule(i, j)))
      E.add_constraint(blackBoard[i][j] >> (~redBoard[i][j] & ~emptyBoard[i][j] & gravityRule(i, j)))

      # make sure implication works properly above, at least one has to be true.
      E.add_constraint(emptyBoard[i][j] | redBoard[i][j] | blackBoard[i][j])
  return E



#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.

def connectFour():
    E = Encoding()
    E = validBoard(E)
    #add winning function with constraints like validBoard to see if board is a won state.

    #E.add_constraint(emptyBoard[0][0])
    #E.add_constraint(~emptyBoard[0][0])


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
