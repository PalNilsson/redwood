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
from typing import Optional, Dict


def prettify(elem: ET.Element) -> str:
    """
    Return a pretty-printed XML string for the Element.

    :param elem: XML element (ET.Element)
    :return: pretty-printed XML string (str).
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_string = reparsed.toprettyxml(indent="    ")  # Four spaces indentation
    # Remove the XML declaration added by minidom
    lines = pretty_string.split('\n')
    pretty_lines = []
    for line in lines:
        if line.strip() and not line.startswith('<?'):
            pretty_lines.append(line)
            # Add an empty line after each host element and comment
            if line.strip().startswith('</host>') or line.strip().startswith('</zone>') or line.strip().startswith(
                    '</link>'):
                pretty_lines.append('')

    return '\n'.join(pretty_lines).strip()


def add_host_with_comment(
        zone: ET.Element,
        comment_text: str,
        host_id: str,
        speed: str,
        core: str,
        props: Optional[Dict[str, str]] = None,
        disk_props: Optional[Dict[str, Dict[str, str]]] = None
):
    """
    Add a host element with an associated comment to the zone.

    :param zone: The parent XML element to which the host is added (ET.Element)
    :param comment_text: The text of the comment to add before the host (str)
    :param host_id: The ID of the host (str)
    :param speed: The speed of the host (str)
    :param core: The number of cores of the host (str)
    :param props: Additional properties for the host. Defaults to None (Optional[Dict[str, str]], optional)
    :param disk_props: Properties for the nested disk element. Defaults to None (Optional[Dict[str, Dict[str, str]]], optional)
    """
    comment = ET.Comment(comment_text)
    zone.append(comment)

    host = ET.SubElement(zone, "host")
    host.set("id", host_id)
    host.set("speed", speed)
    host.set("core", core)

    if props:
        for prop_id, prop_value in props.items():
            prop = ET.SubElement(host, "prop")
            prop.set("id", prop_id)
            prop.set("value", prop_value)

    if disk_props:
        disk = ET.SubElement(host, "disk")
        for disk_prop_id, disk_prop_value in disk_props.items():
            disk.set(disk_prop_id, disk_prop_value)
        for prop_id, prop_value in disk_props["props"].items():
            prop = ET.SubElement(disk, "prop")
            prop.set("id", prop_id)
            prop.set("value", prop_value)


def add_route(zone: ET.Element, src: str, dst: str):
    """
    Add a route element to the zone.

    :param zone: The parent XML element to which the route is added (ET.Element)
    :param src: The source of the route (str)
    :param dst: The destination of the route (str)
    """
    route = ET.Element("route")
    route.set("src", src)
    route.set("dst", dst)
    link_ctn = ET.SubElement(route, "link_ctn")
    link_ctn.set("id", "network_link")
    zone.append(route)


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
    add_host_with_comment(
        zone,
        " The host on which the Controller will run ",
        "UserHost",
        "10Gf",
        "1"
    )

    # Generate the specified number of ComputeHosts
    for i in range(1, num_fields + 1):
        add_host_with_comment(
            zone,
            f" Another host on which the bare-metal compute service will be able to run jobs ",
            f"ComputeHost{i}",
            "35Gf",
            "10",
            {"ram": "16GB"}
        )

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

    # Add the network link
    network_comment = ET.Comment(" A network link shared by EVERY ONE ")
    zone.append(network_comment)
    network_link = ET.SubElement(zone, "link")
    network_link.set("id", "network_link")
    network_link.set("bandwidth", "50MBps")
    network_link.set("latency", "1ms")

    #
    network_comment = ET.Comment(" The same network link connects all hosts together ")
    zone.append(network_comment)

    # Add routes for each compute host
    for i in range(1, num_fields + 1):
        route = ET.Element("route")
        route.set("src", "UserHost")
        route.set("dst", f"ComputeHost{i}")
        link_ctn = ET.SubElement(route, "link_ctn")
        link_ctn.set("id", "network_link")
        # Append the route directly to the zone element
        zone.append(route)

    # Add routes for each storage host
    for i in range(1, num_fields + 1):
        route = ET.Element("route")
        route.set("src", "UserHost")
        route.set("dst", f"StorageHost{i}")
        link_ctn = ET.SubElement(route, "link_ctn")
        link_ctn.set("id", "network_link")
        # Append the route directly to the zone element
        zone.append(route)

    # Add route for the cloud head host
    route = ET.Element("route")
    route.set("src", "UserHost")
    route.set("dst", "CloudHeadHost")
    link_ctn = ET.SubElement(route, "link_ctn")
    link_ctn.set("id", "network_link")
    # Append the route directly to the zone element
    zone.append(route)

    # Add routes from compute to storage hosts
    for i in range(1, num_fields + 1):
        route = ET.Element("route")
        route.set("src", f"ComputeHost{i}")
        route.set("dst", f"StorageHost{i}")
        link_ctn = ET.SubElement(route, "link_ctn")
        link_ctn.set("id", "network_link")
        # Append the route directly to the zone element
        zone.append(route)

    # Add route from cloud head to cloud host
    route = ET.Element("route")
    route.set("src", "CloudHeadHost")
    route.set("dst", "CloudHost")
    link_ctn = ET.SubElement(route, "link_ctn")
    link_ctn.set("id", "network_link")
    # Append the route directly to the zone element
    zone.append(route)

    # Add routes from storage hosts to cloud host
    for i in range(1, num_fields + 1):
        route = ET.Element("route")
        route.set("src", f"StorageHost{i}")
        route.set("dst", "CloudHost")
        link_ctn = ET.SubElement(route, "link_ctn")
        link_ctn.set("id", "network_link")
        # Append the route directly to the zone element
        zone.append(route)

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
