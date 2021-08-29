#!/bin/bash
packetcapture=$(echo $1)

targetdir="/home/basti/.anaconda3/envs/bathesis_development/project"
flowben="flows_benign"
flowmalw="flows_malware"
pcapben="pcaps_benign"
pcapmalw="pcaps_malware"

T2HOME="/home/basti/Software/tranalyzer2-0.8.9"

alias tawk='/home/basti/Software/tranalyzer2-0.8.9/scripts/tawk/tawk'

alias t2='tranalyzer'
	tranalyzer ()
	{ 
	    local _t2="$(_find_t2)";
	    if [ -z "$_t2" ]; then
	        _build_t2;
	        _t2="$(_find_t2)";
	        [ -z "$_t2" ] && return 1;
	    fi;
	    "$_t2" "$@"
	}

_find_t2 ()
{ 
    local _t2=($(find "$T2HOME/tranalyzer2" -type f -name tranalyzer));
    if [ "${#_t2[@]}" -le 1 ]; then
        echo "$_t2";
    else
        echo "$(ls -t1 "${_t2[@]}" | head -1)";
    fi
}

_build_t2 ()
{ 
    local _t2="$1";
    if [ ! -f "$_t2" ]; then
        printf "\e[1;33m'tranalyzer'\e[0;33m executable does not exist... build it (Y/n)?\e[0m ";
        local ans;
        read ans;
        case "$ans" in 
            [Nn] | [Nn][Oo])
                return 1
            ;;
            *)

            ;;
        esac;
        $T2HOME/tranalyzer2/autogen.sh || return 1;
        tput clear;
    fi
}


echo "Preprocess packet capture..."
# Create flows from packet captures
t2 -r $packetcapture -w .
echo $packetcapture


# Extract Features 
for i in $(ls .); do
  if [[ $i =  *"flows.txt" ]]; then
  echo $i
  tawk '{ $timeFirst = utc($timeFirst); $timeLast = utc($timeLast); print $fname,$timeFirst,$timeLast,$duration,$srcIP,$dstIP,$srcPort,$dstPort,$l4Proto,$dstPortClass,$numPktsSnt,$numPktsRcvd,$numBytesSnt,$numBytesRcvd,$minPktSz,$maxPktSz,$avePktSize,$stdPktSize,$aveIAT,$stdIAT,$pktps,$bytps,$httpHosts,$httpMimes,$httpUsrAg,$dnsAname,$sslServerName }' ./$i | tawk 'json()' >> ./data_tmp.json
  fi
done

cat ./data_tmp.json | tr -d '[]' | sed 's/},/}/g' | sed 's/}/},/g' | sed -r '/^\s*$/d' | sed '1s/^/[/' | sed '$ s/.$//' | sed -r '$a]' > ./data

rm *.txt
rm *.json
rm *.xer
rm *.bin
rm *pcapd.pcap

mv data data.json








