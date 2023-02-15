import datetime
from pytz import timezone
import subprocess

def upload_report_file(app, report_txt, channel_id, thread_id, network_number):
    timestamp = datetime.datetime.now(tz = timezone('US/Eastern'))
    response = app.client.files_upload(
        channels=channel_id,
        content=report_txt,
        filetype='txt',
        filename=f"diagnostics_{network_number}_{timestamp.strftime('%Y-%m-%dT%H:%M:%S')}.txt",
        title=f"Diagnostics Report - NN {network_number} on {timestamp.strftime('%Y-%m-%d at %I:%M %p')}",
        thread_ts=thread_id
    )
    return response['file']['id']

def get_report(nn):
    command = ['nn_stats.sh', str(nn)]
    result = subprocess.run(command, capture_output=True, text=True).stdout
    return result