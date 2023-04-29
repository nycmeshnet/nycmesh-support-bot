import requests
import json
from dotenv import load_dotenv
import os
import re

load_dotenv()

def get_uisp_devices():
    response = requests.get("https://uisp.mesh.nycmesh.net/nms/api/v2.1/devices", headers={'x-auth-token': os.environ.get('NYCMESH_TOOL_AUTH_TOKEN')}, verify=False)

    devices = json.loads(response.content)

    if devices == []:
        raise ValueError('Problem downloading UISP devices.')

    return devices

def nn_from_uisp_name(uisp_name):
    matches = re.findall("(?:^|-)(\d{3,})(?:-|$)", uisp_name)
    if not matches:
        return None

    return int(matches[0])

def filter_devices_by_nn(devices, nn):
    filtered_devices = []
    for device in devices:
        try:
            name = device['identification']['displayName']
            nn = nn_from_uisp_name(name)
            if nn:
                filtered_devices.append(device)
        except:
            pass
    return filtered_devices