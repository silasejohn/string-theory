
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

    x_sol = "_A_CA_CACT__G__A_C_TAC_TGACTG_GTGA__C_TACTGACTGGACTGACTACTGACTGGTGACTACT_GACTG_G"
    y_sol = "TATTATTA_TACGCTATTATACGCGAC_GCG_GACGCGTA_T_AC__G_CT_ATTA_T_AC__GCGAC_GC_GGAC_GCG"
    print("First String:", x_final)
    print("Second String:", y_final)
    print(len(x_final) == len(x_sol))
    print(len(y_final) == len(y_sol))
    print(x_final == x_sol)
    print(y_final == y_sol)


def main():
    X = "ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG"
    Y = "TATTATTATACGCTATTATACGCGACGCGGACGCGTATACGCTATTATACGCGACGCGGACGCG"
    find_alignment(X, Y)

if __name__ == "__main__":
    main()