# REDWOOD

## Introduction

This repository contains scripts related to the REDWOOD project.

The project is a collaboration between BNL,ORNL, SLAC, University of Massachusetts,
University of Pittsburgh, and Carnegie Mellon University. The five-year project is funded by US DOE ASCR.

## Scripts

The scripts listed in this section are used to process or extract data relevant to the project.

1. `process_connections.py`: This script processes the connections data from the Rucio metrics file.
The script reads the transfer metrics data from a JSON file, produced by Rucio, and generates another JSON file that
contains the connections and their bandwidths. Typically the metrics data is downloaded once per week. The script can
loop over multiple metrics files.
2. ..