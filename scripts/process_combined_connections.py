# Process the combined_connections.json file to extract connections and bandwidths
# and produce the max_connections.json with the fastest detected transfers

# Note: duplicates will be removed, ie only the fastest bandwidth of A:B and B:A will be stored

import json

# to make the fastest known connection 10 Gbit/s
scaling_factor = 2.2595857275527105


def read_json_to_dict(file_path: str) -> dict:
    """
    Read a json file to a dictionary.

    :param file_path: file path (str)
    :return: json dictionary from file (dict).
    """
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data_dict = json.load(json_file)

    return data_dict


def write_dict_to_json(data_dict: dict, file_path: str):
    """
    Write a dictionary to a json file.

    :param data_dict: data dictionary (dict)
    :param file_path: file path (str).
    """
    print(f'writing dictionary to {file_path}')
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, indent=2)


def inverse(connection: str) -> str:
    """ A:B -> B:A """
    sites = connection.split(":")
    site1 = sites[0]
    site2 = sites[1]

    return f"{site2}:{site1}"


# find max mbps values
connections_with_max = {}
connections = read_json_to_dict("combined_connections.json")
for connection in connections.keys():

    data = connections.get(connection)
    if not data:
        continue

    weeks = []
    days = []
    hours = []
    for info in data:
        weeks.append(info.get('1w', 0))
        days.append(info.get('1d', 0))
        hours.append(info.get('1h', 0))

    # it could happen that there are no '1w', '1d', '1h' values present
    highest_value = max([max(weeks), max(days), max(hours)])
    if highest_value == 0:
        print(f'no max value found for {connection}')
        continue
    connections_with_max[connection] = highest_value * scaling_factor

# find which connection has the highest transfer rate - and the slowest
fastest_connection = {}
highest_value = 0
slowest_connection = {}
lowest_value = 9999
for connection in connections_with_max:

    value = connections_with_max[connection]
    if value > highest_value:
        fastest_connection = {connection: value}
        highest_value = value
    if value < lowest_value:
        slowest_connection = {connection: value}
        lowest_value = value

# finally, only keep the highest value from A:B and B:A
reduced_connections_with_max = {}
for connection in connections_with_max:
    value1 = connections_with_max[connection]
    inv = inverse(connection)
    # has the connection already been processed?
    if inv in reduced_connections_with_max:
        continue

    if inv in connections_with_max:
        value2 = connections_with_max[inv]
    else:
        value2 = 0
    m = max(value1, value2)
    reduced_connections_with_max[connection] = m

# verify that there are no inverse connections in the final dictionary
# (test failure: reduced_connections_with_max['CYFRONET-LCG2:BNL-ATLAS'] = 0)
for connection in reduced_connections_with_max:
    inv = inverse(connection)
    if inv in reduced_connections_with_max:
        print(f'WARNING: found inverse connection {inv} ({connection})')

print(f'fastest connection: {fastest_connection}')
print(f'slowest connection: {slowest_connection}')
print(f'total number of connections (inverse connections removed): {len(reduced_connections_with_max)}')
file_path = 'max_connections.json'
write_dict_to_json(reduced_connections_with_max, file_path)
