import os
import sys
import time
import psutil
import matplotlib.pyplot as plt
import basic_3 as basic 
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




def find_alignment(X:str, Y:str) -> tuple[int, str, str, float, float]:
    #take in string and call recursive hepler function
    alignment = recurse(X,Y)
    return alignment
#find 
def recurse(X:str, Y:str) -> str:
    if (len(X) <= 2 or len(Y) <= 2):
        _, x, y = basic.find_alignment(X,Y)
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
    XL_len = len(Xl)
    Y_len = len(Y)
    
    # empty DP table
    mem_dp = []
    
    # stucture of DP table
    for _ in range(2):
        mem_dp.append([0] * (XL_len + 1))
    
    # fill the first row
    for idx_1 in range(1, XL_len + 1):
        mem_dp[0][idx_1] = idx_1 * GAP_PENALTY
    
    # fill the rest of the table
    for idx_1 in range(1, Y_len + 1):
        mem_dp[1][0] = idx_1 * GAP_PENALTY

        # fill the rest of the row
        for idx_2 in range(1, XL_len + 1):
            # get the cost of a match
            cost_match = A[Xl[idx_2 - 1]][Y[idx_1 - 1]] 

            # fill the cell
            mem_dp[1][idx_2] = min(
                mem_dp[0][idx_2 - 1] + cost_match,
                mem_dp[0][idx_2] + GAP_PENALTY,
                mem_dp[1][idx_2 - 1] + GAP_PENALTY
            )

        # copy the second row to the first row
        for idx_2 in range(0, XL_len):
            mem_dp[0][idx_2] = mem_dp[1][idx_2]
    
    # return the DP table
    return mem_dp[-1]

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


def main():
    cpu_time_array = []
    mem_usage_array = []
    problem_size_array = [] 

    # ### SAMPLE TEST CASES ###
    # sample_dir_name = "sample_test_cases/"
    # sample_file_names = ["input1.txt", "input2.txt", "input3.txt", "input4.txt", "input5.txt"] # os.listdir(file_dir)
    # for idx in range(len(sample_file_names)): 
    #     word_1, word_2 = generate_input_string(sample_dir_name + sample_file_names[idx])
    #     # print("First Word: ", word_1)
    #     # print("Second Word: ", word_2)
    #     cost, x_ret, y_ret, time, mem_used = run_full_algorithm_get_efficiency(word_1, word_2)
    #     problem_size = len(x_ret) + len(y_ret)
    #     cpu_time_array.append(time)
    #     mem_usage_array.append(mem_used)
    #     problem_size_array.append(problem_size)
    #     print(f"\nCost: {cost}")
    #     # print(f"X: {x_ret}")
    #     # print(f"Y: {y_ret}")
    #     print(f"Time: {time}")
    #     print(f"Memory: {mem_used}")
    #     if idx == 4:
    #         print("ASSERTINGGGGGG: ")
    #         assert_input(cost, 63996)
    #         assert_input(len(y_ret), len("_T_T_TATTTTTTATTTTTATTTTATTTTTTATTTTTATTATTTATTTTATTATACGCGACGC___GATTATAC___GCGACGC_GATACGCGACGCGATTATACGCG_ACG_CGTTTA__TTATACG_CG_ACGCGATTA__TACG_CG_ACG_CGATACG_CG_ACGCGATTATACG_CG_ACGCGTT_TAT__T_TTAT_TATACG__CGACG__CGATTATACG_CG_ACG__CGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACG_CGATACG_CG_ACGCGATTATACG_CG_ACG___CGTAT_TAT_TTATTTTATTATACG_CG_ACG__CG_ATTATACGCG_ACG_CGATACG_CG_ACG_CG_AT_TATACGCGACG_CGTTTA__TTATACG_CG_ACGCGATTATACG_CG_ACG_CGATACG_CG_ACGCGATTA__TACG_CG_ACGCGTT_TAT__T_TTA__TT_ATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGATTTATTTTATTATACGCGACGCGATTA__TACG_CG_ACG_CGATACG_CG_ACGCGATTATACGCGACG_CGTTTA__TTATACG_CG_ACGCGATTATACG_CG_ACG_CGATACG_CG_ACGCGATTA__TACG_CG_ACGCGTT_TAT__T_TTA__TT_ATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTATTATTTATTTTATTATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTT_ATTATTTATTTTATTATACGCGACGCGATTATACGCG_ACG_CGATACG_CG_ACG_CG_AT_TATACGCGACG_CGTTTA__TTATACG_CG_ACGCGATTATACG_CG_ACG_CGATACG_CG_ACGCGATTA__TACG_CG_ACGCGTT_TAT__T_TTA__TT_ATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTATTATTTATTTTATTATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGATTTATTTTATTATACGCGACGCGATTA__TACG_CG_ACG_CGATACG_CG_ACGCGATTATACGCGACG_CGTTTA__TTATACG_CG_ACGCGATTATACG_CG_ACG_CGATACG_CG_ACGCGATTA__TACG_CG_ACGCGTT_TAT__T_TTA__TT_ATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTATTATTTATTTTATTATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTAT_TTATTTTATTATACGCGACGCGATTATACGCG_ACG_CGATACG_CG_ACG_CG_AT_TATACGCGACG_CGTTTA__TTATACG_CG_ACGCGATTATACG_CG_ACG_CGATACG_CG_ACGCGATTA__TACG_CG_ACGCGTT_TAT__T_TTA__TT_ATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTATTATTTATTTTATTATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGATTTATTTTATTATACGCGACGCGATTA__TACG_CG_ACG_CGATACG_CG_ACGCGATTATACGCGACG_CGTTTA__TTATACG_CG_ACGCGATTATACG_CG_ACG_CGATACG_CG_ACGCGATTA__TACG_CG_ACGCGTT_TAT__T_TTA__TT_ATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTATTATTTATTTTATTATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTT_ATTATTTATTTTATTATACGCGACGCGATTATACGCG_ACG_CGATACG_CG_ACG_CG_AT_TATACGCGACG_CGTTTA__TTATACG_CG_ACGCGATTATACG_CG_ACG_CGATACG_CG_ACGCGATTA__TACG_CG_ACGCGTT_TAT__T_TTA__TT_ATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTATTATTTATTTTATTATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGATTTATTTTATTATACGCGACGCGATTA__TACG_CG_ACG_CGATACG_CG_ACGCGATTATACGCGACG_CGTTTA__TTATACG_CG_ACGCGATTATACG_CG_ACG_CGATACG_CG_ACGCGATTA__TACG_CG_ACGCGTT_TAT__T_TTA__TT_ATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTATTATTTATTTTATTATACG__CGACG__CGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACGCGTTTATTATACG_CG_ACGCGATTATACG_CG_ACGCGATACG__CGACG__CGATTATACG_CG_ACG_CG"))
    #         print("ASSERTINGGGGGG: ")
    
    ### DATAPOINT TEST CASES ###
    datapoints_dir_name = "datapoints/"
    sample_file_names = os.listdir(datapoints_dir_name)
    # only keep file names that start with "in"
    sample_file_names = [file_name for file_name in sample_file_names if file_name.startswith("in")]
    
    # if a file is in the format of "in#.txt" where # is a number, put that file in index (# - 1)
    sample_file_names = sorted(sample_file_names, key=lambda x: int(x[2:-4]))
    print(sample_file_names)
    iter_ctr = 0
    
    for i in range(len(sample_file_names)):
        iter_ctr += 1
        word_1, word_2 = generate_input_string(datapoints_dir_name + sample_file_names[i])
        cost, x_ret, y_ret, time, mem_used = run_full_algorithm_get_efficiency(word_1, word_2)
        problem_size = len(x_ret) + len(y_ret)
        cpu_time_array.append(time)
        mem_usage_array.append(mem_used)
        problem_size_array.append(problem_size)
        # create output file per iteration run
        print(f"file index {i}")
        print(f"{cost} {time} {mem_used}")
        output_file = open(datapoints_dir_name + f"output{iter_ctr}.txt", "w")
        output_file.write(f"Cost: {cost}\n")
        output_file.write(f"X: {x_ret}\n")
        output_file.write(f"Y: {y_ret}\n")
        output_file.write(f"Time: {time}\n")
        output_file.write(f"Memory: {mem_used}\n")
        output_file.close()
        
    print("cpu_time_array: ", cpu_time_array)
    print("mem_usage_array: ", mem_usage_array)
    print("problem_size_array: ", problem_size_array)
    print("length of cpu_time_array: ", len(cpu_time_array))
    print("length of mem_usage_array: ", len(mem_usage_array))
    print("length of problem_size_array: ", len(problem_size_array))

    # plot a graph for cpu_time vs problem_size using cpu_time_array and problem_size_array
    plt.scatter(problem_size_array, cpu_time_array)
    plt.xlabel("Problem Size")
    plt.ylabel("CPU Time (ms)")
    plt.title("[EFFICIENT] CPU Time vs Problem Size")
    plt.show()

    # plot a graph for cpu_time vs problem_size using cpu_time_array and problem_size_array
    plt.scatter(problem_size_array, mem_usage_array)
    plt.xlabel("Problem Size")
    plt.ylabel("Memory (KB)")
    plt.title("[EFFICIENT] Memory vs Problem Size")
    plt.show()


    

    
if __name__ == "__main__":
    main()

