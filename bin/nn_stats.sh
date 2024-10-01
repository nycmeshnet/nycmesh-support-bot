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
  if (( $1 < 0 )) ; then
    echo "FATAL: Network numbers are greater than 0."
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
  echo Traceroute from $meship to 10.10.10.100
  sshpass -p $OMNI_PASS ssh -o StrictHostKeyChecking=no admin@$meship tool traceroute 10.10.10.100 count=1 use-dns=yes
  reachable=1
else
  echo Router is unreachable. Some tests cannot be performed.
  reachable=0
fi

if (( $reachable == 0 )); then
  echo Skipping device-side statistics...
else

echo
echo ====="Omni Speed Test"=====
echo Speedtest from $meship to 10.10.10.100
echo
speedtest=$(sshpass -p$OMNI_PASS ssh -o StrictHostKeyChecking=no admin@$meship /tool speed-test test-duration=5 10.10.10.100);
echo "$speedtest" | grep done -A 8

echo
echo "=====Omni Interfaces====="
echo

interfaces=$(sshpass -p$OMNI_PASS ssh -o StrictHostKeyChecking=no admin@$meship /interface print);
echo "$interfaces";


fi
