# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Author:
# - Paul Nilsson, paul.nilsson@cern.ch, 2024

"""
Convert csv data from Grafana to JSON.
Create number of CPUs file.
"""

import csv
import json


def read_csv_to_dict(file_path: str) -> dict:
    """
    Read a CSV file and return a dictionary.

    :param file_path: path to the CSV file (str)
    :return: output dictionary (dict).
    """
    data_dict = {}
    with open(file_path, 'r', encoding='utf-8') as csv_file:
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

    for _, data in data_dict.items():
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
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, indent=2)


# path = 'grafana-7days.csv'
# path = 'grafana-1year.csv'
path = 'grafana-6months.csv'
result_dict = read_csv_to_dict(path)

# Display the resulting dictionary
# for timestamp, data in result_dict.items():
#     print(f"Timestamp: {timestamp}, Data: {data}")

_max_values = find_max_values(result_dict)

# Display the maximum values
for _key, _value in _max_values.items():
    print(f"Max value for {_key}: {_value}")

print(len(_max_values.items()))

write_dict_to_json(_max_values, 'number_of_cpus.json')
