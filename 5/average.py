import csv
import os

# Specify the data folder and file path
data_folder = r''  # Replace this with the actual path
file_path = os.path.join(data_folder, 'student_average.csv')

def load_student_data(file_name):
    """
    Reads student data from a CSV file and returns it as a list of dictionaries.
    """
    students = []
    with open(file_name, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            students.append(row)
    return students

def calculate_average(scores):
    """
    Calculates the average of a list of scores.
    """
    return sum(scores) / len(scores)

def calculate_student_averages(students):
    """
    Calculates the average marks for each student.
    Returns a dictionary with student names as keys and their average scores as values.
    """
    student_averages = {}
    for student in students:
        name = student['Name']
        scores = [int(student['Maths']), int(student['Science']), int(student['English'])]
        average_score = calculate_average(scores)
        student_averages[name] = average_score
    return student_averages

def write_student_averages(file_name, student_averages):
    """
    Writes the student averages to a CSV file.
    """
    with open(file_name, mode='w', newline='') as file:
        fieldnames = ['Name', 'Average']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for name, average in student_averages.items():
            writer.writerow({'Name': name, 'Average': average})

# Load student data from the CSV file
students = load_student_data(file_path)
print(students)

# Calculate the average marks for each student
average_marks = calculate_student_averages(students)
print(average_marks)  # Uncomment to see the averages in the console

# Write the averages to a new CSV file
output_file_path = os.path.join(data_folder, 'student_average_grades.csv')  # Output to the same folder
write_student_averages(output_file_path, average_marks)
print(f"Averages written to {output_file_path}")
