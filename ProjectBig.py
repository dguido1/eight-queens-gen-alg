
from search import *

if __name__ == "__main__":
    n = int(input("Enter Queen number: "))#i.e. 5
    ngen = 31
    pmut = 0.1
    #initialize problem
    myNQueen = NQueensProblem(n)
    print("Beginning!")
    genetic_search(myNQueen, ngen, pmut, n)
    print("Done!")