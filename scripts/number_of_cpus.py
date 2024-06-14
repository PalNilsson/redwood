# Convert csv data from Grafana to JSON
# Create number of CPUs file

import csv
import json


def read_csv_to_dict(file_path: str) -> dict:
    """
    Read a CSV file and return a dictionary.

    :param file_path: path to the CSV file (str)
    :return: output dictionary (dict).
    """
    data_dict = {}
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        # Skip the second line full of commas
        #next(reader)

        for row in reader:
            # Adjust for potential leading \ufeff and trailing whitespaces in column names
            timestamp = row.get('\ufeff"Time"'.strip())
            if timestamp:
                data_dict[timestamp] = {key.strip('"'): int(value) if value.isdigit() else value for key, value in row.items() if key != '\ufeff"Time"'}

    return data_dict


def find_max_values(data_dict: dict) -> dict:
    """
    Find the maximum values for each field in the dictionary.

    :param data_dict: data dictionary (dict)
    :return: max values dictionary (dict).
    """
    max_values = {}

    for timestamp, data in data_dict.items():
        for key, value in data.items():
            # Check if the value is an integer before comparing
            if isinstance(value, int):
                # Initialize or update the maximum value for each field
                max_values[key] = max(max_values.get(key, float('-inf')), value)

    return max_values


def write_dict_to_json(data_dict: dict, file_path: str):
    """
    Write a dictionary to a JSON file.

    :param data_dict: data dictionary (dict)
    :param file_path: path to the JSON file (str)
    """
    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=2)


#file_path = 'grafana-7days.csv'
#file_path = 'grafana-1year.csv'
file_path = 'grafana-6months.csv'
result_dict = read_csv_to_dict(file_path)

# Display the resulting dictionary
#for timestamp, data in result_dict.items():
#    print(f"Timestamp: {timestamp}, Data: {data}")

max_values = find_max_values(result_dict)

# Display the maximum values
for key, value in max_values.items():
    print(f"Max value for {key}: {value}")

print(len(max_values.items()))

write_dict_to_json(max_values, 'number_of_cpus.json')
