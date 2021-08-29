# Machine Learning Packet Capture Analyzer
In context of a bachelor thesis this is an approach to analyze and identify malicious traffic in packet captures utilizing Machine Learning algorithms. 
The project primary goal was to contribute digital forensic community and their investigators 👨‍💻 :coffee:. The idea behind this approach was to deal with Big Data
related challenges during digital forensic investigations.

# Install

The setup comes with with a small install script but some packets like pip and git are required for pre-setup.

> `sudo apt-get install python3-pip git -y` </br>

It is recommendend to switch to a virtual environment to not interfere with current environment.

> `sudo pip3 install virtualenv` </br>
> `virtualenv -p /usr/bin/python3.8 venv` </br>
> `source venv/bin/activate`

Then execute the following commands. Please note, that installing Tranalyzer will be installed on the system.

> `git clone https://github.com/jellyfishlake/pcapanalyzer.git` </br>
> `cd pcapanalyzer` </br>
> `sh setup.sh`

## Dependencies
The most important dependency is the powerful [Tranalyzer](https://tranalyzer.com/about#theanteater) tool. It is able to extract lot of useful information from packet captures 
like the raw .pcap format. Tranalyzer will help to read packet capture and extract informations in a way, so that it is 
processable by Machine Learning algorithms.

## System

The tool was tested on `Ubuntu 20.04.03 LTS` having `Python 3.8` environment installed.
We assume that older versions and other distributions should work as well as long Python3(.8) is installed.

# Usage

After setup is done, now you should be able to run following commands from the CLI

> `python predict.py --loadmodel ./model.h5 --pcap sample.pcap`
