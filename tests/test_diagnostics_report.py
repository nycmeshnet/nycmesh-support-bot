import os
from dotenv import load_dotenv
from supportbot.utils.diagnostics_report import get_report

load_dotenv()

# commented out so test doesn't fail off Mesh

# def test_get_uisp_devices():
#     assert len(get_uisp_devices()) > 0

def test_get_report_lbe_only():
    report = get_report(690)
    print(report)

def test_get_report_omni_install():
    report = get_report(344)
    print(report)


if __name__ == '__main__':
    test_get_report_lbe_only()