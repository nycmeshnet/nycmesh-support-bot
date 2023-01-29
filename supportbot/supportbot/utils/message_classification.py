
def is_in_support_channel(message, support_channel_ids):
    return message['channel'] in support_channel_ids

def is_first_message_in_thread(message):
    return not 'thread_ts' in message.keys()

def user_needs_help(message):
    return 'help test' in message['text']
