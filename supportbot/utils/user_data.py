import os

from mesh_database_client import DatabaseClient
from dotenv import load_dotenv

load_dotenv()

class MeshUser:
    def __init__(self, app, user_id, network_number_property_id):
        self._app = app
        self.user_id = user_id
        self._fetched = False
        self._network_number_property_id = network_number_property_id
        self._database_client = DatabaseClient(os.environ.get("SPREADSHEET_ID"))

    def _fetch_profile(self):
        if self._fetched:
            return

        resp = self._app.client.users_profile_get(user=self.user_id)
        self._profile = resp.data['profile']


        self.fetched = True

    @property
    def email(self):
        self._fetch_profile()
        return self._profile['email']

    @property
    def full_name(self):
        self._fetch_profile()
        return self._profile['real_name_normalized']

    @property
    def network_number(self):
        self._fetch_profile()

        slack_network_number = self._profile.get('fields', {}).get(self._network_number_property_id, None)
        if slack_network_number:
            return int(slack_network_number['value'])

        email_network_number = self._database_client.email_to_nn(self.email)
        if email_network_number is not None:
            return int(email_network_number)

        name_network_number = self._database_client.name_to_nn(self.full_name)
        if name_network_number is not None:
            return int(name_network_number)

        # We haven't found a network number, return None
        return None
