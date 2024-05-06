import sys
import time
import psutil

GAP_PENALTY =30

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
        return len(Y) * GAP_PENALTY, len(Y)*"_", Y
    if len(Y) == 0:
        return len(X) * GAP_PENALTY, X, len(X)*"_"
    if X == Y:
        return 0, X, Y
    if len(X) == 1 or len(Y) == 1:
        OPT = find_optimal_matrix(Y,X)
        i = len(X)
        j = len(Y)

        x_final = X
        y_final = Y
        # print(f"base case x: {X} y: {Y} opt: {OPT}")
        # print(f"{i} {j} {X[i-1]} {Y[j-1]}")
        while i > 0 or j > 0:
            if i > 0 and j > 0 and OPT[i][j] == OPT[i-1][j-1] + A[X[i-1]][Y[j-1]]: # matched condition, keep X[i] and Y[j]
                i-=1
                j-=1
            elif j > 0 and OPT[i][j] == OPT[i][j-1] + GAP_PENALTY:  # gap condition, keep Y[j] gap X[i]
                x_final = x_final[:i] + "_" + x_final[i:]
                j-=1
            elif i > 0 and OPT[i][j] == OPT[i-1][j] + GAP_PENALTY: # gap condition, keep X[i] gap Y[j]
                y_final = y_final[:j] + "_" + y_final[j:]
                i-=1

        return OPT[len(X)][len(Y)], x_final, y_final
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
        cur_val = optl[i][-1] + optr[len(Y) - i][-1]
        if cur_val < min_cost:
            min_cost = cur_val
            min_index = i
    Yl = Y[:min_index]
    Yr = Y[min_index:]  
    

    # print(optl)
    # print(optr)
    # print(f"x: {X} y: {Y} index: {min_index} xl: {Xl} xr: {Xr} yl: {Yl} yr: {Yr}")
    
    lcost, xl_align, yl_align = recurse(Xl, Yl)
    rcost, xr_align, yr_align = right_sequence = recurse(Xr, Yr)
    
    #print(f"total cost: {lcost + rcost} xalgin: {xl_align + xr_align} ralign: {yl_align + yr_align}")
    return lcost + rcost, xl_align + xr_align, yl_align + yr_align



    #generate the optimal 
def find_optimal_matrix(Xl:str, Y:str) -> list[list[int]]:
    optl = [[0 for i in range(len(Xl)+1)] for j in range(len(Y)+1)]
    #basecases
    for i in range(len(Y)+1):
        optl[i][0] = i*GAP_PENALTY
    for i in range(len(Xl)+1):
        optl[0][i] = i*GAP_PENALTY

    for i in range(1, len(Y)+1):
        for j in range(1, len(Xl)+1):
            #print(f"{i} {j} {Xl[j-1]} {Y[i-1]} {A[Y[i-1]][Xl[j-1]]}")
            optl[i][j] = min(optl[i-1][j-1] + A[Y[i-1]][Xl[j-1]],
                            optl[i][j-1] + GAP_PENALTY,
                            optl[i-1][j] + GAP_PENALTY)

    return optl

def process_memory():
    process = psutil.Process() 
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024) 
    return memory_consumed

def time_wrapper(X,Y): 
    start_time = time.time() 
    find_alignment(X,Y)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000 
    return time_taken

def run_full_algorithm_get_efficiency(X, Y):
    cost, x_ret, y_ret = find_alignment(X, Y)
    mem_used = process_memory()
    time = time_wrapper(X,Y)
    print(cost)
    print(x_ret)
    print(y_ret)
    print(mem_used)
    print(time)


def main():
    X = "GATAAAAAAACCCCCCCCCC"
    Y = "TAGAAAAAAACCCCCCCCCC"
    X = "ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG"
    Y = "TATTATTATACGCTATTATACGCGACGCGGACGCGTATACGCTATTATACGCGACGCGGACGCG"
    #1
    X = "ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG"
    Y = "TATTATTATACGCTATTATACGCGACGCGGACGCGTATACGCTATTATACGCGACGCGGACGCG"
    #2
    X = "ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG"
    Y = "TTATTATACGCGACGCGATTATACGCGACGCG"
    #3
    X = 'AAAAAAGTCGTCAGTCGTCAAGTCGTCAGTCGTCAAAGTCGTCAGTCGTCAAGTCGTCAGTCGTCAAAAGTCGTCAGTCGTCAAGTCGTCAGTCGTCAAAGTCGTCAGTCGTCAAGTCGTCAGTCGTC'
    Y = 'TATATATATATACGCGTACGCGTATACGCGTACGCGTATATACGCGTACGCGTATACGCGTACGCGTATATATACGCGTACGCGTATACGCGTACGCGTATATACGCGTACGCGTATACGCGTACGCG'
    #4
    X = 'AAAAAAATTTTTTAAAAGGGGAAAAAAAAAAAAAAAAAATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGTCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGAA'
    Y = 'AAAAAAATTTTTTGGGGAAAAAAAAAAAAAAAAAAAAAATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGA'
    run_full_algorithm_get_efficiency(X,Y)


    

    
if __name__ == "__main__":
    main()

