import json

def get_default_nn_element_field(possible_nn):
    element = {
        "type": "number_input",
        "is_decimal_allowed": False,
        "action_id": "manual_number_input"
    }

    if possible_nn is None:
        return element
    else:
        element |= {'initial_value': str(possible_nn)}
        return element
    

def confrimation_dialog_block_kit(channel_id, message_ts, user_id, nn=None):

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
                    "text": f"Are you sure you would like to run diagnostics for this message? This will cause the support bot to connect to <@{user_id}>'s node to provide diagnostic information. "
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
            },
            {
            "type": "input",
            'optional': False,
            "block_id": "numberInputBlock",
            "element": get_default_nn_element_field(nn),
            "label": {
                "type": "plain_text",
                "text": "NN or Install Number:",
                "emoji": True
            }
            },
            {
                "type": "input",
                'optional': True,
                "block_id": "checkboxInputBlock",
                "element": {
                    "type": "checkboxes",
                    "action_id": "at_message_toggle-action",
                    "initial_options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Yes, @ member",
                                "emoji": True
                            },
                            "value": "at_message_checkbox"
                        }
                    ],
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Yes, @ member",
                                "emoji": True
                            },
                            "value": "at_message_checkbox"
                        }
                    ]
                },
                "label": {
                    "type": "plain_text",
                    "text": "@ member from original message?",
                    "emoji": True
                }
            }
        ]
    }

def help_suggestion_message_block_kit(channel_id, message_ts, user_id):
    return {
        "blocks": [
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "It looks like you are requesting support.  Would you like to run an automated diagnostics report to assist our volunteers?"
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Run report"
                        },
                        "style": "primary",
                        "value": 
                            json.dumps({
                                'channel': channel_id,
                                'ts': message_ts,
                                'user': user_id
                            }),
                        "action_id": "run_suggestion_button_ok",
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "No thanks"
                        },
                        "action_id": "run_suggestion_button_no",
                    },
                ]
            },
        ]
    }

def help_suggestion_dialog_block_kit(channel_id, message_ts, user_id, nn=None):

    return {
        "type": "modal",
        "callback_id": "run_suggestion_submit_ok",
        "private_metadata": json.dumps({
            'channel': channel_id,
            'ts': message_ts,
            'user': user_id
        }),
        "title": {
            "type": "plain_text",
            "text": "Run node diagnostics",
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
        "blocks": [{
            "type": "input",
            'optional': True,
            "block_id": "numberInputBlock",
            "element": get_default_nn_element_field(nn),
            "label": {
                "type": "plain_text",
                "text": "Node Number or Install Number:",
                "emoji": True
            }},
        ]
    }