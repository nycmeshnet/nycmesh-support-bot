import json
import requests
from supportbot.utils.user_data import MeshUser

class OsTicketClient():
    def __init__(self, api_key):
        self.api_header_open = {'X-API-Key':api_key}
        self.api_header_close_reopen = {'apikey':api_key}

    def open_ticket(self, name, email, subject, message):

        data = {
            'ip': '99.99.99.99', #value required for osTicket IP authentication
            'name': name, 
            'email': email, 
            'subject': 'Follow-up-bot: ' + name,
            'message': message #TODO: add slack_thread_link
            }
        data_json = json.dumps(data)

        r = requests.post(
            'https://devsupport.nycmesh.net/api/http.php/tickets.json', 
            data=data_json, 
            headers=self.api_header_open
            )

        return r
    
    def get_parameters(self, ticket_id, status_id=None, message=''):
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
        return parameters
    
    def close_ticket(self, ticket_id, message):
        close_status_id = 3
        parameters = self.get_parameters(ticket_id, status_id=close_status_id, message=message)
        data = {
            'query': 'ticket',
            'condition': 'close',
            'parameters': parameters
            }
        data_json = json.dumps(data)

        r = requests.post(
            'https://devsupport.nycmesh.net/ost_wbs/?', 
            data=data_json, 
            headers=self.api_header_close_reopen
            )

        return r

    
    def reopen_ticket(self, ticket_id, message):
        reopen_status_id = 1
        parameters = self.get_parameters(ticket_id, status_id=reopen_status_id, message=message)
        data = {
            'query': 'ticket',
            'condition': 'close',
            'parameters': parameters
            }
        
        data_json = json.dumps(data)

        r = requests.post(
            'https://devsupport.nycmesh.net/ost_wbs/?', 
            data=data_json, 
            headers=self.api_header_close_reopen
            )
        
        return r
    

def open_user_ticket(os_ticket_client: OsTicketClient, user_id, app):
    user = MeshUser(app, user_id, None)
    message = f'Member requested support in #support channel.'
    response = os_ticket_client.open_ticket(user.full_name, user.email, 'Message dialog input', 'Test Message')

    return response

