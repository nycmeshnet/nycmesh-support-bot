from functools import partial

from slack_bolt import App

from supportbot.utils.credentials import load_credentials
from supportbot.utils.diagnostics_report import upload_report_file
from supportbot.utils.message_classification import is_in_support_channel, user_needs_help
from slack_bolt.adapter.socket_mode import SocketModeHandler

from supportbot.utils.user_data import MeshUser


def run_app(config):
    print("Starting bolt app...")

    slack_credentials = load_credentials(config['credentials_path'])
    app = App(token=slack_credentials["SLACK_BOT_TOKEN"])
    SocketModeHandler(app, slack_credentials["SLACK_APP_TOKEN"]).start()

    @app.event(
        event={"type": "message", "subtype": None},
        matchers=[
            partial(is_in_support_channel, support_channel_ids=config['channel_ids']),
            user_needs_help
        ]
    )
    def respond_to_help_requests(message):
        user = MeshUser(app, message['user'], config['nn_property_id'])

        app.client.chat_postMessage(
            channel=message['channel'],
            thread_ts=message['ts'],
            text=f"This is a reply to <@{message['user']}>! It looks like "
                 f"your email is {user.email} {'and' if user.network_number else 'but'} your network number "
                 f"{'is ' + user.network_number if user.network_number else 'could not be found'}. "
                 f"Here's a diagnostics report to help our volunteers:",
        )

        upload_report_file(app, "DATA\n" * 43, message['channel'], message['ts'], user.network_number)

    @app.event("message")
    def handle_message_events():
        """This handler silences warnings about "unhandled" message events"""
        pass
