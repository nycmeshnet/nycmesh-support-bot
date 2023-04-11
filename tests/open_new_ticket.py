# openNewTicket.py

import sys
import json
import requests
import urllib3
from collections import Mapping

#populate these variables 
name    = 'Jason Howard'
email   = 'jason3@jasonhoward.org'
subject = 'test subject'
message = 'test ticket'

headers = {'X-API-Key':'DB481236E4F361F4FA2F2EA92312FE07'}
data = {
    'ip': '99.99.99.99', #value required for osTicket IP authentication
    'name': name, 
    'email': email, 
    'subject': 'NYC Mesh API Test: ' + subject,
    'message': message
    }
data_json = json.dumps(data)

r = requests.post(
    'https://devsupport.nycmesh.net/api/http.php/tickets.json', 
    data=data_json, 
    headers=headers
    )

# debug print to file
#with open('debug.log', 'w') as f:
#    original_stdout = sys.stdout
#    sys.stdout = f # Change the standard output to the file we created.
#    print(data_json)
#    sys.stdout = original_stdout # Reset the standard output to its original value


# print response
print(r) #response code
print(r.text) #new ticketID
