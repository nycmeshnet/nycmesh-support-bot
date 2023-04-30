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

def is_lbe(device):
    return 'lbe' in device['identification']['displayName'].lower()

def is_ubiquity(device):
    try:
        return device['identification']['vendor'] == 'Ubiquiti'
    except:
        return False

def lbe_only(devices):
    if len(devices) == 1 and is_lbe(devices[0]):
        return True
    return False

def cidr_to_ip(cidr):
    return cidr.split('/')[0]

def get_ubiquity_device_description(device):
    return f"""
IP: {cidr_to_ip(device['ipAddress'])}
Last seen: {human_readable_uisp_time(device['overview']['lastSeen'])}
Signal: {device['overview']['signal']} DBm
Downlink: {device['overview']['downlinkCapacity']/1000000} mbps
Uplink: {device['overview']['uplinkCapacity']/1000000} mbps
Status: {device['overview']['status']}
Outage score: {device['overview']['outageScore']}"""
    
def get_commmon_device_description(device):
    return f"""
Name: {device['identification']['displayName']}
Location: {device['identification']['site']['name']}"""
        

def generate_uisp_section(devices):
    uisp_outputs = [
        '\n\n=====UISP Stats=====',
        'Warning: UISP stats polled infrequently, may be out of date.',
        ]
    for device in devices:
        uisp_output = get_commmon_device_description(device)
 
        if is_ubiquity(device):
            uisp_output += f'{get_ubiquity_device_description(device)}'

        uisp_outputs.append(uisp_output)

    return '\n'.join(uisp_outputs)

def ping_report(ip):
    report = '=====Ping/Trace=====\n\n'
    command = ['ping', '-c', '1', ip]
    report += subprocess.run(command, capture_output=True, text=True).stdout

    return report

def get_report(nn):
    
    report = ''

    devices = get_uisp_devices_by_nn(nn)

    if lbe_only(devices):
        report += f'NN {nn} is an LBE only site, some details will be omitted.\n\n'
        report += ping_report(cidr_to_ip(devices[0]['ipAddress']))
    else:
        command = ['nn_stats.sh', str(nn)]
        # report += subprocess.run(command, capture_output=True, text=True).stdout
        report += "test section"

    report += generate_uisp_section(devices)
    return report