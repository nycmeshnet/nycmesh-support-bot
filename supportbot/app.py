import json
from functools import partial

from slack_bolt import App

from supportbot.request_handler import handle_support_request
from supportbot.utils.block_kit_templates import confrimation_dialog_block_kit
from supportbot.utils.message_classification import is_in_support_channel, is_first_message
from slack_bolt.adapter.socket_mode import SocketModeHandler
from supportbot.utils.block_kit_templates import confrimation_dialog_block_kit, help_suggestion_dialog_block_kit, help_suggestion_message_block_kit


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
            is_first_message
        ]
    )
    def respond_to_help_suggestion(message):
        # app.client.chat_postEphemeral not working
        print(f"thread ts: {message['ts']}")
        print(f"message['channel']: {message['channel']}")
        print(f"message['user']: {message['user']}")
        app.client.chat_postMessage(
            channel=message['channel'],
            thread_ts=message['ts'],
            blocks=help_suggestion_message_block_kit["blocks"],
            user=message['user'],
            text="New support request detected, offering to run supportbot on supported platforms",
        )

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

    @app.action("run_suggestion_button")
    def submit_run_request(ack, body, logger):
        ack()
        resp = app.client.views_open(
            trigger_id=body["trigger_id"],
            view=help_suggestion_dialog_block_kit(
                body['channel']['id'],
                body['message']['ts'],
                body['user']['id']
            )
        )

    @app.view("run_suggestion_submit")
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