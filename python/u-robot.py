#Info
#	Python Exchange Web services library: https://pyexchange.readthedocs.org/en/latest/
#Installation
#	sudo apt-get install libxml2 libxml2-dev libxslt1-dev python-pip python-dev zlib1g-dev && pip install lxml pyexchange
#	download: https://pypi.python.org/packages/source/t/tzlocal/tzlocal-1.2.tar.gz
#	extract it and run sudo python setup.py install
from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from pytz import timezone
from datetime import datetime
from tzlocal import get_localzone
import getpass, ConfigParser

#The code is open source, but the url, username and password are not.
#The url and username are stored in a separate config file.
config = ConfigParser.RawConfigParser()
config.read('example.cfg')
URL = unicode(config.get('Section1', 'ExchangeServerUrl'))
USERNAME = unicode(config.get('Section1', 'UserName'))
#The password is read at startup of the program.
PASSWORD = getpass.getpass('Password: ')

# Set up the connection to Exchange
connection = ExchangeNTLMAuthConnection(url=URL,
                                        username=USERNAME,
                                        password=PASSWORD)
service = Exchange2010Service(connection)

events = service.calendar().list_events(
    start=get_localzone().localize(datetime(2015, 10, 1, 11, 0, 0)),
    end=get_localzone().localize(datetime(2015, 10, 29, 11, 0, 0)),
    details=True
)

for event in events.events:
    print "{start} {stop} - {subject}".format(
        start=event.start,
        stop=event.end,
        subject=event.subject
    )
