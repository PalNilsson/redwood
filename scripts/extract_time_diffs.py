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
Extract time differences (job start - task start times) from a WRENCH JSON file.

..
"""

import json


def read_json_to_dict(file_path: str) -> dict:
    """
    Read a json file to a dictionary.

    :param file_path: file path (str)
    :return: json dictionary from file (dict).
    """
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data_dict = json.load(json_file)

    return data_dict


def main():
    """Perform main actions for the script."""
    # Load JSON data
    workflow_execution = read_json_to_dict('/tmp/wrench.json')
    if not workflow_execution:
        print("Failed to load JSON data")
        exit(-1)

    # Iterate through each task
    try:
        for task in workflow_execution['workflow_execution']['tasks']:
            # Extract start times
            compute_start = task['compute']['start']
            whole_task_start = task['whole_task']['start']

            # Calculate the difference
            start_time_difference = compute_start - whole_task_start

            # Print the result
            print(f"Task ID: {task['task_id']}")
            print(f"Compute Start Time: {compute_start}")
            print(f"Whole Task Start Time: {whole_task_start}")
            print(f"Difference: {start_time_difference}\n")
    except KeyError as e:
        print(f"Failed to extract data from JSON file: {e}")
        exit(-1)


if __name__ == "__main__":
    main()
