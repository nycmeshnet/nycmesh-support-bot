import json


def confrimation_dialog_block_kit(channel_id, message_ts, user_id):
    return {
        "type": "modal",
        "callback_id": "manually_run_diagnostics",
        "private_metadata": json.dumps({
            'channel': channel_id,
            'ts': message_ts,
            'user': user_id
        }),
        "title": {
            "type": "plain_text",
            "text": "Run node diagnostics?",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
            "emoji": True
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Are you sure you would like to run diagnostics for this message? This will "
                            f"cause the support bot look up <@{user_id}>'s network number and connect to "
                            "their node to provide diagnostic information. "
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "The bot will respond in-thread with the diagnostic information"
                    }
                ]
            }
        ]
    }