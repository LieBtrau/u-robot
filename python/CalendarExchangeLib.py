#!/usr/bin/env python3
#
# Authentication to Microsoft 365:
#   - Basic authentication (username/password) is being deprecated in favor of OAuth-tokens
#   - For using OAuth, this application must first be registered with Azure Active Directory
#
# References:
#   https://docs.microsoft.com/en-us/exchange/client-developer/exchange-web-services/how-to-authenticate-an-ews-application-by-using-oauth
#   https://ecederstrand.github.io/exchangelib/#oauth-authentication
#
#
# Installation:
# pip install exchangelib
#
import configparser
from exchangelib import OAuth2Credentials, DELEGATE, Account, Configuration, Identity


class CalendarExchangeLib:
    '''Get calendar data from Microsoft 365 using ExchangeLib library'''

    def __init__(self, config_file):
        config = configparser.RawConfigParser()
        config.read(config_file)
        username = str(config.get('Section1', 'UserName'))

        credentials = OAuth2Credentials(
            client_id=str(config.get('Section1', 'client_id')),
            client_secret=str(config.get('Section1', 'client_secret')),
            tenant_id=str(config.get('Section1', 'tenant_id')),
            identity=Identity(primary_smtp_address=username)
        )

        self.test_account = Account(
            primary_smtp_address=username,
            config=Configuration(server='outlook.office365.com', credentials=credentials),
            autodiscover=False,
            access_type=DELEGATE
        )

    def getCalendarEvents(self, startdate, duration):
        items = self.test_account.calendar.view(start=startdate, end=startdate + duration)
        return items