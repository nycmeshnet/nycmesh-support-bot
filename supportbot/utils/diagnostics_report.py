import datetime


def upload_report_file(app, report_txt, channel_id, thread_id, network_number):
    timestamp = datetime.datetime.now()
    response = app.client.files_upload(
        channels=channel_id,
        content=report_txt,
        filetype='txt',
        filename=f"diagnostics_{network_number}_{timestamp.strftime('%Y-%m-%dT%H:%M:%S')}.txt",
        title=f"Diagnostics Report - NN {network_number} on {timestamp.strftime('%Y-%m-%d at %I:%M %p')}",
        thread_ts=thread_id
    )
    return response['file']['id']
