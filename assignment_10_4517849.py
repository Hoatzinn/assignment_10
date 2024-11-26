#!/usr/bin/python3

# Python Code
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import assignment_9

def read_scrabble_score(path:str) -> assignment_9.ScrabbleScorer:
    with open(path, "r") as file:
        content = file.readlines()
    
    content = content[1:-1]
    dictionary = {}
    for line in content:
        if not line == content[-1]:
            dictionary[line[5:6]] = int(line[9:-2])
        else:
            dictionary[line[5:6]] = int(line[-3:-1])

    return assignment_9.ScrabbleScorer(dictionary)

def read_student_data(path: str, scrabble: assignment_9.ScrabbleScorer) -> assignment_9.Database:
    with open(path, "r") as file:
        content = file.read()
    content = content.split("\n")

    content = [line.split(",") for line in content]
    
    improved_list = []
    for line in content:
        for e in range(len(line)):
            if line[e] == "":
                line = line[:e]
                break
        improved_list.append(line)
    
    improved_list = improved_list[1:-1]
    
    student_names = [line[0] for line in improved_list]
    
    student_grades = [line[1:] for line in improved_list]
    student_grades = [[float(grade) for grade in student] for student in student_grades] # or values = [list(map(float, student)) for student in values]

    list_of_students = []

    for student_number in range(len(student_names)):
        list_of_students.append(assignment_9.Student(student_names[student_number], student_grades[student_number], scrabble))
    
    return assignment_9.Database(list_of_students)


def show_count_scrabble_score(data: assignment_9.Database):
    pass

def show_count_average_grade():
    pass

def show_average_grade_vs_scrabble_score():
    pass

def show_name_length_vs_scrabble_score():
    pass

if __name__ == "__main__":
  	# Reading in the data
    scrabble = read_scrabble_score("scrabble_scores.json")
    data = read_student_data("database.csv", scrabble)
    print(data)

  	# # Plots for the main assignment 
    # show_count_scrabble_score(data)
    # show_count_average_grade(data)
    # show_name_length_vs_scrabble_score(data)
    # show_average_grade_vs_scrabble_score(data)

  	# Uncomment the code below for the extra bits
  
    # # Extra Bit Option 1
    # show_programming_history("programming_time_data.npy")

    # # Extra Bit Option 2
  	# # If pillow is not installed on your computer you can install it using: "conda install pillow"
  	# with Image.open("pumpkin.png") as img:
    #     img = np.array(img)
    # show_mask_pumpkin(img, size=5)