import os
from webbrowser import get

from mesh_database_client import MeshDBDatabaseClient
from supportbot.utils.diagnostics_report import upload_report_file, get_report
from supportbot.utils.user_data import MeshUser
import subprocess
from supportbot.utils.block_kit_templates import confrimation_dialog_block_kit, help_suggestion_message_block_kit
from slack_bolt import App

def nn_to_map_url(nn):
    base = 'https://www.nycmesh.net/map/nodes/'
    return f'<{base}-{nn}|NN{nn}>'


def handle_support_request(app, config, user_id, channel_id, message_ts, manual_number=None):
    database_client = MeshDBDatabaseClient(os.environ.get("MESHDB_AUTH_TOKEN"))
    user = MeshUser(app, user_id, config['nn_property_id'], database_client=database_client)

    network_number = None
    if manual_number:
        manual_nn = database_client.get_nn(int(manual_number))
        if manual_nn:
            network_number = manual_nn
            text = (
                f"The network number entered was {nn_to_map_url(network_number)}" +
                (f" (via install #{manual_number})" if int(manual_number) != int(network_number) else "") +
                f". Diagnostic report running..."
            )
        else:
            text = (
                f"Entered number: {manual_number} could not be found. Please check the number is a "
                f"valid install or network number and try again"
            )
    else:
        if user.network_number:
            network_number = user.network_number
            text = (
                f"The network number {nn_to_map_url(user.network_number)} was automatically detected. "
                f"Diagnostic report running..."
            )
        else:
            text = (
                "The Install Number could not be automatically determined.  You can find your "
                "Install Number by searching the registered email for the Subject "
                "\"NYC Mesh Rooftop Install.\"  Providing this number will help volunteers locate "
                "your number in our system to better assist you."
            )

    app.client.chat_postMessage(
        channel=channel_id,
        thread_ts=message_ts,
        text=text
    )

    if network_number:
        try:
            report_text = get_report(network_number)

            upload_report_file(app, report_text, channel_id, message_ts, network_number, "Here's a diagnostics report to help our volunteers:")
        except Exception as e:
            app.client.chat_postMessage(
                channel=channel_id,
                thread_ts=message_ts,
                text="An error was encountered while attempting to run diagnostics. Please try again later."
            )
            raise e
