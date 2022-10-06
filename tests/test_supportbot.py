import multiprocessing
import time
import os
from dotenv import load_dotenv

from supportbot.app import run_app
from supportbot.utils.diagnostics_report import get_report

load_dotenv()

def test_env():
    assert os.environ.get("SLACK_BOT_TOKEN") and os.environ.get("SLACK_APP_TOKEN")

def test_get_report():
    get_report(458)

if __name__ == '__main__':
    test_get_report()