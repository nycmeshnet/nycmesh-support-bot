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
from numpy import sqrt

load_dotenv()


class DatabaseClient:
    def __init__(self, spreadsheet_id=None, include_active=False):
        self.spreadsheet_id = spreadsheet_id
        if self.spreadsheet_id is None:
            self.spreadsheet_id = os.environ.get("SPREADSHEET_ID")

        SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        # created in Google Cloud admin
        SERVICE_ACCOUNT_FILE = "credentials.json"

        credentials_dict = self._get_sheets_credentials_from_env()
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict
        )
        self.service = build("sheets", "v4", credentials=credentials)

        # Call the Sheets API
        self.sheet = self.service.spreadsheets()

        self.signup_df = self.get_signup_df()
        self.links_df = self.get_links_df()

        if include_active:
            self.active_node_df = self.get_active_node_df()
            self.active_link_df = self.get_active_link_df()

    def _get_sheets_credentials_from_env(self):
        try:
            credentials_mapping = {
                "type": "GOOGLE_SHEETS_TYPE",
                "project_id": "GOOGLE_SHEETS_PROJECT_ID",
                "private_key_id": "GOOGLE_SHEETS_PRIVATE_KEY_ID",
                "private_key": "GOOGLE_SHEETS_PRIVATE_KEY",
                "client_email": "GOOGLE_SHEETS_CLIEND_EMAIL",
                "client_id": "GOOGLE_SHEETS_CLIENT_ID",
                "auth_uri": "GOOGLE_SHEETS_AUTH_URI",
                "token_uri": "GOOGLE_SHEETS_TOKEN_URI",
                "auth_provider_x509_cert_url": "GOOGLE_SHEETS_AUTH_PROVIDER_X509_CERT_URL",
                "client_x509_cert_url": "GOOGLE_SHEETS_CLIENT_509_CERT_URL",
            }

            credentials = {}
            for key, value in credentials_mapping.items():
                credentials[key] = os.environ.get(value)

            credentials["private_key"] = credentials["private_key"].replace("\\n", "\n")

            return credentials
        except Exception as e:
            print(e)
            raise ValueError("Problem parsing Google Sheets credentials")

    def get_range_as_df(self, range):
        result = (
            self.sheet.values()
            .get(spreadsheetId=self.spreadsheet_id, range=range)
            .execute()
        )
        values = result.get("values", [])

        df = pd.DataFrame(values[1:], columns=values[0])
        return df

    def get_signup_df(self):
        df = self.get_range_as_df("Form Responses 1!A:AP")

        # force columns to be specific type
        df["NN"] = pd.to_numeric(df["NN"], errors="coerce").fillna(0).astype(int)
        df["ID"] = pd.to_numeric(df["ID"], errors="coerce").fillna(0).astype(int)

        df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
        df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

        df["installDate"] = pd.to_datetime(df["installDate"], errors="coerce")

        df.drop(df.tail(1).index, inplace=True)

        return df

    def get_links_df(self):
        df = self.get_range_as_df("Links!A:I")

        # force columns to be specific type
        df["to"] = pd.to_numeric(df["to"], errors="coerce").fillna(0).astype(int)
        df["from"] = pd.to_numeric(df["from"], errors="coerce").fillna(0).astype(int)

        return df

    def get_active_node_df(self):
        df = self.signup_df.copy()
        df = df.sort_values(by=["installDate"])
        df = df[df["Status"].isin(["Installed", "NN assigned"])]
        df = df[df["NN"] != 0]
        df = df.drop_duplicates(subset="NN", keep="first")

        return df

    def get_active_link_df(self):
        df = self.links_df.copy()

        columns_list = list(df.columns)
        columns_list[6] = "to_nn"
        columns_list[7] = "from_nn"

        df.columns = columns_list

        df["to"] = df["to_nn"]
        df["from"] = df["from_nn"]

        df["to"] = pd.to_numeric(df["to"], errors="coerce").fillna(0).astype(int)
        df["from"] = pd.to_numeric(df["from"], errors="coerce").fillna(0).astype(int)

        df = df[~df["status"].isin(["dead", "planned"])]

        df = df[(df["to"] != 0) & (df["from"] != 0)]

        # enure only active nodes are in links df
        nns = self.active_node_df["NN"]
        df = df[df["from"].isin(nns) & df["to"].isin(nns)]

        return df

    def name_to_nn(self, name):
        signup_df = self.signup_df
        name_df = signup_df[signup_df["Name"].str.contains(name, case=False)]

        if name_df.empty:
            return None

        entry = name_df.iloc[0]
        if (nn := entry["NN"]) == 0:
            return None
        return nn

    def email_to_nn(self, email):
        # TODO multiple emails recency
        signup_df = self.signup_df
        email_df = signup_df[signup_df["Email"].str.contains(email, case=False)]

        if email_df.empty:
            return None

        entry = email_df.iloc[0]
        if (nn := entry["NN"]) == 0:
            return None
        return nn

    # def address_to_nn(self, address):
    #     signup_df = self.signup_df

    #     geocode_result = self.gmaps.geocode(address)
    #     location = geocode_result[0]['geometry']['location']
    #     lat = location['lat']
    #     lng = location['lng']

    #     deg_to_feet = 288200

    #     lat_diff = abs(signup_df['Latitude']-lat)*deg_to_feet
    #     lng_diff = abs(signup_df['Longitude']-lng)*deg_to_feet
    #     distance = sqrt(lat_diff**2 + lng_diff**2)
    #     signup_df['distance'] = distance
    #     min_distance = distance.min()

    #     # check if closest signup request is further than 200ft
    #     if min_distance > 200:
    #         return None

    #     min_index = distance.idxmin()
    #     closest = signup_df.iloc[min_index]

    #     if closest['NN'] == 0:
    #         return None

    #     return closest['NN']

    def nn_to_linked_nn(self, nn):
        links_df = self.links_df

        from_df = links_df[links_df["from"] == nn]
        to_df = links_df[links_df["to"] == nn]

        from_nns = from_df["to"].tolist()
        to_nns = to_df["from"].tolist()

        connected_nodes = from_nns + to_nns

        return connected_nodes

    def get_nn(self, input_number):
        if input_number is None:
            return None

        input_number = int(input_number)

        id_rows = self.signup_df[self.signup_df["ID"] == input_number]
        for index, row in id_rows.iterrows():
            if row["Status"] == "NN assigned":
                return input_number
            elif row["Status"] == "Installed":
                return row["NN"]

        nn_rows = self.signup_df[self.signup_df["NN"] == input_number]
        for index, row in nn_rows.iterrows():
            if row["Status"] == "Installed":
                return input_number

        return None

    def nn_to_location(self, nn):
        if not isinstance(nn, int):
            raise ValueError("nn must be an integer")
        row = self.signup_df[self.signup_df["NN"] == nn].iloc[0]
        return {"Latitude": row.Latitude, "Longitude": row.Longitude}


if __name__ == "__main__":
    database_client = DatabaseClient(include_active=True)
    name = database_client.name_to_nn("test")
    print(name)
