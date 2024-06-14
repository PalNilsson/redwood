# Make sure that all queues have populated RSE and GFLOPS info
# Note: the filtering was perhaps already done by the scripts that
#       created the earlier JSON files. The script also writes out
#       the number of queues (150 as of June 14, 2024).

import json


def read_json_to_dict(file_path: str) -> dict:
    """
    Read a json file to a dictionary.

    :param file_path: path to the JSON file (str)
    :return: data dictionary (dict).
    """
    with open(file_path, 'r') as json_file:
        data_dict = json.load(json_file)

    return data_dict


queues = read_json_to_dict('queues-corepower_based.json')

# make sure there are entries for all queues
for queue in queues:

    # get the GFLOPS number for this queue
    gflops = queues.get(queue).get("GFLOPS")
    if not gflops:
        print(f'GFLOPS unknown for {queue}')

    # verify that the queue has RSE(s)
    rses = queues.get(queue).get("RSE")
    if not rses:
        print(f'RSE(s) unknown for {queue}')

print(f"verified {len(queues)} queues")
