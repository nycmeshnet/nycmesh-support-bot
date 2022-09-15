from supportbot.utils.diagnostics_report import upload_report_file
from supportbot.utils.user_data import MeshUser


def handle_support_request(app, config, user_id, channel_id, message_ts):
    user = MeshUser(app, user_id, config['nn_property_id'])

    app.client.chat_postMessage(
        channel=channel_id,
        thread_ts=message_ts,
        text=f"This is a reply to <@{user_id}>! It looks like "
             f"your email is {user.email} {'and' if user.network_number else 'but'} your network number "
             f"{'is ' + str(user.network_number) if user.network_number else 'could not be found'}. "
             f"Here's a diagnostics report to help our volunteers:",
    )

    if user.network_number:
        upload_report_file(app, "DATA\n" * 43, channel_id, message_ts, user.network_number)