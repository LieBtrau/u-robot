#!/usr/bin/env python3
#
# Authentication to Microsoft 365:
#   - Basic authentication (username/password) is being deprecated in favor of OAuth-tokens
#   - For using OAuth, this application must first be registered with Azure Active Directory
#
# References:
#   https://docs.microsoft.com/en-us/exchange/client-developer/exchange-web-services/how-to-authenticate-an-ews-application-by-using-oauth
#   https://ecederstrand.github.io/exchangelib/#oauth-authentication
#   https://docs.microsoft.com/en-us/exchange/client-developer/exchange-web-services/how-to-control-access-to-ews-in-exchange
#
# Further references and examples:
# https://github.com/ecederstrand/exchangelib/issues/566
# https://stackoom.com/en/question/3icko
#
# Installation:
# pip install exchangelib
#

import configparser
import logging
import sys
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
    # Print first 100 inbox messages in reverse order
    for item in test_account.inbox.all().order_by('-datetime_received')[:100]:
        print(item.subject)


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
