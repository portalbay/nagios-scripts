#!/bin/bash


dhcp_oid="1.3.6.1.4.1.12356.101.23.2"
ip="$1"
community=$(cat /usr/local/nagios/libexec/.env| grep forti_com | cut -f 2 -d '=' | tr -d \")

pool_percentage=$(/usr/bin/snmpwalk -v2c -c$community $ip $dhcp_oid | /usr/bin/cut -f2 -d ':' )
nag_text_result=""
nag_status_code=0

if [ -z "$pool_percentage"];then
        echo "SNMP ERROR, check setup."
        exit 2
fi

for line in $pool_percentage; do
        if [ $line != "0" ]; then
                nag_text_result="$nag_text_result $line%."
                if [ $line -gt "90" ]; then
                        nag_status_code=2
                elif [ $line -gt "85" ]; then
                        nag_status_code=1
                fi
        fi
done

echo "$nag_text_result Pool Leases Allocated."
exit $nag_status_code

#Return code    Service status
#0      OK
#1      WARNING
#2      CRITICAL
#3      UNKNOWN
#Other  CRITICAL : unknown return code
