# Machine Learning Packet Capture Analyzer
This is an approach to analyze and identify malicious traffic in packet captures utilizing Machine Learning algorithms 👨‍💻
:dancer: :coffee:

# Install

##

The setup comes with with a small install script.

> `sh setup.sh`

## Tranalyzer
Tranalyzer is a powerful tool to extract useful information from packet captures like the raw .pcap format.

## System

The tool was tested on `Ubuntu 20.04 LTS` having Python 3.8 environment installed.
We assume CentOS/Fedora/Red Hat distributions and more should work as well as long Python3.8 is installed.

# Usage

After setup is done, now you should be able to run following commands from the CLI

> `python3.8 predict.py --loadmodel ./model.h5 --pcap sample.pcap`
