import json
import requests

class OsTicketClient():
    def __init__(self, api_key):
        self.api_header = {'X-API-Key':api_key}

    def open_ticket(self, name, email, subject, message):

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
            headers=self.api_header
            )

        return r
    
    def get_parameters(self, ticket_id, status_id, message):
        parameters = {
            'ticket_id': ticket_id,
            'body':f'<p>{message}</p>',
            'staff_id':3,
            'status_id':status_id,
            'team_id':1,
            'dept_id':1,
            'topic_id':1,
            'username':'Test User1'
            }
    
    def close_ticket(self, ticket_id, message):
        close_status_id = 3
        parameters = self.get_parameters(ticket_id, close_status_id, message)
        data = {
            'query': 'ticket',
            'condition': 'close',
            'parameters': parameters
            }
        data_json = json.dumps(data)

        r = requests.post(
            'https://devsupport.nycmesh.net/ost_wbs/?', 
            data=data_json, 
            headers=self.api_header
            )

        return r

    
    def reopen_ticket(self, ticket_id, message):
        reopen_status_id = 1
        parameters = self.get_parameters(ticket_id, 1, message)
        data = {
            'query': 'ticket',
            'condition': 'close',
            'parameters': parameters
            }
        
        data_json = json.dumps(data)

        r = requests.post(
            'https://devsupport.nycmesh.net/ost_wbs/?', 
            data=data_json, 
            headers=self.api_header
            )
        
        return r