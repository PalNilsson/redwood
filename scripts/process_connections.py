# process the latest.json rucio file to extract connections and bandwidths

import json
import os


def read_json_to_dict(file_path: str) -> dict:
    """
    Read a json file to a dictionary.

    :param file_path: file path (str)
    :return: json dictionary from file (dict).
    """
    with open(file_path, 'r') as json_file:
        data_dict = json.load(json_file)

    return data_dict


def write_dict_to_json(data_dict: dict, file_path: str):
    """
    Write a dictionary to a json file.

    :param data_dict: data dictionary (dict)
    :param file_path: file path (str).
    """
    print(f'writing dictionary to {file_path}')
    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=2)


# input_files = ['latest.json']
input_files = [
    'latest-01.10.2024.json',
    'latest-01.23.2024.json',
    'latest-14.02.2024.json',
    'latest-26.02.2024.json',
    'latest-04.03.2024.json',
    'latest-11.03.2024.json',
    'latest-18.03.2024.json',
    'latest-25.03.2024.json',
    'latest-01.04.2024.json',
    'latest-08.04.2024.json',
    'latest-15.04.2024.json',
    'latest-22.04.2024.json',
    'latest-29.04.2024.json',
    'latest-30.04.2024.json',
    'latest-01.05.2024.json',
    'latest-02.05.2024.json',
    'latest-03.05.2024.json',
    'latest-06.05.2024.json',
    'latest-13.05.2024.json',
    'latest-20.05.2024.json',
    'latest-27.05.2024.json',
    'latest-04.06.2024.json',
    'latest-10.06.2024.json',
]

data_dir = os.path.join(os.getcwd(), 'data')

# extract all info; { connection: [dashb] }
all_connections = {}

# get connections and bandwidths
for file_name in input_files:
    print(f'processing {file_name}')
    connections = read_json_to_dict(os.path.join(data_dir, file_name))

    for connection in connections.keys():

        sites = connection.split(':')
        local_site = sites[0]
        remote_site = sites[1]
        # ignore self-connection
        if local_site == remote_site:
            continue
        if 'UNKNOWN' in {local_site, remote_site}:
            continue

        if connection not in all_connections:
            all_connections[connection] = []

        # are there any bandwidth numbers for this connection?
        mbps = connections.get(connection).get('mbps')
        if not mbps:
            # print(f'no mbps info for connection {connection}')
            continue

        dashb = mbps.get('dashb')
        if not dashb:
            print(f'no dashb info for connection {connection}')
            continue

        # print(f'connectino={connection} dashb={dashb}')

        all_connections[connection].append(dashb)

empty = 0
# names = []
for connection in all_connections.keys():

    bandwidths = all_connections[connection]
    # print(f'connection={connection} bandwidths={bandwidths}')
    if not bandwidths:
        empty += 1
        # names.append(connection)

print(f'There were {empty} empty connections out of a total of {len(all_connections.keys())}')
write_dict_to_json(all_connections, 'combined_connections.json')
