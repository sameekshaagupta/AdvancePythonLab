import os
import json
import re
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import numpy as np
# Function to check if the file exists
def file_exists(filename):
    return os.path.exists(filename)

# Function to validate email format
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Function to validate data for each student
def validate_student_data(student):
    errors = []

    # Check Student ID
    if not isinstance(student.get('Student ID'), int) or student['Student ID'] <= 0:
        errors.append('Invalid Student ID')
    
    # Check Name
    if not isinstance(student.get('Name'), str) or not student['Name'].strip():
        errors.append('Invalid Name')
    
    # Check Email
    if not is_valid_email(student.get('Email')):
        errors.append('Invalid Email')
    
    # Check Course Name
    if not isinstance(student.get('Course Name'), str) or not student['Course Name'].strip():
        errors.append('Invalid Course Name')
    
    # Check Credits
    if not isinstance(student.get('Credits'), int) or student['Credits'] <= 0:
        errors.append('Invalid Credits')
    
    # Check Grade
    valid_grades = ['A', 'B', 'C', 'F']
    if student.get('Grade') not in valid_grades:
        errors.append('Invalid Grade')
    
    return errors

# Function to load the data from the json file
def load_data(filename):
    if not file_exists(filename):
        raise FileNotFoundError(f"File {filename} not found.")
    
    with open(filename, 'r') as file:
        return json.load(file)
#hehe
# Function to generate bar chart
def generate_pie_chart(grade_distribution):
    labels = list(grade_distribution.keys())
    sizes = list(grade_distribution.values())
    
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("Grade Distribution")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig("grade_distribution_pie_chart.png")
    plt.close()

# Generate Histogram for Credits
def generate_histogram(credits):
    plt.figure(figsize=(6, 6))
    plt.hist(credits, bins=range(min(credits), max(credits) + 1), edgecolor='black', alpha=0.7)
    plt.title("Credits Distribution Histogram")
    plt.xlabel("Credits")
    plt.ylabel("Number of Students")
    plt.savefig("credits_histogram.png")
    plt.close()

# Generate Multiple Bar Charts
def generate_multiple_bar_charts(course_distribution, grade_distribution):
    # Course Distribution Bar Chart
    plt.figure(figsize=(6, 6))
    plt.bar(course_distribution.keys(), course_distribution.values(), color='skyblue')
    plt.title("Course Distribution")
    plt.xlabel("Courses")
    plt.ylabel("Number of Students")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("course_distribution_bar_chart.png")
    plt.close()
def generate_stacked_bar_chart(course_distribution, grade_distribution):
    courses = list(course_distribution.keys())
    grades = ['A', 'B', 'C', 'F']

    # Initialize data for stacking the bars
    grade_counts = {grade: [0] * len(courses) for grade in grades}

    # Populate the grade counts for each course
    for i, course in enumerate(courses):
        for grade, count in grade_distribution.items():
            grade_counts[grade][i] = count.get(course, 0)

    # Convert counts into arrays for stacked bars
    a_counts = np.array(grade_counts['A'])
    b_counts = np.array(grade_counts['B'])
    c_counts = np.array(grade_counts['C'])
    f_counts = np.array(grade_counts['F'])

    # Plot the stacked bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(courses, a_counts, label='A', color='green')
    plt.bar(courses, b_counts, bottom=a_counts, label='B', color='blue')
    plt.bar(courses, c_counts, bottom=a_counts + b_counts, label='C', color='orange')
    plt.bar(courses, f_counts, bottom=a_counts + b_counts + c_counts, label='F', color='red')

    plt.xlabel("Courses")
    plt.ylabel("Number of Students")
    plt.title("Stacked Bar Chart - Course and Grade Distribution")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig("stacked_bar_chart.png")
    plt.close()
#hehe
def generate_bar_chart(course_data):
    courses = list(course_data.keys())
    student_counts = list(course_data.values())
    
    plt.bar(courses, student_counts, color='skyblue')
    plt.xlabel('Courses')
    plt.ylabel('Number of Students')
    plt.title('Course Enrollment Distribution')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('course_distribution.png')
    plt.close()

# Function to create the PDF report
def create_pdf_report(course_data, average_credits, grade_distribution):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'University Course Enrollment Report - ' + datetime.now().strftime('%Y-%m-%d'), ln=True, align='C')
    pdf.ln(10)
    
    # Course Distribution
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, 'Course Distribution:', ln=True)
    for course, count in course_data.items():
        pdf.cell(200, 10, f"{course}: {count} students", ln=True)
    
    pdf.ln(10)
    
    # Average Credits
    pdf.cell(200, 10, f"Average Credits: {average_credits:.2f}", ln=True)
    
    pdf.ln(10)
    
    # Grade Distribution
    pdf.cell(200, 10, 'Grade Distribution:', ln=True)
    for grade, count in grade_distribution.items():
        pdf.cell(200, 10, f"{grade}: {count} students", ln=True)
    
    # Insert bar chart image
    pdf.ln(10)
    pdf.cell(200, 10, 'Course Enrollment Distribution:', ln=True)
    pdf.image('course_distribution.png', x=10, y=pdf.get_y(), w=190)
    
    # Output the PDF
    pdf.output("course_enrollment_report.pdf")

# Main function to process the data
def main():
    try:
        # Load the data from the JSON file
        filename = 'course_enrollment_data.json'
        data = load_data(filename)
        
        # Initialize statistics
        course_data = {}
        total_credits = 0
        grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'F': 0}
        valid_students = 0
        invalid_students = 0
        
        # Process each student entry
        for student in data:
            errors = validate_student_data(student)
            if errors:
                print(f"Invalid entry for Student ID {student['Student ID']}: {', '.join(errors)}")
                invalid_students += 1
            else:
                valid_students += 1
                # Update course data
                course = student['Course Name']
                course_data[course] = course_data.get(course, 0) + 1
                # Update total credits
                total_credits += student['Credits']
                # Update grade distribution
                grade_distribution[student['Grade']] += 1
        
        # Calculate average credits
        average_credits = total_credits / valid_students if valid_students > 0 else 0
        
        # Generate bar chart
        generate_bar_chart(course_data)
        
        # Create PDF report
        create_pdf_report(course_data, average_credits, grade_distribution)
        
        print(f"Processing complete. Valid students: {valid_students}, Invalid students: {invalid_students}")
        print("Report generated: 'course_enrollment_report.pdf'")
    
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError:
        print("Error decoding the JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
