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
from xml.dom import minidom


def prettify(elem: ET.Element) -> str:
    """
    Return a pretty-printed XML string for the Element.

    :param elem: XML element (ET.Element)
    :return: pretty-printed XML string (str).
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_string = reparsed.toprettyxml(indent="  ")

    # Remove the XML declaration added by minidom
    return '\n'.join(pretty_string.split('\n')[1:])


def generate_xml(filename: str, num_fields: int):
    """
    Generate a trivial XML file with a specified number of fields.

    :param filename: file name to write the XML to (str)
    :param num_fields: number of fields to generate (int).
    """
    # Create the root element
    root = ET.Element("root")

    # Generate the specified number of fields
    for i in range(1, num_fields + 1):
        field = ET.SubElement(root, "field")
        field.set("node", f"compute_node_{i}")
        field.set("bandwidth", "1000Mbps")

    # Pretty print the XML
    pretty_xml = prettify(root)

    # Add the XML declaration and DOCTYPE
    xml_declaration = "<?xml version='1.0'?>\n<!DOCTYPE platform SYSTEM \"https://simgrid.org/simgrid.dtd\">\n"
    full_xml = xml_declaration + pretty_xml

    # Write the pretty-printed XML to the output file
    with open(filename, 'w') as f:
        f.write(full_xml)


def main():
    """Perform main actions for the script."""
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
