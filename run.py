

from nnf import Var
from lib204 import Encoding

C = Var('A winning column')
L = Var("Black's turn")
J = Var("Red's turn")
R = Var("Red unit")
B = Var('Black unit')
H = Var("A winning row")
Z = Var("This value is true when x is zero")
W = Var("A winning game")
U = Var("An occupied slot")
P = Var("if either black or red has the option to win in one turn")
D = Var("A winning diagonal")



#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.

def connectFour_validWin():
    T = Encoding()
    T.add_constraint(~L | ~J)
    T.add_constraint(~B | ~R)
    T.add_constraint(B | R | Z)
    T.add_constraint(B | R | (~B & ~R))
    T.add_constraint(~H | ((B&B&B&B)|(R&R&R&R)))
    T.add_constraint(~C | ((B&B&B&B)|(R&R&R&R)))
    T.add_constraint(~P | (~U&B&B&B)|(B&~U&B&B)(B&B&~U&B)|B&B&B&~U)|(~U&R&R&R)|(R&~U&R&R)(R&R&~U&R)|R&R&R&~U))
    T.add_constraint(~W | (H | C | D))
    return T

def connectFour_blackWin():
    T = Encoding()
    T.add_constraint(~L | ~J)
    T.add_constraint(~B | ~R)
    T.add_constraint(B | R | Z)
    T.add_constraint(B | R | (~B & ~R))
    T.add_constraint(~H | ((B&B&B&B)|(R&R&R&R)))
    T.add_constraint(~C | ((B&B&B&B)|(R&R&R&R)))
    T.add_constraint(~P | (~U&B&B&B)|(B&~U&B&B)(B&B&~U&B)|B&B&B&~U)|(~U&R&R&R)|(R&~U&R&R)(R&R&~U&R)|R&R&R&~U))
    T.add_constraint(~W)
    T.add_constraint(B&B&B)
    return T

def connectFour_redWin():
    T = Encoding()
    T.add_constraint(~L | ~J)
    T.add_constraint(~B | ~R)
    T.add_constraint(B | R | Z)
    T.add_constraint(B | R | (~B & ~R))
    T.add_constraint(~H | ((B&B&B&B)|(R&R&R&R)))
    T.add_constraint(~C | ((B&B&B&B)|(R&R&R&R)))
    T.add_constraint(~P | (~U&B&B&B)|(B&~U&B&B)(B&B&~U&B)|B&B&B&~U)|(~U&R&R&R)|(R&~U&R&R)(R&R&~U&R)|R&R&R&~U))
    T.add_constraint(~W)
    T.add_constraint(R&R&R)
    return T



if __name__ == "__main__":

    T = connectFour_validWin()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([P,W,H,C,D], 'PWHCD'):
        print(" %s: %.2f" % (v, T.likelihood(vn)))
    print()
