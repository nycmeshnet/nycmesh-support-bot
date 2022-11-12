#!/bin/bash

# Read .env file
# Stolen from https://gist.github.com/mihow/9c7f559807069a03e302605691f85572?permalink_comment_id=3625310#gistcomment-3625310
set -a
source <(cat .env | sed -E 's/(\s+=\s*)|(\s*=\s+)/=/g' | sed -e '/^#/d;/^\s*$/d' -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g")
set +a

echo "=====Node Stats====="
echo


# input network number from shell
echo "Network Number: $1";

# test if input is a number under 8000

if (( $1 )) 2>/dev/null; then
  if (( $1 > 8000 )) ; then
    echo "FATAL: Network numbers are below 8000."
    exit
  fi
else
  echo "FATAL: Input is not a number."
  exit
fi

# convert number to ip octets

nn=$1;

ipfourthoctet=$(($nn%100));
ipthirdoctet=$((($nn-$ipfourthoctet)/100));
meship="10.69."$ipthirdoctet"."$ipfourthoctet;

echo "Mesh IP: $meship";

# ping and traceroute to host, set reachable flag

echo
echo "=====Ping/Trace====="
echo

ping -c 1 $meship > /dev/null;

if (( $? == 0 )); then
  latency=$(ping -c 4 $meship | tail -1 | awk '{print $4}' | cut -d '/' -f 2);
  echo Router is reachable with a latency of $latency milliseconds.
  echo
  traceroute $meship;
  reachable=1
else
  echo Router is unreachable. Some tests cannot be performed.
  reachable=0
fi

if (( $reachable == 0 )); then
  echo Skipping device-side statistics...
else

echo
echo "=====Omni Interfaces====="
echo

# print interfaces on host

interfaces=$(sshpass -p$OMNI_PASS ssh -o StrictHostKeyChecking=no admin@$meship /interface print);
echo "$interfaces";

# speed test from host to sn3

echo
echo ====="Omni Speed Test"=====
echo
speedtest=$(sshpass -p$OMNI_PASS ssh -o StrictHostKeyChecking=no admin@$meship /tool speed-test test-duration=5 10.69.7.13);
echo "$speedtest" | grep done -A 8

fi

# get device info from searching nn in uisp

echo
echo "=====UISP Stats====="
echo

uispgrab=$(/app/bin/nycmesh-tool uisp devices getDevices --x-auth-token "$NYCMESH_TOOL_AUTH_TOKEN" 2>/dev/null | jq '.[]');
devices=$(echo $uispgrab | jq 'select(.identification.name | match("'$nn'"))');

#echo "$devices";

count=0;
OFS="$IFS"
IFS=$','
for row in $(echo "$devices" | jq -r '"\(.identification.name),\(.identification.site.name),\(.overview.signal),\(.overview.downlinkCapacity),\(.overview.uplinkCapacity),"'); do
if (( $count == 0 )); then count=1; fi
if (( $count == 1 )); then echo "Name: $row";
elif (( $count == 2 )); then echo "Location: $row";
elif (( $count == 3 )) && (( $row != 'null')); then echo "Signal: $row";
elif (( $count == 4 )) && (( $row != 'null')); then echo "Downlink: $(($row/1000000)) Mbps";
elif (( $count == 5 )) && (( $row != 'null')); then echo "Uplink: $(($row/1000000)) Mbps";
elif (( $count == 6 )); then count=1; echo; echo $row; fi
count=$(($count+1));
done
IFS="$OFS"

if (($count == 0 )); then
  echo No devices found containing $nn in name.
fi

echo
echo EOF
