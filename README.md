# REDWOOD

## Introduction

This repository contains scripts related to the REDWOOD project.

The project is a collaboration between BNL,ORNL, SLAC, University of Massachusetts,
University of Pittsburgh, and Carnegie Mellon University. The five-year project is funded by US DOE ASCR.

Note: Extracts from the PanDA DB, Grafana, Rucio transfer metrics and other data are not included in this repository,
but can be made available upon request.

## Scripts

The scripts listed in this section are used to process or extract data relevant to the project.

1. <b>Connections</b>: `process_connections.py`: This script processes the connections data from a JSON metrics file.
The script reads the transfer metrics data from the JSON file, produced by Rucio, and generates another JSON file
(`combined_connections.json`) that contains the connections and their bandwidths. Typically the metrics data is
downloaded once per week. The script can loop over multiple metrics files.
2. <b>Number of CPUs</b>: `number_of_cpus.py`: Extract the number of CPUs from a CSV file, copied from Grafana,
and convert it to a JSON file (`number_of_cpus.json`). The Grafana data used in this study, contains the number of CPUs
used by the PanDA pilot jobs.