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
        comment = ET.Comment(" Another host on which the bare-metal compute service will be able to run jobs ")
        zone.append(comment)

        host = ET.SubElement(zone, "host")
        host.set("id", f"ComputeHost{i}")
        host.set("speed", "35Gf")
        host.set("core", "10")

        # Add the nested prop element
        prop = ET.SubElement(host, "prop")
        prop.set("id", "ram")
        prop.set("value", "16GB")

    # Generate the specified number of StorageHosts
    for i in range(1, num_fields + 1):
        comment = ET.Comment(" The host on which the first storage service will run ")
        zone.append(comment)

        host = ET.SubElement(zone, "host")
        host.set("id", f"StorageHost{i}")
        host.set("speed", "10Gf")
        host.set("core", "1")

        # Add the nested disk element with its properties
        disk = ET.SubElement(host, "disk")
        disk.set("id", "hard_drive")
        disk.set("read_bw", "100MBps")
        disk.set("write_bw", "100MBps")

        prop_size = ET.SubElement(disk, "prop")
        prop_size.set("id", "size")
        prop_size.set("value", "5000GiB")

        prop_mount = ET.SubElement(disk, "prop")
        prop_mount.set("id", "mount")
        prop_mount.set("value", "/")

    # Add the cloud compute service hosts
    cloud_comment1 = ET.Comment(" The host on which the cloud compute service will run ")
    zone.append(cloud_comment1)
    cloud_head_host = ET.SubElement(zone, "host")
    cloud_head_host.set("id", "CloudHeadHost")
    cloud_head_host.set("speed", "10Gf")
    cloud_head_host.set("core", "1")

    cloud_disk = ET.SubElement(cloud_head_host, "disk")
    cloud_disk.set("id", "hard_drive")
    cloud_disk.set("read_bw", "100MBps")
    cloud_disk.set("write_bw", "100MBps")

    cloud_prop_size = ET.SubElement(cloud_disk, "prop")
    cloud_prop_size.set("id", "size")
    cloud_prop_size.set("value", "5000GiB")

    cloud_prop_mount = ET.SubElement(cloud_disk, "prop")
    cloud_prop_mount.set("id", "mount")
    cloud_prop_mount.set("value", "/scratch/")

    cloud_comment2 = ET.Comment(" The host on which the cloud compute service will start VMs ")
    zone.append(cloud_comment2)
    cloud_host = ET.SubElement(zone, "host")
    cloud_host.set("id", "CloudHost")
    cloud_host.set("speed", "25Gf")
    cloud_host.set("core", "8")

    cloud_ram_prop = ET.SubElement(cloud_host, "prop")
    cloud_ram_prop.set("id", "ram")
    cloud_ram_prop.set("value", "16GB")
    # Pretty print the XML
    pretty_xml = prettify(platform)

    # Add the XML declaration and DOCTYPE
    xml_declaration = "<?xml version='1.0'?>\n<!DOCTYPE platform SYSTEM \"https://simgrid.org/simgrid.dtd\">\n"
    full_xml = xml_declaration + pretty_xml

    # Write the full XML to the output file
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
