#!/usr/bin/python3

# Python Code
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def read_scrabble_score(path:str):
    with open(path, "r") as file:
        result = file.read()
    return result

def read_student_data():
    pass

def show_count_scrabble_score():
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

  	# Plots for the main assignment 
    show_count_scrabble_score(data)
    show_count_average_grade(data)
    show_name_length_vs_scrabble_score(data)
    show_average_grade_vs_scrabble_score(data)

  	# Uncomment the code below for the extra bits
  
    # # Extra Bit Option 1
    # show_programming_history("programming_time_data.npy")

    # # Extra Bit Option 2
  	# # If pillow is not installed on your computer you can install it using: "conda install pillow"
  	# with Image.open("pumpkin.png") as img:
    #     img = np.array(img)
    # show_mask_pumpkin(img, size=5)