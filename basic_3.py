import sys
import time
import psutil
GAP_PENALTY = 30

mismatch = {"A": {"A": 0, "C": 110, "G": 48, "T": 94},
            "C": {"A": 110, "C": 0, "G": 118, "T": 48},
            "G": {"A": 48, "C": 118, "G": 0, "T": 110},
            "T": {"A": 94, "C": 48, "G": 110, "T": 0}
            }


# parameters: X = 1st string, Y = 2nd string
# bottom-up pass
def basic_algorithm(X:str, Y:str, m, n) -> list[list[int]]:
    OPT = [[0 for i in range(n)] for j in range(m)]

    # initialize column 0 and row 0
    for i in range(m):
        OPT[i][0] = i*GAP_PENALTY
    for i in range(n):
        OPT[0][i] = i*GAP_PENALTY

    for i in range(1, m):
        for j in range(1, n):
            OPT[i][j] = min(OPT[i-1][j-1] + mismatch[X[i-1]][Y[j-1]], OPT[i-1][j] + GAP_PENALTY, OPT[i][j-1] + GAP_PENALTY)
    print(OPT[m-1][n-1])
    return OPT


# top-down pass
def find_alignment(X:str, Y:str):
    m = len(X)
    n = len(Y)

    x_final = X
    y_final = Y

    OPT = [[0 for i in range(m+1)] for i in range(n+1)]
    OPT = basic_algorithm(X, Y, m+1, n+1)

    alignment = ""

    i = m
    j = n
    print(f"opt cost is {OPT[m][n]}")
    while i > 0 or j > 0:
        if i > 0 and j > 0 and OPT[i][j] == OPT[i-1][j-1] + mismatch[X[i-1]][Y[j-1]]: # matched condition, keep X[i] and Y[j]
            i-=1
            j-=1
        elif j > 0 and OPT[i][j] == OPT[i][j-1] + GAP_PENALTY:  # gap condition, keep Y[j] gap X[i]
            x_final = x_final[:i] + "_" + x_final[i:]
            j-=1
        elif i > 0 and OPT[i][j] == OPT[i-1][j] + GAP_PENALTY: # gap condition, keep X[i] gap Y[j]
            y_final = y_final[:j] + "_" + y_final[j:]
            i-=1
        else:
            print("NOT SUPPOSED TO BE HERE")

    return OPT[m][n], x_final, y_final


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
    X = 'AAAAAAATTTTTTAAAAGGGGAAAAAAAAAAAAAAAAAATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGTCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGAA'
    Y = 'AAAAAAATTTTTTGGGGAAAAAAAAAAAAAAAAAAAAAATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGA'

    run_full_algorithm_get_efficiency(X, Y)

if __name__ == "__main__":
    main()