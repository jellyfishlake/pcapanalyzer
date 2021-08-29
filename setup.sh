#!/bin/bash


pip install pandas jinja2 pycaret xhtml2pdf argparse datetime
wget https://tranalyzer.com/download/tranalyzer/tranalyzer2-0.8.11lmw2.tar.gz
tar xzf tranalyzer2-0.8.11lmw2.tar.gz
./$(ls -d */ | grep tranalyzer)setup.sh -T -e

cat <<EOT >> ~/.bashrc
if [ -f "$PWD/$(ls -d */ | grep tranalyzer)scripts/t2_aliases" ]; then
    . "$PWD$(ls -d */ | grep tranalyzer)scripts/t2_aliases"
fi
EOT
