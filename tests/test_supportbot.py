import multiprocessing
import time
import os
from dotenv import load_dotenv

from supportbot.app import run_app

load_dotenv()

def test_env():
    assert os.environ.get("SLACK_BOT_TOKEN") and os.environ.get("SLACK_APP_TOKEN")

if __name__ == '__main__':
    test_env()