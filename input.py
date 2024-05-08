# file for reading input text
import os
import sys

def print_lines(lines: list[str]):
    for line in lines:
        print(line) 

def parse_input_file(file_name: str) -> tuple[str, str]:
    
    # store input word, list of indices, and file lines
    input_word = ""
    lines = ""
    list_of_indices = []
    

    # check if file exists, read all lines
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    # store input word and list of indices
    input_word = lines[0].strip()
    for i in range(1, len(lines)):
        list_of_indices.append(int(lines[i].strip()))
    
    # return input word and list of indices
    return input_word, list_of_indices        

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

def generate_input_string(file_name: str, actual_base_string: str = "", verbose: bool = False):
    # parse input file
    input_word, list_of_indices = parse_input_file(file_name)

    if verbose:
        print("Input Word: ", input_word)
        print("List of Indices: ", list_of_indices)

    # process input
    output_string = process_input(input_word, list_of_indices, verbose)

    if verbose:
        print ("Output String: ", output_string)

    if actual_base_string == "":
        return output_string

    # assert input
    assert_input(output_string, actual_base_string)

    return output_string

validation_string = "ACACTGACTACTGACTGGTGACTACTGACTGG"
generate_input_string("input.txt", validation_string, verbose=True)