import supportbot.app
import click

from supportbot.constants import DEFAULT_CHANNEL_IDS, DEFAULT_CREDENTIALS_PATH, DEFAULT_NETWORK_NUMBER_PROPERTY_ID


@click.command()
@click.option('--credentials', default=DEFAULT_CREDENTIALS_PATH, help="Path to credentials JSON file")
@click.option(
    '--channel-ids',
    default=DEFAULT_CHANNEL_IDS,
    help="The Slack ID number for the channel to run the bot in"
)
@click.option(
    '--nn-property-id',
    default=DEFAULT_NETWORK_NUMBER_PROPERTY_ID,
    help="The Slack ID number for the user property containing their network number"
)
def main(credentials, channel_ids, nn_property_id):
    supportbot.app.run_app({
        'credentials_path': credentials,
        'channel_ids': channel_ids,
        'nn_property_id': nn_property_id
    })


if __name__ == "__main__":
    main()