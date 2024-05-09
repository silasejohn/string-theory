import sys
import time
import psutil
import os
import matplotlib.pyplot as plt
import tracemalloc

GAP_PENALTY = 30

mismatch = {"A": {"A": 0, "C": 110, "G": 48, "T": 94},
            "C": {"A": 110, "C": 0, "G": 118, "T": 48},
            "G": {"A": 48, "C": 118, "G": 0, "T": 110},
            "T": {"A": 94, "C": 48, "G": 110, "T": 0}
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
            OPT[i][j] = min(OPT[i-1][j-1] + mismatch[X[i-1]][Y[j-1]], OPT[i-1][j] + GAP_PENALTY, OPT[i][j-1] + GAP_PENALTY)
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
    start_time = time.time() 
    cost, x_ret, y_ret = find_alignment(X,Y)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000 
    memoryTaken = process_memory()

    return cost, x_ret, y_ret, time_taken, memoryTaken
    # print(cost)
    # print(x_ret)
    # print(y_ret)
    # print(time)
    # print(mem_used)

def main():
    cpu_time_array = []
    mem_usage_array = []
    problem_size_array = [] 
    
    ### SAMPLE TEST CASES ###
    # sample_dir_name = "sample_test_cases/"
    # sample_file_names = ["input1.txt", "input2.txt", "input3.txt", "input4.txt", "input5.txt"] # os.listdir(file_dir)
    # for idx in range(len(sample_file_names)): 
    #     word_1, word_2 = generate_input_string(sample_dir_name + sample_file_names[idx])
    #     print("First Word: ", word_1)
    #     print("Second Word: ", word_2)
    #     cost, x_ret, y_ret, time, mem_used = run_full_algorithm_get_efficiency(word_1, word_2)
    #     problem_size = len(x_ret) + len(y_ret)
    #     cpu_time_array.append(time)
    #     mem_usage_array.append(mem_used)
    #     problem_size_array.append(problem_size)
    #     print(f"Cost: {cost}")
    #     print(f"X: {x_ret}")
    #     print(f"Y: {y_ret}")
    #     print(f"Time: {time}")
    #     print(f"Memory: {mem_used}")

    ### DATAPOINT TEST CASES ###
    datapoints_dir_name = "datapoints/"
    sample_file_names = os.listdir(datapoints_dir_name)
    # only keep file names that start with "in"
    sample_file_names = [file_name for file_name in sample_file_names if file_name.startswith("in")]
    
    # if a file is in the format of "in#.txt" where # is a number, put that file in index (# - 1)
    sample_file_names = sorted(sample_file_names, key=lambda x: int(x[2:-4]))
    #print(sample_file_names)
    # iter_ctr = 13
    
# for i in range(len(sample_file_names)):
# for i in range(len(sample_file_names)):
    for i in range(len(sample_file_names)):
        word_1, word_2 = generate_input_string(datapoints_dir_name + sample_file_names[i])
        cost, x_ret, y_ret, time, mem_used = run_full_algorithm_get_efficiency(word_1, word_2)
        problem_size = len(x_ret) + len(y_ret)
        cpu_time_array.append(time)
        mem_usage_array.append(mem_used)
        problem_size_array.append(problem_size)
        print(f"file index {i}")
        print(f"{cost} {time} {mem_used}")

    # plot a graph for cpu_time vs problem_size using cpu_time_array and problem_size_array
    plt.scatter(problem_size_array, cpu_time_array)
    plt.xlabel("Problem Size")
    plt.ylabel("CPU Time (ms)")
    plt.title("[BASIC] CPU Time vs Problem Size")
    plt.show()

    # plot a graph for cpu_time vs problem_size using cpu_time_array and problem_size_array
    plt.scatter(problem_size_array, mem_usage_array)
    plt.xlabel("Problem Size")
    plt.ylabel("Memory (KB)")
    plt.title("[BASIC] Memory vs Problem Size")
    plt.show()
if __name__ == "__main__":
    main()