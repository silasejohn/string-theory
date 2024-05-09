import os
import sys
import time
import psutil
import matplotlib.pyplot as plt
import argparse

GAP_PENALTY =30

A = {"A" : {"A":0, "C":110, "G":48, "T":94},
     "C" : {"A":110, "C":0, "G":118, "T":48},
     "G" : {"A":48, "C":118, "G":0, "T":110},
     "T" : {"A":94, "C":48, "G":110, "T":0}
     }


def parse_input_file(file_name: str) -> tuple[str, str]:
    
    # store input word, list of indices, and file lines
    lines = ""
    input_word_1 = ""
    input_word_2 = ""
    index_list_1 = []
    index_list_2 = []

    found_second_word = False
    
    # check if file exists, read all lines
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # slice lines into 4 parts: first line with a word, next j lines with integers (not sure how many), next line with a word, final k lines with integers (not sure how many)
    input_word_1 = lines[0].strip()
    for i in range(1, len(lines)):
        if not found_second_word:
            if lines[i].strip().isdigit():
                index_list_1.append(int(lines[i].strip()))
            else:
                input_word_2 = lines[i].strip()
                found_second_word = True
        elif found_second_word:
            if lines[i].strip().isdigit():
                index_list_2.append(int(lines[i].strip()))
            else:
                print("Error: unexpected input")
                sys.exit(1)
    
    # return input word and list of indices
    return input_word_1, index_list_1, input_word_2, index_list_2

def process_input(input_word: str, list_of_indices: list[int], verbose: False) -> None:
    # modified_string starts as input_word 
    modified_string = input_word

    if verbose:
        print("First Base String: ", modified_string)

    # (insert) input_word into modified_string after index i 
    for i in list_of_indices:
        new_string = modified_string[:i+1] + modified_string + modified_string[i+1:] # i+1 is not inclusive on first slice
        if verbose:
            print("Insertion after index", str(i) + ":", new_string)
        modified_string = new_string

    # return modified_string
    return modified_string

def assert_input(generated_base_string, actual_base_string):
    print("Generated base string: ", generated_base_string)
    print("Actual base string: ", actual_base_string)
    assert generated_base_string == actual_base_string, "Generated base string does not match actual base string"

def test_all_datapoints(_file_dir: str):
    # check each datapoint test case
    file_dir = _file_dir
    file_names = os.listdir(file_dir)
    # number of files in directory
    print("Number of files: ", len(file_names))
    file_ctr = 0
    string_1_array = []
    string_2_array = []

    for file_name in file_names:
        file_ctr += 1
        print("Parsing file: ", file_ctr, " of ", len(file_names))
        print("File: ", file_dir + file_name)
        print("Running test case for file: ", file_name)
        output_string_1, output_string_2 = generate_input_string(file_dir + "/" + file_name)
        string_1_array.append(output_string_1)
        string_2_array.append(output_string_2)
        print ("\nOutput String 1: ", output_string_1)
        print ("\nOutput String 2: ", output_string_2)   
        print ("Completed test case for file " + str(file_ctr) + " of", len(file_names))
        print("\n")
    
    return string_1_array, string_2_array

def generate_input_string(file_name: str, actual_base_string_1: str = "", actual_base_string_2: str = "", verbose: bool = False):
    # parse input file
    input_word_1, index_list_1, input_word_2, index_list_2 = parse_input_file(file_name)

    if verbose:
        print("Input Word 1: ", input_word_1)
        print("List of Indices: ", index_list_1)
        print("Input Word 2: ", input_word_2)
        print("List of Indices: ", index_list_2)

    # process input
    output_string_1 = process_input(input_word_1, index_list_1, verbose)
    output_string_2 = process_input(input_word_2, index_list_2, verbose)

    if verbose:
        print ("Output String 1: ", output_string_1)
        print ("Output String 2: ", output_string_2)

    if actual_base_string_1 == "":
        return output_string_1, output_string_2

    # assert input
    assert_input(output_string_1, actual_base_string_1)
    assert_input(output_string_2, actual_base_string_2)

    return output_string_1, output_string_2



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
            OPT[i][j] = min(OPT[i-1][j-1] + A[X[i-1]][Y[j-1]], OPT[i-1][j] + GAP_PENALTY, OPT[i][j-1] + GAP_PENALTY)
    #print(OPT[m-1][n-1])
    return OPT

# top-down pass
def basic_find_alignment(X:str, Y:str):
    m = len(X)
    n = len(Y)

    x_final = X
    y_final = Y

    OPT = [[0 for i in range(m+1)] for i in range(n+1)]
    OPT = basic_algorithm(X, Y, m+1, n+1)

    alignment = ""

    i = m
    j = n
    #print(f"opt cost is {OPT[m][n]}")
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
        else:
            print("NOT SUPPOSED TO BE HERE")

    return OPT[m][n], x_final, y_final


def find_alignment(X:str, Y:str) -> tuple[int, str, str, float, float]:
    #take in string and call recursive hepler function
    alignment = recurse(X,Y)
    return alignment
#find 
def recurse(X:str, Y:str) -> str:
    if (len(X) <= 2 or len(Y) <= 2):
        _, x, y = basic_find_alignment(X,Y)
        return _, x, y

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
        cur_val = optl[i] + optr[len(Y) - i]
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
def find_optimal_matrix(Y:str, Xl:str) -> list[list[int]]:
    # get the length of the strings
    m = len(Xl) + 1 
    n = len(Y) + 1
    dp = []
    for i in range(2):
        temp = []
        for j in range(m):
            temp.append(0)
        dp.append(temp)
            
    
    # Fill the DP table
    for i in range(1, m):
        dp[0][i] = i * GAP_PENALTY
    for i in range(1, n):
        dp[1][0] = i * GAP_PENALTY
        for j in range(1, m):
            dp[1][j] = min(
                dp[1][j - 1] + GAP_PENALTY,
                dp[0][j - 1] + A[Xl[j - 1]][Y[i - 1]],
                dp[0][j] + GAP_PENALTY
            )
        for j in range(0, m):
            dp[0][j] = dp[1][j]
    
    
    return dp[-1]

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
    return cost, x_ret, y_ret, time, mem_used
    # print(cost)
    # print(x_ret)
    # print(y_ret)
    # print(mem_used)
    # print(time)


def main(input_file, output_file):
    
    word_1, word_2 = generate_input_string(str(input_file))
    cost, x_ret, y_ret, time, mem_used = run_full_algorithm_get_efficiency(word_1, word_2)
    
    # create output file per iteration run
    output_file = open(str(output_file), "w")
    output_file.write(f"{cost}\n")
    output_file.write(f"{x_ret}\n")
    output_file.write(f"{y_ret}\n")
    output_file.write(f"{time}\n")
    output_file.write(f"{mem_used}\n")
    output_file.close()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process input and output files")
    parser.add_argument("input_file", help="Path to the input file")
    parser.add_argument("output_file", help="Path to the output file")
    args = parser.parse_args()
    main(args.input_file, args.output_file)

