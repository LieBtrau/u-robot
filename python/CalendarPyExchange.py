#!/usr/bin/env python3
#
# Info
#	Python Exchange Web services library: https://pyexchange.readthedocs.org/en/latest/
# Installation:
#	sudo apt install espeak libxml2 libxml2-dev libxslt1-dev python3-pip python-dev zlib1g-dev && pip install configparser lxml pyexchange pyserial pyttsx3 tzlocal
#
# This uses NTLM authentication and is for on-premises servers only.  
#   See https://docs.microsoft.com/en-us/exchange/client-developer/exchange-web-services/authentication-and-ews-in-exchange for more information.

from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from datetime import timezone

class CalendarPyExchange:
    '''
    Get calendar data from on-premises Outlook server
    '''
    def __init__(self, config):
        '''
        The following parameters must be present in the config file:
            url -- link to the .asmx file on the exchange server
            username -- your domain name\\username
            password -- password
        '''
        self.url = str(config.get('Section1', 'ExchangeServerUrl'))
        self.username = str(config.get('Section1', 'UserName'))
        self.password = str(config.get('Section1', 'Password'))
       

    def getCalendarEvents(self, startdate, duration):
        ''' Set up the connection to Exchange
        Keyword arguments:
        startdate -- events will be returned that are ongoing on or started after this date
        duration -- events will be returned that are ongoing during this period, counting from the start date

        Returns: a list of events, with their timestamps set to UTC time zone.  The trailing +00:00 means that it's UTC.  Without
                    the trailing +00:00 it would mean that the datetime object is agnostic.
        '''
        if startdate.tzinfo is None or startdate.tzinfo.utcoffset(startdate) is None:
            raise ValueError('startdate must have time zone info attached')
        # Convert to UTC
        startdate = startdate.astimezone(timezone.utc)
        connection = ExchangeNTLMAuthConnection(url=self.url, username=self.username, password=self.password)
        service = Exchange2010Service(connection)
        events = service.calendar().list_events(
            start=startdate,
            end=startdate + duration,
            details=True
        )
        return events
