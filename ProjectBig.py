
from search import *

if __name__ == "__main__":
    n = int(input("Enter Queen number: "))              #i.e. 5
    ngen = 100
    pmut = .3


    myNQueen = NQueensProblem(n)


    print("Beginning!")
    genetic_search(myNQueen, ngen, pmut, n)
    print("Done!")