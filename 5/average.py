import csv;

def calculate_average(scores):
    return sum(scores)/len(scores)
students = []
with open('5\student_average.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        name = row['Name']
        scores = [int(row['Maths']), int(row['Science']), int(row['Hindi'])]
        average_score = calculate_average(scores)
        students.append({'Name': name, 'Average': average_score})


with open('student_average_grade.csv', mode='w', newline='') as file:
    fieldnames = ['Name', 'Average']
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()
    for student in students:
        csv_writer.writerow({'Name': student['Name'], 'Average': student['Average']})
print("Average scores have been calculate and written to 'student_average_grade.csv'")