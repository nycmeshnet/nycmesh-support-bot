import os
from dotenv import load_dotenv
from supportbot.utils.diagnostics_report import get_report, lbe_traceroute_report, generate_uisp_section
from supportbot.utils.uisp_data import get_uisp_devices_by_nn
import pytest
import sys
from distutils.util import strtobool

load_dotenv()
on_mesh = strtobool(os.environ.get("ON_MESH", default="False"))

@pytest.mark.skipif(not on_mesh or sys.platform == "win32", reason="not on mesh or on windows")
def test_get_report_lbe_only():
    report = get_report(690)
    print(report)

@pytest.mark.skipif(not on_mesh or sys.platform == "win32", reason="not on mesh or on windows")
def test_get_report_omni_install():
    report = get_report(344)
    print(report)

@pytest.mark.skipif(not on_mesh or sys.platform == "win32", reason="not on mesh or on windows")
def test_lbe_traceroute_report():
    report = lbe_traceroute_report('10.96.182.236')
    print(report)

@pytest.mark.skipif(not on_mesh, reason="not on mesh or on windows")
def test_generate_uisp_section():
    nn = 136
    devices = get_uisp_devices_by_nn(nn)
    report = generate_uisp_section(devices)
    print(report)

if __name__ == "__main__":
    test_generate_uisp_section()
