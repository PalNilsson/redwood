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
and convert it to a JSON file (`number_of_cpus.json`). Specifically, the data was extracted by querying the number of
job slots. The maximum number of slots used during six months was then found by the script. Note that this
script is currently not used, in favor of using the corepower and number of cores per queue instead.
3. <b>Combined data</b>: `combined.py`: Combine GFLOPS, number of CPUs and RSE info into one file. The total GFLOPS
number is calculated by multiplying the known total core power (`corepower.json` from the ATLAS benchmarking campaign)
per queue, with the total number of cores (`queue_corecount.json` from pilot jobs, extracted from job records). The
core power is the average benchmark per core for a queue. It is not however proportional to GFLOPS, but is the best
measurement we have using real data. The script also combines the RSE info from the Rucio transfer metrics
(`queues_and_rses.json`). The script produces the file `queues-corepower_based.json`.
4. <b>Consistency</b>: `verify.py`: Verify the consistency of the data in the `queues-corepower_based.json` file. The
script verifies that are "GFLOPS" and "RSE" entries for all queues in the file. The script also calculates the number
of queues.

