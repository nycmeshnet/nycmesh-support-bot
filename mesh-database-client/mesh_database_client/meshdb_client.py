from __future__ import print_function

import os

from dotenv import load_dotenv

load_dotenv()

import requests
from mesh_database_client import endpoints
from mesh_database_client.database import DatabaseClient


class MeshDBDatabaseClient(DatabaseClient):
    def __init__(self, mesh_db_auth_token):
        self.requests_sesssion = requests.Session()
        self.requests_sesssion.headers['Authorization'] = f"Token {mesh_db_auth_token}"

    def _member_id_to_nn(self, member_id):
        install_query_response = self.requests_sesssion.get(
            endpoints.INSTALL_LOOKUP_ENDPOINT,
            params={"member": member_id, "status": "Active"},
        )
        install_query_response.raise_for_status()
        install_query_json = install_query_response.json()

        if not install_query_json["results"]:
            return None

        # If there are multiple active installs for this member, arbitrary select the first one
        install = install_query_json["results"][0]

        if not install["network_number"]:
            return None

        return install["network_number"]

    def name_to_nn(self, name):
        member_query_response = self.requests_sesssion.get(
            endpoints.MEMBER_LOOKUP_ENDPOINT, params={"name": name}
        )
        member_query_response.raise_for_status()
        member_query_json = member_query_response.json()

        if not member_query_json["results"]:
            return None

        # If there are multiple members with this name, arbitrary select the first member
        member_id = member_query_json["results"][0]["id"]
        return self._member_id_to_nn(member_id)

    def email_to_nn(self, email):
        member_query_response = self.requests_sesssion.get(
            endpoints.MEMBER_LOOKUP_ENDPOINT, params={"email_address": email}
        )
        member_query_response.raise_for_status()
        member_query_json = member_query_response.json()

        if not member_query_json["results"]:
            return None

        # If there are multiple members with this email, arbitrary select the first member. This
        # should not be common, member objects are deduplicated on email address
        member_id = member_query_json["results"][0]["id"]
        return self._member_id_to_nn(member_id)

    def get_nn(self, input_number):
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
            endpoints.INSTALL_LOOKUP_ENDPOINT,
            params={"network_number": input_number, "status": "Active"},
        )
        install_num_query_response.raise_for_status()
        install_num_query_json = install_num_query_response.json()

        if install_num_query_json["results"]:
            # We found an install for this as an install number, translate that to an NN
            return install_num_query_json["results"][0]["network_number"]

        return None


if __name__ == "__main__":
    database_client = MeshDBDatabaseClient(os.environ.get("MESHDB_AUTH_TOKEN"))
    nn = database_client.name_to_nn("Brian Hall")
    print(nn)
