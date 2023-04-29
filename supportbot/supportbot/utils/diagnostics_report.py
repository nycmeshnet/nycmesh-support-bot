import datetime
from pytz import timezone
import subprocess
from supportbot.utils.uisp_data import get_uisp_devices_by_nn, human_readable_uisp_time

def upload_report_file(app, report_txt, channel_id, thread_id, network_number, initial_comment):
    timestamp = datetime.datetime.now(tz = timezone('US/Eastern'))
    response = app.client.files_upload(
        channels=channel_id,
        content=report_txt,
        filetype='txt',
        filename=f"diagnostics_{network_number}_{timestamp.strftime('%Y-%m-%dT%H:%M:%S')}.txt",
        title=f"Diagnostics Report - NN {network_number} on {timestamp.strftime('%Y-%m-%d at %I:%M %p')}",
        thread_ts=thread_id,
        initial_comment=initial_comment
    )
    return response['file']['id']

def lbe_only(devices):
    names = [x['identification']['displayName'].lower() for x in devices]
    if len(names) == 1 and 'lbe' in ' '.join(names):
        return True
    return False

def get_report(nn):
    
    devices = get_uisp_devices_by_nn(nn)

    if lbe_only(devices):
        device = devices[0]
        device_name = device['identification']['displayName']
        ip = device['ipAddress'].split('/')[0]
        last_seen = human_readable_uisp_time(device['overview']['lastSeen'])
        # signal
        # uptime
        return f'This node is LBE only, some diagnostics information is not available.\ndevice name: {device_name}\nip: {ip}\nlast seen (polls infrequently): {last_seen}'

    command = ['nn_stats.sh', str(nn)]
    result = subprocess.run(command, capture_output=True, text=True).stdout
    return result