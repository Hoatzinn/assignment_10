#!/usr/bin/python3

# Python Code
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

#region assignment 9
class ScrabbleScorer:
    """
    A class representing a scrabble score

    Attributes:
        scrabble_scores (dict): the scores of each of the letters in the alphabet
    -----------------------------------------------------------------------------
    Notable methods:
        __call__: an instance of ScrabbleScorer is callable and can be used to calculate the score of a input-string
    """
    def __init__(self, scrabble_scores:dict):
        self.scrabble_scores = scrabble_scores
    
    def __call__(self, input_string:str) -> int:
        input_string = input_string.upper()
        score = 0
        for char in input_string:
            if char in self.scrabble_scores:
                score += self.scrabble_scores[char]
        return score
    
    def __eq__(self, scrabble_scores):
        return scrabble_scores.scrabble_scores == self.scrabble_scores
    
    def __repr__(self):
        return str(self.scrabble_scores)


class Student:
    """
    A class representing a student

    Attributes:
        name (str): the name of the student
        grades (list): a list of floats containing the grades of the student
        scrabble_scorer (dict or ScrabbleScorer): the scrabble scores for each letter of the student
    ------------------------------------------------------------------------------------------------
    Notable methods:
        new_grade: adds a grade (float) to the student
        getter and setter methods: get_grades, set_grades, get_scrabble_scorer and set_scrabble_scorer
        name_value: returns the score of the student-name based of of the scrabble_scorer parameter
    """
    def __init__(self, name:str, grades:list, scrabble_scorer:dict | ScrabbleScorer):
        self.name = name
        self.grades = grades

        if isinstance(scrabble_scorer, dict):
            scrabble_scorer = ScrabbleScorer(scrabble_scorer)
        self.scrabble_scorer = scrabble_scorer

        self.num = 0

    def new_grade(self, grade:float):
        self.grades.append(grade)
    
    def get_grades(self):
        return self.grades

    def set_grades(self, grades = []):
        if isinstance(grades, list):
            self.grades = grades
        else:
            raise TypeError(f"grades must be of type list (not {type(grades)})")
    
    def get_scrabble_scorer(self):
        return self.scrabble_scorer
    
    def set_scrabble_scorer(self, scrabble_scorer:dict | ScrabbleScorer):
        if isinstance(scrabble_scorer, dict):
            self.scrabble_scorer = ScrabbleScorer(scrabble_scorer)
        elif isinstance(scrabble_scorer, ScrabbleScorer):
            self.scrabble_scorer = scrabble_scorer
        else:
            raise TypeError(f"scrabblescorer must be of type ScrabbleScorer (not {type(scrabble_scorer)})")
    
    def name_value(self):
        return self.scrabble_scorer(self.name)
    
    def __repr__(self):
        return f"Student(name={self}, grades={self.grades})"

    def __gt__(self, student):
        return self.name_value() > student.name_value()
    def __lt__(self, student):
        return self.name_value() < student.name_value()
    def __ge__(self, student):
        return self.name_value() >= student.name_value()
    def __le__(self, student):
        return self.name_value() <= student.name_value()
    def __eq__(self, student):
        return self.name_value() == student.name_value()
    def __ne__(self, student):
        return self.name_value() != student.name_value()
    

    def __len__(self):
        return len(self.grades)

    def __iter__(self):
        return iter(self.grades)
 
    def __str__(self):
        return self.name

class Database:
    """
    A class representing a database of students

    Attributes:
        input_list (list): a list containing all the students
    ---------------------------------------------------------
    Notable methods:
        sort: sorts the Database based on a key
        __call__: an instance of this class is callable and can used to return the abundance of a key input
    """
    def __init__(self, input_list:list = []):
        self.list = input_list
    
    def sort(self, key=lambda a:a, reverse=False):
        self.list.sort(key=key, reverse=reverse)

    def __repr__(self):
        return str([student for student in self.list])
    
    def __add__(self, second_database):
        return Database(self.list + second_database.list)

    def __call__(self, object=lambda a : a.name_value()):
        dictionary = {}
        
        reduced_list = map(object, self.list)

        for element in reduced_list:
            try:
                dictionary[element] = dictionary[element]+1
            except KeyError:
                dictionary[element] = 1
        
        return dictionary

#endregion

def read_scrabble_score(path:str) -> ScrabbleScorer:
    """
    Reads the contents of the scrabble_scores.json file and returns a ScrabbleScorer object based on the contents.

        Parameters:
            path (str): the path of the JSON file
        Returns:
            scrabble_score (ScrabbleScorer): Scrabble scores for a Student instance
    """
    with open(path, "r") as file:
        content = file.readlines()
    
    content = content[1:-1]
    dictionary = {}
    for line in content:
        if not line == content[-1]:
            dictionary[line[5]] = int(line[9:-2])
        else:
            dictionary[line[5]] = int(line[9:-1])

    return ScrabbleScorer(dictionary)

def read_student_data(path: str, scrabble: ScrabbleScorer) -> Database:
    """
    Reads the contents of the database.csv file and returns the contents in a Database instance

        Parameters:
            path (str): the path of the CSV file
            scrabble (ScrabbleScorer): 
        Returns:
            data (Database): student data in Database format
    """
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
        list_of_students.append(Student(student_names[student_number], student_grades[student_number], scrabble))
    
    return Database(list_of_students)


def show_count_scrabble_score(data: Database) -> None:
    """
    Reads contents from a Database-instance and shows a bar plot based on the abundance of Student.name_values scores
        
        Parameters:
            data (Database): database containing Student-instances
        Returns:
            None
    """
    d = data()
    scores = list(d.keys())
    abundance = list(d.values())
    plt.bar(scores, abundance)
    plt.ylabel("Abundance of name values")
    plt.xlabel("Scrabble score")
    plt.title("Scrabble score count")
    plt.show()

def show_count_average_grade(data: Database) -> None:
    """
    Reads contents from a Database-instance and shows a hist plot based on the average grade of the Student-instances in it
        
        Parameters:
            data (Database): database containing Student-instances
        Returns:
            None
    """
    average_grades = list(map(lambda student: np.mean(student.get_grades()), data.list))

    plt.hist(average_grades, 50)
    plt.ylabel("Amount of averages grades")
    plt.xlabel("Average grade")
    plt.title("Abundance of student grades")
    plt.show()

def show_average_grade_vs_scrabble_score(data: Database) -> None:
    """
    Reads contents from a Database-instance and shows a scatter plot based on average grade vs the name_value of the Student-instances 
        
        Parameters:
            data (Database): data containing Student-instances
        Returns:
            None
    """
    average_grades = list(map(lambda student: np.mean(student.get_grades()), data.list))
    scrabble_scores = list(map(lambda student: student.name_value(), data.list))

    plt.scatter(average_grades, scrabble_scores, 4)
    plt.xlabel("Average Grades of student")
    plt.ylabel("Name Value of student")
    plt.title("Average Grades vs Name Value")
    plt.grid(True)
    plt.show()

def show_name_length_vs_scrabble_score(data: Database) -> None:
    """
    Reads contents from a Database-instance and shows a scatter plot based on length of the names vs the name_value of the Student-instances
        
        Parameters:
            data (Database): data containing Student-instances
        Returns:
            None
    """
    name_lengths = list(map(lambda student: len(student.name), data.list))
    scrabble_scores = list(map(lambda student: student.name_value(), data.list))

    plt.scatter(name_lengths, scrabble_scores, 4)
    plt.xlabel("Length of Student Name")
    plt.ylabel("Name Value of Student")
    plt.title("Name length vs Name Value")
    plt.grid(True)
    plt.show()

def average_rgb(pixel_list: np.array) -> np.array:
    """
    Return the average RGB of a 2D or 3D NumPy array

        Parameters:
            pixel_list (numpy.array): 2D or 3D array of RGB-values
        
        Returns:
            RBG-value (np.array): average RGB value
    """
    if pixel_list.shape[-1] != 3:
        raise ValueError(f"Please insert list of lists (of lists) with final lists of 3 elements (rgb), not {pixel_list.shape[-1]} elements.")
    result = []

    if len(pixel_list.shape) == 2:
        for channel in range(3):
            result.append(np.mean(list(map(lambda pix: pix[channel], pixel_list))))

    elif len(pixel_list.shape) == 3:
        temp_result = []
        for line in pixel_list:
            line_average = []
            for channel in range(3):
                line_average.append(np.mean(list(map(lambda pix: pix[channel], line))))
            temp_result.append(line_average)
        temp_result = np.array(temp_result).astype(int)
        
        for channel in range(3):
            result.append(np.mean(list(map(lambda pix: pix[channel], temp_result))))

    else:
        raise ValueError(f"pixel_list has too many or too few dimension ({len(pixel_list.shape)} dimensions)")
        
    return np.array(result)


def show_mask_pumpkin(image: np.array, size: int) -> None:
    """
    Shows a masked pumpkin image, where the pumpkin is pixelated

        Parameters:
            image (numpy.array): the image in numpy.array
            size (int): changes the size of the pixels
        
        Returns:
            None
    """
    area = ((57, 122), (257, 322))
    x1, y1 = area[0]
    x2, y2 = area[1]

    masked_image = image.copy()

    for x in range(x1, x2, size):
        for y in range(y1, y2, size):
            # print(f"Changing area x1: {x} to x2: {x+size}, y1: {y} to y2: {y+size}")
            masked_image[y:y+size, x:x+size] = average_rgb(image[y:y+size, x:x+size])

    plt.imshow(masked_image, interpolation='nearest')
    plt.show()

if __name__ == "__main__":
    # Reading in the data
    scrabble = read_scrabble_score("scrabble_scores.json")
    data = read_student_data("database.csv", scrabble)

    # Plots for the main assignment 
    show_count_scrabble_score(data)
    show_count_average_grade(data)
    show_average_grade_vs_scrabble_score(data)
    show_name_length_vs_scrabble_score(data)

    # Extra Bit Option 2
    # If pillow is not installed on your computer you can install it using: "conda install pillow"
    with Image.open("pumpkin.png") as img:
        img = np.array(img)
    show_mask_pumpkin(img, size=10)