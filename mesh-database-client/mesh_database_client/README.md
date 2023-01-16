## Updating packages
[pipreqs](https://pypi.org/project/pipreqs/) can be used to update packages.

## Testing
Testing uses Pytest.  A `.env` file with all values in the `Sheets database` section is required.

### Testing Database
The .env file contains the id of a testing database.  Although sensitive user content has been removed we should keep it secret until we consult with the original database creators.  Addresses (without appartment number) have been left in since they are already public on the map and add useful context.  All tests (public code) use fully anonymized values/rows.  