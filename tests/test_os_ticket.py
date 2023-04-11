from supportbot.utils.os_ticket import OsTicketClient 
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OS_TICKET_API_KEY")
os_ticket_client = OsTicketClient(api_key=api_key)

def open_sample_ticket():
    name = 'Jason Howard'
    email = 'jason3@jasonhoward.org'
    subject = 'test subject 2'
    message = 'test ticket'

    r = os_ticket_client.open_ticket(name, email, subject, message)

    return r

def test_open_ticket():
    r = open_sample_ticket()

    # print response
    print(r) #response code
    print(r.text) #new ticketID

def test_close_ticket():
    ticket_id = open_sample_ticket().text
    print(f'ticket_id: {ticket_id}')

    message = 'test close ticket'

    r = os_ticket_client.close_ticket(ticket_id, message)

    # print response
    print(r) #response code
    print(r.text) #new ticketID

def test_reopen_ticket():

    ticket_id = open_sample_ticket().text
    print(f'ticket_id: {ticket_id}')
    # os_ticket_client.close_ticket(ticket_id, 'test close ticket')
    
    # message = 'test reopen ticket'
    # r = os_ticket_client.reopen_ticket(ticket_id, message)

    # print response
    # print(r) #response code
    # print(r.text) #new ticketID

if __name__ == '__main__':
    test_open_ticket()