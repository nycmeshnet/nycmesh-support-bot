import requests
import json
from dotenv import load_dotenv
import os
import re
from datetime import datetime

load_dotenv()

def get_uisp_devices():
    response = requests.get("https://uisp.mesh.nycmesh.net/nms/api/v2.1/devices", headers={'x-auth-token': os.environ.get('UISP_AUTH_TOKEN')}, verify=False)

    devices = json.loads(response.content)

    if devices == []:
        raise ValueError('Problem downloading UISP devices.')

    return devices

def nn_from_uisp_name(uisp_name):
    matches = re.findall("(?:^|-)(\d{1,})(?:-|$)", uisp_name)
    if not matches:
        return None

    return int(matches[0])

def filter_devices_by_nn(devices, nn):
    filtered_devices = []
    for device in devices:
        try:
            name = device['identification']['displayName']
            uisp_nn = nn_from_uisp_name(name)
            if uisp_nn == nn:
                filtered_devices.append(device)
        except:
            pass
    return filtered_devices

def get_uisp_devices_by_nn(nn):
    devices = filter_devices_by_nn(get_uisp_devices(), nn)
    if len(devices) == 0:
        return None
    return devices

def human_readable_uisp_time(uisp_time_string):
    date_object = datetime.fromisoformat(uisp_time_string.replace("Z", "+00:00"))
    human_time_string = date_object.strftime("%Y-%m-%d %H:%M:%S")
    return human_time_string
