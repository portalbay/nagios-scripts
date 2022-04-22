#!/usr/bin/python

import requests, json
import sys
import base64
from dotenv import load_dotenv
import os

bt_total_license= 2500
bt_percent_WARN = 96
bt_percent_CRIT = 98

#load .env file for API creds
load_dotenv()
beyondtrust_auth = os.getenv('beyondtrust_auth')

#Initial Auth to API
token_url = "https://company_domain_here.beyondtrustcloud.com/oauth2/token"
client_auth_b64 = base64_bytes = base64.b64encode(beyondtrust_auth)

#Simple request to API to pull counts
headers = {"authorization": "Basic " + client_auth_b64}
data = {"grant_type": "client_credentials"}
jsonResponse = requests.post (token_url,headers=headers, json=data).json()
headers = {"authorization": "Bearer " + jsonResponse ["access_token"]}
bt_jmp_count = requests.get("https://company_domain_here.beyondtrustcloud.com/api/config/v1/jump-client?per_page=1&current_page=1" , headers=headers).headers['X-BT-Pagination-Last-Page']


bt_liscense_free = bt_total_license - int(bt_jmp_count)
bt_liscense_percent = int((float(bt_jmp_count) / float(bt_total_license)) * 100)


if bt_liscense_percent < bt_percent_WARN:
    print( "Beyond Trust Liscense Usage: " +  str( bt_liscense_percent) +  "%, " + "Available: " + str(bt_liscense_free)  + ", Used: " + str(bt_jmp_count) )
    sys.exit(0)
elif bt_liscense_percent >= bt_percent_WARN:
    print( "Beyond Trust Liscense WARN: " +  str( bt_liscense_percent) +  "%, " + "Available: " + str(bt_liscense_free)  + ", Used: " + str(bt_jmp_count) )
    sys.exit(1)
elif bt_liscense_percent >= bt_percent_WARN:
    print( "Beyond Trust Liscense CRIT: " +  str( bt_liscense_percent) +  "%, " + "Available: " + str(bt_liscense_free)  + ", Used: " + str(bt_jmp_count) )
    sys.exit(1)

#    sys.exit(0)
#
#Return code    Service status
#0      OK
#1      WARNING
#2      CRITICAL
#3      UNKNOWN
#Other  CRITICAL : unknown return code
