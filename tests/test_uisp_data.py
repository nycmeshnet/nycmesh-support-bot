import os
from datetime import timedelta

from dateutil import tz
from dotenv import load_dotenv
from supportbot.utils.uisp_data import nn_from_uisp_name, get_uisp_devices, human_readable_uisp_time
import pytest
from distutils.util import strtobool

load_dotenv()
on_mesh = strtobool(os.environ.get("ON_MESH", default="False"))

@pytest.mark.skipif(not on_mesh, reason="Not on mesh")
def test_get_uisp_devices():
    assert len(get_uisp_devices()) > 0

def test_nn_from_uisp_name():
    assert nn_from_uisp_name("lbe-5134-diy-455") == 5134
    assert nn_from_uisp_name("lbe-5134") == 5134
    assert nn_from_uisp_name("5134-lbe") == 5134
    assert nn_from_uisp_name("nycmesh-lbe-136") == 136
    assert nn_from_uisp_name("nycmesh-19-omni") == 19
    assert nn_from_uisp_name("nycmesh-3-omni") == 3

def test_uisp_time_is_converted_to_nyc():
    assert human_readable_uisp_time(
        "2024-03-01T13:50:06Z",
        tz.tzoffset("EDT", timedelta(hours=-4))
    ) == "2024-03-01 09:50:06"

    assert human_readable_uisp_time(
        "2024-03-01T13:50:06Z",
        tz.tzoffset("EST", timedelta(hours=-5))
    ) == "2024-03-01 08:50:06"


if __name__ == "__main__":
    test_nn_from_uisp_name()
