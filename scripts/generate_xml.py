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
Generate platform XML for WRENCH simulations.
Usage: python generate_xml.py --filename <filename> --nodes <number of nodes>
"""

import argparse
import xml.etree.ElementTree as ET


def generate_xml(filename, num_fields):
    # Create the root element
    root = ET.Element("root")

    # Generate the specified number of fields
    for i in range(1, num_fields + 1):
        field = ET.SubElement(root, "field")
        field.set("node", f"compute_node_{i}")
        field.set("bandwidth", "1000Mbps")

    # Create an ElementTree object
    tree = ET.ElementTree(root)

    # Write the tree to the output file
    tree.write(filename)


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Generate a trivial XML file.')
    parser.add_argument('--filename', type=str, required=True, help='The name of the output XML file.')
    parser.add_argument('--nodes', type=int, required=True, help='The number of fields in the XML file.')

    # Parse the arguments
    args = parser.parse_args()

    # Generate the XML file
    generate_xml(args.filename, args.nodes)


if __name__ == "__main__":
    main()
