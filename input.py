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

def process_input(input_word: str, list_of_indices: list[int]) -> None:
    # base_string starts as input_word 
    base_string = input_word

    # (insert) input_word into base_string after index i 
    for i in list_of_indices:
        base_string = base_string[:i] + input_word + base_string[i:]

    # return base_string
    return base_string


input_word, list_of_indices = parse_input_file("input.txt")

print("Input Word: ", input_word)
print("List of Indices: ", list_of_indices)

output_string = process_input(input_word, list_of_indices)

print ("Output String: ", output_string)