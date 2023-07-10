import os
from dotenv import load_dotenv
from supportbot.utils.uisp_data import nn_from_uisp_name, get_uisp_devices
import pytest
from distutils.util import strtobool

load_dotenv()
on_mesh = strtobool(os.environ.get("ON_MESH"))

@pytest.mark.skipif(not on_mesh, reason="Not on mesh")
def test_get_uisp_devices():
    assert len(get_uisp_devices()) > 0

def test_nn_from_uisp_name():
    assert nn_from_uisp_name("lbe-5134-diy-455") == 5134
    assert nn_from_uisp_name("lbe-5134") == 5134
    assert nn_from_uisp_name("5134-lbe") == 5134
    assert nn_from_uisp_name("nycmesh-lbe-136") == 136

if __name__ == "__main__":
    test_nn_from_uisp_name()