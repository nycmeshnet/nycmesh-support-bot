from webbrowser import get
from supportbot.utils.diagnostics_report import upload_report_file, get_report
from supportbot.utils.user_data import MeshUser
import subprocess

def handle_support_request(app, config, user_id, channel_id, message_ts, manual_number=None, at_member = True):
    user = MeshUser(app, user_id, config['nn_property_id'], manual_number=manual_number)

    if at_member:
        text = f"This is a reply to <@{user_id}>! It looks like your email is {user.email} {'and' if user.network_number else 'but'} your network number {'is ' + str(user.network_number) if user.network_number else 'could not be found'}. {'Here is a diagnostics report to help our volunteers:' if user.network_number else ''}"
    else:
        text = f"Member email is {user.email} {'and' if user.network_number else 'but'} the network number {'is ' + str(user.network_number) if user.network_number else 'could not be found'}. {'Here is a diagnostics report to help our volunteers:' if user.network_number else ''}"

    app.client.chat_postMessage(
        channel=channel_id,
        thread_ts=message_ts,
        text=text
    )

    if user.network_number:
        report = get_report(user.network_number)

        upload_report_file(app, report, channel_id, message_ts, user.network_number)