import logging
import os

from mesh_database_client import MeshDBDatabaseClient
from dotenv import load_dotenv
import re

load_dotenv()

class MeshUser:
    def __init__(self, app, user_id, network_number_property_id, database_client=None):
        self._app = app
        self.user_id = user_id
        self._fetched = False
        self._network_number_property_id = network_number_property_id
        if database_client:
            self._database_client = database_client
        else:
            self._database_client = MeshDBDatabaseClient(os.environ.get("MESHDB_AUTH_TOKEN"))

    def _fetch_profile(self):
        if self._fetched:
            return

        logging.info(f"Fetching user profile for user: {self.user_id}")
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
        logging.info(f"Attempting to find an NN for {self.user_id}")
        self._fetch_profile()

        slack_nn_raw = self._profile.get('fields', {}).get(self._network_number_property_id, None)
        if slack_nn_raw:
            logging.info(f"Found NN text ({slack_nn_raw}) in user's slack profile: {self.user_id}. Validating...")
            slack_nn_matches = re.findall("(\d{3,})", slack_nn_raw['value'])

            # slack property nn / install number
            if slack_nn_matches and (validated_slack_nn := self._database_client.get_nn(int(slack_nn_matches[0]))):
                logging.info(f"Validated NN, using this as a placeholder: {self.user_id}")
                return validated_slack_nn

        # slack name nn / install number
        slack_name_combined =  f"{self._profile['real_name']} {self._profile['display_name']}"
        name_nn_embeded_list = re.findall("(\d{3,})", slack_name_combined)

        logging.info(f"Checking name for embedded numbers: {slack_name_combined}")
        if name_nn_embeded_list and (validated_name_nn_embeded := self._database_client.get_nn(name_nn_embeded_list[0])):
            logging.info(f"Found number {validated_name_nn_embeded} in slack profile name")
            return validated_name_nn_embeded

        # email nn lookup
        logging.info(f"Looking up NN in database by email: {self.email}")
        email_nn = self._database_client.email_to_nn(self.email)
        logging.debug(f"Heard back from database client")
        if email_nn is not None:
            logging.info(f"Found NN for email {self.email}: {email_nn}")
            return int(email_nn)

        # name nn lookup
        logging.info(f"Looking up NN in database by name: {self.full_name}")
        name_nn = self._database_client.name_to_nn(self.full_name)
        logging.debug(f"Heard back from database client")
        if name_nn is not None:
            logging.info(f"Found NN for name {self.full_name}: {name_nn}")
            return int(name_nn)

        # We haven't found a network number
        logging.info(f"Couldn't find an NN for {self.user_id}")
        return None
