"""A simple example of how to access the Google Analytics API."""

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = Credentials.from_service_account_file(
        key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
            accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(
                accountId=account,
                webPropertyId=property).execute()

            if profiles.get('items'):
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')
    return None


def get_results(service, profile_id):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions within the past seven days.
    return service.data().ga().get(
        ids='ga:' + profile_id,
        start_date='2020-10-01',
        end_date='2020-10-01',
        metrics='ga:users',
        segment='users::condition::ga:deviceCategory==desktop').execute()


def print_results(results):
    # Print data nicely for the user.
    if results:
        print('View (Profile):', results.get('profileInfo').get('profileName'))
        print('Total Sessions:', results.get('rows')[0][0])

    else:
        print('No results found')


def main():
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics']
    key_file_location = r'/Users/loctek/Downloads/glowing-hearth-294204-4863d900237d.json'
    # Authenticate and construct service.
    service = get_service(
        api_name='analytics',
        api_version='v3',
        scopes=scope,
        key_file_location=key_file_location)
    # profile_id = '240528426'
    # data = service.data().ga().get(
    #     ids='ga:' + profile_id,
    #
    # )
    profile_id = '141269146'  # 不是副本权限不足
    # profile_id = '240528426'
    print(profile_id)
    results = get_results(service, profile_id)
    print(results)
    print_results(results)


if __name__ == '__main__':
    main()
