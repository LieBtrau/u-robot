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

from calendar import month
import configparser
import logging
import sys
import datetime
from tzlocal import get_localzone
from exchangelib import OAuth2Credentials, DELEGATE, Account, Configuration, Identity


def main(argv):
    config = configparser.RawConfigParser()
    config.read('example.cfg')
    username = str(config.get('Section1', 'UserName'))

    credentials = OAuth2Credentials(
        client_id=str(config.get('Section1', 'client_id')),
        client_secret = str(config.get('Section1', 'client_secret')),
        tenant_id=str(config.get('Section1', 'tenant_id')),
        identity=Identity(primary_smtp_address=username)
    )

    config = Configuration(server='outlook.office365.com', credentials=credentials)

    test_account = Account(
        primary_smtp_address = username,
        config = config,
        autodiscover = False,
        access_type = DELEGATE
    )

    start = datetime.datetime.now(get_localzone())
    items = test_account.calendar.view(
        start=start,
        end=start + datetime.timedelta(weeks=4),
    )
    for item in items:
        print(item.start, item.end, item.subject)



if __name__ == '__main__':
    # Setup
    logging.basicConfig(
        level=logging.INFO,
        format=('[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s'),
        handlers=[
            logging.FileHandler('debug.log'),
            logging.StreamHandler(sys.stdout),
        ]
    )
    main(sys.argv[1:])
