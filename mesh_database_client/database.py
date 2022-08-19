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
import googlemaps
from dotenv import load_dotenv
from numpy import sqrt

load_dotenv()

class DatabaseClient:

    def __init__(self, spreadsheet_id = None):

        if spreadsheet_id is None:
            self.spreadsheet_id = os.environ.get("SPREADSHEET_ID")
        else:
            self.spreadsheet_id = spreadsheet_id

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

        self.process_signup_df()
        self.process_links_df()

        # drop last signup_df column which does not contain data
        self.signup_df.drop(self.signup_df.tail(1).index,inplace=True)

        self.gmaps = googlemaps.Client(key=os.environ.get("MAPS_API"))

    def get_range_as_df(self, range):
        result = self.sheet.values().get(spreadsheetId=self.spreadsheet_id,range=range).execute()
        values = result.get('values', [])
        
        df = pd.DataFrame(values[1:], columns = values[0])
        return df

    def process_signup_df(self):
        df = self.signup_df
 
        # force columns to be specific type
        df['NN'] = (pd.to_numeric(df['NN'], errors="coerce")
                         .fillna(0)
                         .astype(int))

        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
         
        self.signup_df = df


    def process_links_df(self):
        df = self.links_df

        # force columns to be specific type
        df = df.astype({'to':'float'})
        df = df.astype({'from':'float'})
        df = df.astype({'to':'int'})
        df = df.astype({'from':'int'})
        
        self.links_df = df

    def name_to_nn(self, name):
        signup_df = self.signup_df
        name_df = signup_df[signup_df['Name'].str.contains(name, case=False)]
        if not name_df.empty:
            entry = name_df.iloc[0]
            return entry['NN']
        else:
            return None

    def email_to_nn(self, email):
        # TODO multiple emails recency
        signup_df = self.signup_df
        email_df = signup_df[signup_df['Email'].str.contains(email, case=False)]
        if not email_df.empty:
            entry = email_df.iloc[0]
            return entry['NN']
        else:
            return None

    def deg_to_feet(deg):
        return deg * 288200

    def address_to_nn(self, address):
        signup_df = self.signup_df

        geocode_result = self.gmaps.geocode(address)
        location = geocode_result[0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']

        deg_to_feet = 288200

        lat_diff = abs(signup_df['Latitude']-lat)*deg_to_feet
        lng_diff = abs(signup_df['Longitude']-lng)*deg_to_feet
        distance = sqrt(lat_diff**2 + lng_diff**2)
        signup_df['distance'] = distance
        min_distance = distance.min()

        # check if closest signup request is further than 200ft
        if min_distance > 200:
            return None

        min_index = distance.idxmin()
        closest = signup_df.iloc[min_index]
        return closest['NN']


    def nn_to_linked_nn(self, nn):
        links_df = self.links_df
        
        from_df = links_df[links_df['from']==nn]
        to_df = links_df[links_df['to']==nn]

        from_nns = from_df['to'].tolist() 
        to_nns = to_df['from'].tolist() 

        connected_nodes = from_nns + to_nns

        return connected_nodes

if __name__ == '__main__':
    database_client = DatabaseClient()
    name = database_client.name_to_nn("test")
    print(name)