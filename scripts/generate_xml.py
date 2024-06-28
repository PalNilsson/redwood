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
    #rough_string = ET.tostring(elem, 'utf-8')
    #reparsed = minidom.parseString(rough_string)
    #pretty_string = reparsed.toprettyxml(indent="    ")  # Four spaces indentation

    # Remove the XML declaration added by minidom
    #return '\n'.join([line for line in pretty_string.split('\n') if line.strip()])

    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_string = reparsed.toprettyxml(indent="    ")  # Four spaces indentation
    # Remove the XML declaration added by minidom
    lines = pretty_string.split('\n')
    pretty_lines = []
    for line in lines:
        if line.strip() and not line.startswith('<?'):
            pretty_lines.append(line)
            # Add an empty line after each host element
            if line.strip().startswith('</host>') or line.strip().startswith('</zone>'):
                pretty_lines.append('')
    return '\n'.join(pretty_lines).strip()


def generate_xml(filename: str, num_fields: int):
    """
    Generate a trivial XML file with a specified number of fields.

    :param filename: file name to write the XML to (str)
    :param num_fields: number of fields to generate (int).
    """
    # Create the platform element with version attribute
    platform = ET.Element("platform")
    platform.set("version", "4.1")

    # Create the zone element
    zone = ET.SubElement(platform, "zone")
    zone.set("id", "AS0")
    zone.set("routing", "Full")

    # Add the controller host element with comment
    comment1 = ET.Comment(" The host on which the Controller will run ")
    zone.append(comment1)
    controller_host = ET.SubElement(zone, "host")
    controller_host.set("id", "UserHost")
    controller_host.set("speed", "10Gf")
    controller_host.set("core", "1")

    # Generate the specified number of ComputeHosts
    for i in range(1, num_fields + 1):
        # comment = ET.Comment(f" Another host on which the bare-metal compute service will be able to run jobs ")
        # zone.append(comment)

        host = ET.SubElement(zone, "host")
        host.set("id", f"ComputeHost{i}")
        host.set("speed", "35Gf")
        host.set("core", "10")

        # Add the nested prop element
        prop = ET.SubElement(host, "prop")
        prop.set("id", "ram")
        prop.set("value", "16GB")

        # Add an empty line after each ComputeHost, except the last one
        # if i < num_fields:
        #     zone.append(ET.Comment(""))  # Empty line represented by an empty comment

    # Pretty print the XML
    pretty_xml = prettify(platform)

    # Write the full XML to the output file
    with open(filename, 'w') as f:
        f.write(pretty_xml)


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
