import os
from dotenv import load_dotenv

from supportbot.utils import user_data
from slack_bolt import App

load_dotenv()

# # commented out until we have a system for creating test users
# def test_network_number():
#     app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
#     user = user_data.MeshUser(app, 'U03TK054116', 'Xf03SY3N2RD2')
#     nn = user.network_number
#     print(nn)

# if __name__ == '__main__':
#     test_network_number()