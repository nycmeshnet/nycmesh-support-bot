# close.py

import sys
import json
import requests
import urllib3
from collections import Mapping

header = {'apikey':'DB481236E4F361F4FA2F2EA92312FE07'}
ticketID = 15885
parameters = {
    'ticket_id': ticketID,
    'body':'<p>Ticket closed. Thank You!</p>',
    'staff_id':3,
    'status_id':3,
    'team_id':1,
    'dept_id':1,
    'topic_id':1,
    'username':'Test User1'
    }
data = {
    'query': 'ticket',
    'condition': 'close',
    'parameters': parameters
    }
data_json = json.dumps(data)

r = requests.post(
    'https://devsupport.nycmesh.net/ost_wbs/?', 
    data=data_json, 
    headers=header
    )

# debug print to file
with open('debug.log', 'w') as f:
    original_stdout = sys.stdout
    sys.stdout = f # Change the standard output to the file we created.
    print(data_json)
    sys.stdout = original_stdout # Reset the standard output to its original value


# print response
print(r) #response code
print(r.text) #new ticketID
