from __future__ import print_function

import logging
import os
from venv import logger

from dotenv import load_dotenv

load_dotenv()

import requests
from mesh_database_client import endpoints
from mesh_database_client.database import DatabaseClient


class MeshDBDatabaseClient(DatabaseClient):
    def __init__(self, mesh_db_auth_token):
        self.requests_sesssion = requests.Session()
        self.requests_sesssion.headers['Authorization'] = f"Token {mesh_db_auth_token}"
        self.logger = logging.Logger("MeshDBClient")

    def _member_id_to_nn(self, member_id):
        self.logger.info(f"Converting member ID: {member_id} to NN")
        install_query_response = self.requests_sesssion.get(
            endpoints.INSTALL_LOOKUP_ENDPOINT,
            params={"member": member_id, "status": "Active"},
        )
        self.logger.debug(
            f"Got response for member ID {member_id}: "
            f"HTTP {install_query_response.status_code}: {install_query_response.text}"
        )
        install_query_response.raise_for_status()
        install_query_json = install_query_response.json()

        if not install_query_json["results"]:
            self.logger.debug(
                f"Found no active installs for member ID {member_id}"
            )
            return None

        # If there are multiple active installs for this member, arbitrary select the first one
        install = install_query_json["results"][0]

        if not install["node"]["network_number"]:
            self.logger.debug(
                f"Install #{install['install_number']} does not have a network number for member ID {member_id}"
            )
            return None

        self.logger.debug(
            f"Found network number: {install['node']['network_number']} for member ID {member_id}"
        )
        return install["node"]["network_number"]

    def name_to_nn(self, name):
        self.logger.info(f"Querying for name {name}")
        member_query_response = self.requests_sesssion.get(
            endpoints.MEMBER_LOOKUP_ENDPOINT, params={"name": name}
        )
        self.logger.debug(f"Got response for name {name}: HTTP {member_query_response.status_code}: {member_query_response.text}")
        member_query_response.raise_for_status()
        member_query_json = member_query_response.json()

        if not member_query_json["results"]:
            self.logger.debug("No results found when searching by name")
            return None

        # If there are multiple members with this name, arbitrary select the first member
        member_id = member_query_json["results"][0]["id"]
        return self._member_id_to_nn(member_id)

    def email_to_nn(self, email):
        self.logger.info(f"Querying for email address {email}")
        member_query_response = self.requests_sesssion.get(
            endpoints.MEMBER_LOOKUP_ENDPOINT, params={"email_address": email}
        )
        self.logger.debug(f"Got response for email {email}: HTTP {member_query_response.status_code}: {member_query_response.text}")
        member_query_response.raise_for_status()
        member_query_json = member_query_response.json()

        if not member_query_json["results"]:
            self.logger.debug("No results found when searching by email")
            return None

        # If there are multiple members with this email, arbitrary select the first member. This
        # should not be common, member objects are deduplicated on email address
        member_id = member_query_json["results"][0]["id"]
        return self._member_id_to_nn(member_id)

    def get_nn(self, input_number):
        try:
            if input_number is None:
                return None

            input_number = int(input_number)

            # Check if this looks like an NN
            nn_query_response = self.requests_sesssion.get(
                endpoints.INSTALL_LOOKUP_ENDPOINT,
                params={"network_number": input_number, "status": "Active"},
            )
            nn_query_response.raise_for_status()
            nn_query_json = nn_query_response.json()

            if nn_query_json["results"]:
                # We found valid installs for this NN, return it to the caller unchanged
                return input_number

            # Hm, this doesn't look like an NN, maybe it's an install number?
            install_num_query_response = self.requests_sesssion.get(
                endpoints.INSTALL_GET_ENDPOINT + str(input_number) + '/'
            )
            install_num_query_response.raise_for_status()
            install_num_query_json = install_num_query_response.json()

            if install_num_query_json["status"] == "Active" and install_num_query_json["node"]:
                # We found an install for this as an install number, translate that to an NN
                return install_num_query_json["node"]["network_number"]

            return None
        except requests.exceptions.RequestException:
            return None


if __name__ == "__main__":
    database_client = MeshDBDatabaseClient(os.environ.get("MESHDB_AUTH_TOKEN"))
    nn = database_client.name_to_nn("Brian Hall")
    print(nn)
