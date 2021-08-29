#!/bin/bash

# Variables
tran=$(ls -d */ | grep tranalyzer)
taw="$(ls -d */ | grep tranalyzer)scripts/tawk/tawk"
t2="$tran/tranalyzer2/build/tranalyzer"

# Extract Flows
$t2 -r $1 -w ./

# Preprocess Tranalyzer output
$taw '{ $timeFirst = utc($timeFirst); $timeLast = utc($timeLast); print $timeFirst,$timeLast,$duration,$srcIP,$dstIP,$srcPort,$dstPort,$l4Proto,$dstPortClass,$numPktsSnt,$numPktsRcvd,$numBytesSnt,$numBytesRcvd,$minPktSz,$maxPktSz,$avePktSize,$stdPktSize,$aveIAT,$stdIAT,$pktps,$bytps,$httpHosts,$httpMimes,$httpUsrAg,$dnsAname,$sslServerName }' $(ls *_flows.txt) | $taw 'json()' >> ./data_tmp.json

# Each line is in json format. This puts all line to one json file
cat ./data_tmp.json | tr -d '[]' | sed 's/},/}/g' | sed 's/}/},/g' | sed -r '/^\s*$/d' | sed '1s/^/[/' | sed '$ s/.$//' | sed -r '$a]' > ./data

# Cleanup
rm *.txt
rm *.json

# Rename
mv data data.json








