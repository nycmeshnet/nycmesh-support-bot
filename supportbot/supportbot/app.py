import json
import requests
from functools import partial

from slack_bolt import App

from supportbot.request_handler import handle_support_request
from supportbot.utils.block_kit_templates import confrimation_dialog_block_kit
from supportbot.utils.message_classification import is_in_support_channel, is_first_message_in_thread
from supportbot.utils.user_data import MeshUser
from slack_bolt.adapter.socket_mode import SocketModeHandler
from supportbot.utils.block_kit_templates import confrimation_dialog_block_kit, help_suggestion_dialog_block_kit, help_suggestion_message_block_kit

import os
from dotenv import load_dotenv

from mesh_database_client import DatabaseClient

load_dotenv()

def run_app(config):
    print("Starting bolt app...")

    app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

    database_client_cached = DatabaseClient(os.environ.get("SPREADSHEET_ID"))

    @app.shortcut("run_node_diagnostics")
    def open_modal(ack, shortcut, client):
        ack()

        user_id = shortcut['message']['user']
        user = MeshUser(app, user_id, config['nn_property_id'], database_client_cached=database_client_cached)
        nn = user.network_number
        message = shortcut['message']

        resp = client.views_open(
            trigger_id=shortcut["trigger_id"],
            view=confrimation_dialog_block_kit(
                shortcut['channel']['id'],
                message['thread_ts'] if 'thread_ts' in message else message['ts'],
                shortcut['message']['user'],
                nn = nn
            )
        )

    # Manual shorcut button flow

    @app.view("manually_run_diagnostics")
    def submit_manually_run_diagnostics(ack, body, client, view, logger):
        ack()
        metadata = json.loads(view['private_metadata'])
        
        manual_number_input = view['state']['values']['numberInputBlock']['manual_number_input']
        if 'value' in manual_number_input:
            manual_number = manual_number_input['value']
        else:
            manual_number = None

        at_member_input = view['state']['values']['checkboxInputBlock']['at_message_toggle-action']['selected_options']
        if len(at_member_input) > 0:
            at_member = True
        else:
            at_member = False

        handle_support_request(app, config, metadata['user'], metadata['channel'], metadata['ts'], manual_number=manual_number, at_member=at_member)

    # Automated response flow in response to message in Support channel

    @app.event(
        event={"type": "message", "subtype": None},
        matchers=[
            partial(is_in_support_channel, support_channel_ids=config['channel_ids']),
            is_first_message_in_thread
        ]
    )
    def respond_with_help_suggestion(message):
        root_message_ts = message['thread_ts'] if 'thread_ts' in message else message['ts']
        app.client.chat_postEphemeral(
            channel=message['channel'],
            blocks=help_suggestion_message_block_kit(message['channel'], root_message_ts, message['user'])['blocks'],
            text="New support request detected, offering to run supportbot on supported platforms",
            user=message['user'],
            metadata="test"
        )

    @app.action("run_suggestion_button_ok")
    def open_help_suggestion_dialog_block_kit(ack, body, logger):
        ack()

        metadata = json.loads(body['actions'][0]['value'])
        user = MeshUser(app, metadata['user'], config['nn_property_id'], database_client_cached=database_client_cached)
        nn = user.network_number

        app.client.views_open(
            trigger_id=body["trigger_id"],
            view=help_suggestion_dialog_block_kit(
                metadata['channel'],
                metadata['ts'],
                metadata['user'],
                nn = nn
            )
        )

        requests.post(body['response_url'], json = {
            'response_type': 'ephemeral',
            'text': '',
            'replace_original': True,
            'delete_original': True
        })

    @app.action("run_suggestion_button_no")
    def run_suggestion_button_no(ack, body, logger):
        ack()

        requests.post(body['response_url'], json = {
            'response_type': 'ephemeral',
            'text': '',
            'replace_original': True,
            'delete_original': True
        })


    @app.view("run_suggestion_submit_ok")
    def submit_run_request(ack, body, client, view, logger):
        ack()
        metadata = json.loads(view['private_metadata'])
        manual_number_input = view['state']['values']['numberInputBlock']['manual_number_input']
        if 'value' in manual_number_input:
            manual_number = manual_number_input['value']
        else:
            manual_number = None
        handle_support_request(app, config, metadata['user'], metadata['channel'], metadata['ts'], manual_number=manual_number, at_member = False)


    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()