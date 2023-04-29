import os
from dotenv import load_dotenv
from supportbot.utils.uisp_data import nn_from_uisp_name, get_uisp_devices

load_dotenv()

# commented out so test doesn't fail off Mesh
# def test_get_uisp_devices():
#     assert len(get_uisp_devices()) > 0

def test_nn_from_uisp_name():
    assert nn_from_uisp_name("lbe-5134-diy-455") == 5134
    assert nn_from_uisp_name("lbe-5134") == 5134
    assert nn_from_uisp_name("5134-lbe") == 5134

if __name__ == "__main__":
    test_nn_from_uisp_name()