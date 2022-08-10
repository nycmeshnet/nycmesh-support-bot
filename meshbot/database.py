from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseClient:

    def __init__(self):

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        # created in Google Cloud admin
        SERVICE_ACCOUNT_FILE = 'credentials.json'

        signup_sheet_range = 'Form Responses 1!A:AO'
        links_sheet_range = 'Links!A:I'

        CREDS = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        self.service = build('sheets', 'v4', credentials=CREDS)

        # Call the Sheets API
        self.sheet = self.service.spreadsheets()

        # load all data into dataframe
        self.signup_df = self.get_range_as_df(signup_sheet_range)
        self.links_df = self.get_range_as_df(links_sheet_range)

        # drop last signup_df column which does not contain data
        self.signup_df.drop(self.signup_df.tail(1).index,inplace=True)

    def get_range_as_df(self, range):
        SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
        result = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=range).execute()
        values = result.get('values', [])
        
        df = pd.DataFrame(values, columns = values[0])
        return df

    def name_to_nn(self, name):
        signup_df = self.signup_df
        name_df = signup_df[signup_df['Name'].str.contains(name, case=False)]
        if not name_df.empty:
            entry = name_df.iloc[0]
            return entry['NN']
        else:
            return None

    def email_to_nn(self, email):
        signup_df = self.signup_df
        email_df = signup_df[signup_df['Email'].str.contains(email, case=False)]
        if not email_df.empty:
            entry = email_df.iloc[0]
            return entry['NN']
        else:
            return None

    def address_to_nn(self, address):
        signup_df = self.signup_df
        address_df = signup_df[signup_df['Location'].str.contains(address, case=False)]
        if not address_df.empty:
            entry = address_df.iloc[0]
            return entry['NN']
        else:
            return None

if __name__ == '__main__':
    database_client = DatabaseClient()
    name = database_client.name_to_nn("Fedor Garin")
    print(name)