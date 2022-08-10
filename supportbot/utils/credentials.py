import json
import os
import sys

from supportbot.constants import DEFAULT_CREDENTIALS_PATH


def load_credentials(credentials_path=DEFAULT_CREDENTIALS_PATH):
    """
    Load credentials from disk and validate that they contain the appropriate keys
    :return: A `dict` with keys for the `SLACK_APP_TOKEN` and `SLACK_BOT_TOKEN`
    """
    if not os.path.exists(credentials_path):
        print(f"Please provide credentials via {credentials_path} or override search path using --credentials flag")
        sys.exit(10)

    with open(credentials_path, 'r') as credentials_file:
        credentials = json.load(credentials_file)

    if any(key not in credentials or len(credentials[key]) < 50 for key in ['SLACK_APP_TOKEN', 'SLACK_BOT_TOKEN']):
        print(f"Credentials file {credentials_path} invalid, please see README.md for appropriate syntax")
        sys.exit(11)

    return credentials
