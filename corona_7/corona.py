import os
import json
from collections import defaultdict

# Function to read all JSON files in the given directory and its subdirectories
def read_json_files(directory):
    data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        file_data = json.load(f)
                        data.append(file_data)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {file_path}")
                except Exception as e:
                    print(f"An error occurred while reading {file_path}: {e}")
    return data

# Function to calculate statistics for each country
def calculate_statistics(data):
    stats = defaultdict(lambda: {'confirmed_cases': 0, 'deaths': 0, 'recovered': 0})
    
    # Summing up the values for each country
    for entry in data:
        country = entry['country']
        stats[country]['confirmed_cases'] += entry['confirmed_cases']['total']
        stats[country]['deaths'] += entry['deaths']['total']
        stats[country]['recovered'] += entry['recovered']['total']
    
    # Calculate active cases
    for country, values in stats.items():
        values['active_cases'] = values['confirmed_cases'] - values['deaths'] - values['recovered']
    
    return stats

# Function to find the top 5 countries with highest and lowest confirmed cases
def find_top_bottom_countries(stats):
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]['confirmed_cases'], reverse=True)
    top_5_countries = sorted_stats[:5]
    bottom_5_countries = sorted_stats[-5:]
    
    return top_5_countries, bottom_5_countries

# Function to generate the summary report and save it to a JSON file
def generate_summary_report(stats, file_name='covid19_summary.json'):
    with open(file_name, 'w') as f:
        json.dump(stats, f, indent=4)

# Main function to execute the program
def main(directory):
    # Step 1: Read the data from all JSON files
    data = read_json_files(directory)
    
    # Step 2: Calculate statistics for each country
    stats = calculate_statistics(data)
    
    # Display statistics for each country
    for country, values in stats.items():
        print(f"Country: {country}")
        print(f"Total Confirmed Cases: {values['confirmed_cases']}")
        print(f"Total Deaths: {values['deaths']}")
        print(f"Total Recovered: {values['recovered']}")
        print(f"Total Active Cases: {values['active_cases']}")
        print("-" * 40)

    # Step 3: Find the top 5 and bottom 5 countries based on confirmed cases
    top_5, bottom_5 = find_top_bottom_countries(stats)
    
    # Display the top 5 and bottom 5 countries
    print("\nTop 5 countries with highest confirmed cases:")
    for country, values in top_5:
        print(f"{country}: {values['confirmed_cases']} confirmed cases")
    
    print("\nBottom 5 countries with lowest confirmed cases:")
    for country, values in bottom_5:
        print(f"{country}: {values['confirmed_cases']} confirmed cases")

    # Step 4: Generate the summary report and save it to a file
    generate_summary_report(stats)

# Directory where your JSON files are stored
directory = r'7'  # Replace with your actual directory path

# Run the program
main(directory)
