# Combine GFLOPS, number of CPUs and RSE info into one file.
# The total GFLOPS number is calculated by multiplying the GFLOPS number per CPU with
# the total number of CPUs.

# use queue_corecount.json for number of cores per queue
# use corepower.json for corepower, ie the average benchmark per core for a queue

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


def write_dict_to_json(data_dict: dict, file_path: str):
    """
    Write a dictionary to a JSON file.

    :param data_dict: data dictionary (dict)
    :param file_path: path to the JSON file (str)
    """
    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=2)  # 'indent' parameter is used for pretty formatting


queues_and_rses = read_json_to_dict('queues_and_rses.json')

option = 2
scale_factor = 1 if option == 1 else 10

# option 1
# based on average run times and total number of CPUs
# gflops_per_cpu = read_json_to_dict('gflops_per_cpu.json')
# number_of_cpus = read_json_to_dict('number_of_cpus.json')

# option 2
# based on corepower and total number of cores
gflops_per_cpu = read_json_to_dict('corepower.json')
number_of_cpus = read_json_to_dict('queue_corecount.json')

# add new field 'gflops' to queues and rses dictionary
combined = {}
for queue in queues_and_rses:

    # get the number of CPUs for this queue
    n_cpus = number_of_cpus.get(queue)
    if not n_cpus:
        print(f'number of CPUs unknown for {queue}')
        continue

    # get the GFLOPS number for this queue
    if option == 1:
        gflops = gflops_per_cpu.get(queue)
    else:
        d = gflops_per_cpu.get(queue)
        gflops = d.get('corepower')
    if not gflops:
        print(f'GFLOPS unknown for {queue}')
        continue

    # verify that the queue has RSE(s)
    rses = queues_and_rses.get(queue)
    if not rses:
        print(f'RSE(s) unknown for {queue}')
        continue

    # add to new dictionary
    try:
        combined[queue] = {}
        combined[queue]['RSE'] = rses.get('RSE')
        combined[queue]['GFLOPS'] = int(gflops) * int(n_cpus) * scale_factor
    except Exception as exc:
        print(f'exception caught: {exc}')

print(f'combined info for {len(combined.keys())} queues')
filename = 'queues-runtimes_based.json' if option == 1 else 'queues-corepower_based.json'
write_dict_to_json(combined, filename)
