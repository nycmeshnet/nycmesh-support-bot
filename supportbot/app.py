import json
from functools import partial

from slack_bolt import App

from supportbot.request_handler import handle_support_request
from supportbot.utils.block_kit_templates import confrimation_dialog_block_kit
from supportbot.utils.message_classification import is_in_support_channel, user_needs_help
from slack_bolt.adapter.socket_mode import SocketModeHandler

import os
from dotenv import load_dotenv

load_dotenv()

def run_app(config):
    print("Starting bolt app...")

    app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

    @app.event(
        event={"type": "message", "subtype": None},
        matchers=[
            partial(is_in_support_channel, support_channel_ids=config['channel_ids']),
            user_needs_help
        ]
    )
    def respond_to_help_requests(message):
        handle_support_request(app, config, message['user'], message['channel'], message['ts'])

    @app.event("message")
    def handle_message_events():
        """This handler silences warnings about "unhandled" message events"""
        pass

    @app.shortcut("run_node_diagnostics")
    def open_modal(ack, shortcut, client):
        ack()

        resp = client.views_open(
            trigger_id=shortcut["trigger_id"],
            view=confrimation_dialog_block_kit(
                shortcut['channel']['id'],
                shortcut['message_ts'],
                shortcut['message']['user']
            )
        )
        print(resp)

    @app.view("manually_run_diagnostics")
    def modal_submit(ack, body, client, view, logger):
        ack()
        metadata = json.loads(view['private_metadata'])
        
        manual_number_input = view['state']['values']['numberInputBlock']['manual_number-action']
        if 'value' in manual_number_input:
            manual_number = manual_number_input['value']
        else:
            manual_number = None

        handle_support_request(app, config, metadata['user'], metadata['channel'], metadata['ts'], manual_number=manual_number)


    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()