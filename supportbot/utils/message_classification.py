
def is_in_support_channel(message, support_channel_ids):
    return message['channel'] in support_channel_ids


def user_needs_help(message):
    return 'help' in message['text']
