

GAP_PENALTY = 30

A = {"A" : {"A":0, "C":110, "G":48, "T":94},
     "C" : {"A":110, "C":0, "G":118, "T":48},
     "G" : {"A":48, "C":118, "G":0, "T":110},
     "T" : {"A":94, "C":48, "G":110, "T":0}
     }


def find_alignment(X:str, Y:str) -> tuple[int, str, str, float, float]:
    #take in string and call recursive hepler function
    alignment = recurse(X,Y)
    return alignment
#find 
def recurse(X:str, Y:str) -> str:
    if len(X) == 0:
        return Y
    if len(Y) == 0:
        return X
    if X == Y:
        return X
    if len(X) == 1 and len(Y) == 1:
        return X+Y
    #split x in half and from left and right
    Xl = X[0:len(X)//2]
    Xr = X[len(X)//2:]
    #process x1 first
    #create opt matrix
    optl = find_optimal_matrix(Xl, Y)
    optr = find_optimal_matrix(Xr[::-1], Y[::-1])
    min_index = -1
    min_cost = 9999999999999999999
    for i in range(len(optl)):
        cur_val = optl[i][-1] + optr[i][-1]
        if cur_val < min_cost:
            min_cost = cur_val
            min_index = i
    Yl = Y[:min_index]
    Yr = Y[min_index:]  
    print(f"x: {X} y: {Y} index: {min_index} xl: {Xl} xr: {Xr} yl: {Yl} yr: {Yr}")
    print(optl)
    print(optr)
    left_sequence = recurse(Xl, Yl)
    right_sequence = recurse(Xr, Yr)
    
    print(f"{left_sequence} {right_sequence}")
    return left_sequence + right_sequence




    #generate the optimal 
def find_optimal_matrix(Xl:str, Y:str) -> list[list[int]]:
    optl = [[0 for i in range(len(Xl)+1)] for i in range(len(Y)+1)]
    #basecases
    for i in range(len(Y)+1):
        optl[i][0] = 0
    for i in range(len(Xl)+1):
        optl[0][i] = i*GAP_PENALTY

    for i in range(1, len(Y)+1):
        for j in range(1, len(Xl)+1):
            print(f"{i} {j} {Xl[j-1]} {Y[i-1]} {A[Y[i-1]][Xl[j-1]]}")
            optl[i][j] = min(optl[i-1][j-1] + A[Y[i-1]][Xl[j-1]],
                            optl[i][j-1] + GAP_PENALTY,
                            optl[i-1][j] + GAP_PENALTY)

    return optl

def main():
    print(find_alignment("ACACTGACTACTGACTGGTGACTACTGACTGG", "TATTATACGCTATTATACGCGACGCGGACGCG"))
    
if __name__ == "__main__":
    main()