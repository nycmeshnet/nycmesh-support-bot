import os

from mesh_database_client import DatabaseClient
from dotenv import load_dotenv
import re
import json

load_dotenv()

class MeshUser:
    def __init__(self, app, user_id, network_number_property_id, manual_number=None):
        self._app = app
        self.user_id = user_id
        self._fetched = False
        self._network_number_property_id = network_number_property_id
        self._database_client = DatabaseClient(os.environ.get("SPREADSHEET_ID"))
        self._manual_number = manual_number

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

        # user entered manual input
        if self._manual_number:
            manual_nn = self._database_client.get_nn(int(self._manual_number))
            if manual_nn is not None:
                return manual_nn

        slack_nn = self._profile.get('fields', {}).get(self._network_number_property_id, None)

        # slack property nn / install number
        if slack_nn and (validated_slack_nn := self._database_client.get_nn(int(slack_nn['value']))):
            return validated_slack_nn

        # slack name nn / install number
        slack_name_combined =  f"{self._profile['real_name']} {self._profile['display_name']}"
        name_nn_embeded_list = re.findall("(\d{3,})", slack_name_combined)

        if name_nn_embeded_list and (validated_name_nn_embeded := self._database_client.get_nn(name_nn_embeded_list[0])):
            return validated_name_nn_embeded

        # email nn lookup
        email_nn = self._database_client.email_to_nn(self.email)
        if email_nn is not None:
            return int(email_nn)

        # name nn lookup
        name_nn = self._database_client.name_to_nn(self.full_name)
        if name_nn is not None:
            return int(name_nn)

        # We haven't found a network number
        return None
