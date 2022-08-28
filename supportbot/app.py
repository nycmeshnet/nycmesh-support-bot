import json
from functools import partial

from slack_bolt import App

from supportbot.request_handler import handle_support_request
from supportbot.utils.credentials import load_credentials
from supportbot.utils.message_classification import is_in_support_channel, user_needs_help
from slack_bolt.adapter.socket_mode import SocketModeHandler


def run_app(config):
    print("Starting bolt app...")

    slack_credentials = load_credentials(config['credentials_path'])
    app = App(token=slack_credentials["SLACK_BOT_TOKEN"])

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
            view={
                "type": "modal",
                "callback_id": "manually_run_diagnostics",
                "private_metadata": json.dumps({
                    'channel': shortcut['channel']['id'],
                    'ts': shortcut['message_ts'],
                    'user': shortcut['message']['user']
                }),
                "title": {
                    "type": "plain_text",
                    "text": "Run node diagnostics?",
                    "emoji": True
                },
                "submit": {
                    "type": "plain_text",
                    "text": "Submit",
                    "emoji": True
                },
                "close": {
                    "type": "plain_text",
                    "text": "Cancel",
                    "emoji": True
                },
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Are you sure you would like to run diagnostics for this message? This will "
                                    f"cause the support bot look up <@{shortcut['message']['user']}>'s network number and connect to "
                                    "their node to provide diagnostic information. "
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": "The bot will respond in-thread with the diagnostic information"
                            }
                        ]
                    }
                ]
            }
        )
        print(resp)

    @app.view("manually_run_diagnostics")
    def modal_submit(ack, body, client, view, logger):
        ack()
        metadata = json.loads(view['private_metadata'])
        handle_support_request(app, config, metadata['user'], metadata['channel'], metadata['ts'])


    SocketModeHandler(app, slack_credentials["SLACK_APP_TOKEN"]).start()
