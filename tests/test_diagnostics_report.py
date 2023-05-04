import os
from dotenv import load_dotenv
from supportbot.utils.diagnostics_report import get_report, lbe_traceroute_report
import pytest
import sys

load_dotenv()
on_mesh = os.environ.get("ON_MESH")

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