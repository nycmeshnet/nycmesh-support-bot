import logging

import supportbot.app
import click

from supportbot.constants import DEFAULT_CHANNEL_IDS, DEFAULT_NETWORK_NUMBER_PROPERTY_ID


@click.command()

@click.option(
    '--channel-ids',
    default=DEFAULT_CHANNEL_IDS,
    help="The Slack ID number for the channel to run the bot in",
    multiple=True
)
@click.option(
    '--nn-property-id',
    default=DEFAULT_NETWORK_NUMBER_PROPERTY_ID,
    help="The Slack ID number for the user property containing their network number"
)
def main(channel_ids, nn_property_id):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)  # Set log level to INFO
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    supportbot.app.run_app({
        'channel_ids': channel_ids,
        'nn_property_id': nn_property_id
    })

if __name__ == "__main__":
    main()