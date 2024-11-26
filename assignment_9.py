#!/usr/bin/python3

# define the ScrabbleScorer class, which takes one argument, of type dictionary
class ScrabbleScorer:
    def __init__(self, scrabble_scores:dict):
        self.scrabble_scores = scrabble_scores
    
    # __call__ takes one argument of type string, and returns the score of that string based on the scores of the characters according to scrabble_scores
    def __call__(self, input_string:str) -> int:
        input_string = input_string.upper()
        score = 0
        for char in input_string:
            if char in self.scrabble_scores:
                score += self.scrabble_scores[char]
        return score
    
    # __eq__ allows instances of ScrabbleScorer to be checked on equality according to the scrabble_scores dictionary
    def __eq__(self, scrabble_scores):
        return scrabble_scores.scrabble_scores == self.scrabble_scores
    
    def __repr__(self):
        return str(self.scrabble_scores)


# define the Student class which takes a name a list of grades and a scrabble_scorer of type dict or of type ScrabbleScorer
class Student:
    def __init__(self, name:str, grades:list, scrabble_scorer:dict | ScrabbleScorer):
        self.name = name
        self.grades = grades

        # checks what the type is of scrabble_scorer and adjusts the self.scrabble_scorer variable accordingly
        if isinstance(scrabble_scorer, dict):
            scrabble_scorer = ScrabbleScorer(scrabble_scorer)
        self.scrabble_scorer = scrabble_scorer

        self.num = 0

    # this function adds a grde to self.grade
    def new_grade(self, grade:float):
        self.grades.append(grade)
    
    # this function returns self.grades
    def get_grades(self):
        return self.grades

    # this function changes self.grades to the input grades
    def set_grades(self, grades = []):
        if isinstance(grades, list):
            self.grades = grades
        else:
            raise TypeError(f"grades must be of type list (not {type(grades)})")
    
    # this function returns the scrabble_scorer variable
    def get_scrabble_scorer(self):
        return self.scrabble_scorer
    
    # this function allows for setting the scrabble_scorer from a function
    def set_scrabble_scorer(self, scrabble_scorer:dict | ScrabbleScorer):
        if isinstance(scrabble_scorer, dict):
            self.scrabble_scorer = ScrabbleScorer(scrabble_scorer)
        elif isinstance(scrabble_scorer, ScrabbleScorer):
            self.scrabble_scorer = scrabble_scorer
        else:
            raise TypeError(f"scrabblescorer must be of type ScrabbleScorer (not {type(scrabble_scorer)})")
    
    # allows for calculating of the value of the student
    def name_value(self):
        return self.scrabble_scorer(self.name)
    
    # representation of student
    def __repr__(self):
        return f"Student(name={self}, grades={self.grades})"

    # all comparison operators
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
    
    
    # this function calculates the length of the grades
    def __len__(self):
        return len(self.grades)

    # this function allows the student to be used as an iterator
    def __iter__(self):
        self.num = 0
        return self
    
    # this function iterates through the grades
    def __next__(self):
        if self.num > len(self.grades)-1:
            raise StopIteration
        else:
            self.num += 1
            return self.grades[self.num-1]
    
    # string representation of Student, with self.name as output
    def __str__(self):
        return self.name

# define the Database class which takes one optional list as input
class Database:
    def __init__(self, input_list:list = []):
        self.list = input_list
    
    # this function allows the database to be sorted using a function as input, and to be reversed using the reverse argument
    def sort(self, key=lambda a:a, reverse=False):
        self.list.sort(key=key, reverse=reverse)

    # string representation of a Database instance
    def __repr__(self):
        return str([student for student in self.list])
    
    # allows addition of two Database instances
    def __add__(self, second_database):
        return Database(self.list + second_database.list)

    # allows instances of Database to be called, which returns the abundance of an argument of student
    def __call__(self, object=lambda a : a.name_value()):
        dictionary = {}
        
        reduced_list = map(object, self.list)

        for element in reduced_list:
            try:
                dictionary[element] = dictionary[element]+1
            except KeyError:
                dictionary[element] = 1
        
        return dictionary