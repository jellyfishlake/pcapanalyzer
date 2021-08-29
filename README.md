# Machine Learning Packet Capture Analyzer
In context of a bachelor thesis this is an approach to analyze and identify malicious traffic in packet captures utilizing Machine Learning algorithms. 
The idea behind this project was to contribute digital forensic community and their investigators. 👨‍💻
:coffee:

# Install

The setup comes with with a small install script. It is recommendend to switch to a virtual environment to not interfere with existing environments.

> `sudo apt-get install python3-pip` <\br>
> `sudo pip3 install virtualenv`
> `virtualenv -p /usr/bin/python3.8 pcapanalyzer`
> `source pcapanalyzer/bin/activate`

Then

> `sh setup.sh`

## Dependencies
The most important dependency is the powerful [Tranalyzer](https://tranalyzer.com/about#theanteater) tool. It is able to extract lot of useful information from packet captures 
like the raw .pcap format. Tranalyzer will help to read packet capture and extract informations in a way, so that it is 
processable by Machine Learning algorithms.

## System

The tool was tested on `Ubuntu 20.04.03 LTS` having `Python 3.8` environment installed.
We assume that older versions and other distributions should work as well as long Python3.8 is installed.

# Usage

After setup is done, now you should be able to run following commands from the CLI

> `python3.8 predict.py --loadmodel ./model.h5 --pcap sample.pcap`
