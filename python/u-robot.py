# Info
#	Python Exchange Web services library: https://pyexchange.readthedocs.org/en/latest/
# Installation
#	sudo apt-get install libxml2 libxml2-dev libxslt1-dev python-pip python-dev zlib1g-dev && pip install lxml pyexchange
#	download: https://pypi.python.org/packages/source/t/tzlocal/tzlocal-1.2.tar.gz
#	extract it and run sudo python setup.py install
from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from pytz import timezone
from datetime import datetime, timedelta
from tzlocal import get_localzone
import getpass, ConfigParser, subprocess


def speak(sentence):
    p = subprocess.Popen('pico2wave -w lookdave.wav \'' + sentence + '\' && aplay lookdave.wav', shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()
    return retval


def getCalendarEvents(url, username, password, startdate, duration):
    # Set up the connection to Exchange
    connection = ExchangeNTLMAuthConnection(url=url,
                                            username=username,
                                            password=password)
    service = Exchange2010Service(connection)
    events = service.calendar().list_events(
        start=get_localzone().localize(startdate),
        end=get_localzone().localize(startdate + duration),
        details=True
    )
    return events


def validEvent(event):
    return not str(event.subject).startswith('Canceled')


def speakEvent(event):
    if str(event.location) == 'None':
        return
    sentence = TITLE + ', you have a ' + event.subject + ' meeting.\n'
    duetime = event.start - datetime.now(get_localzone())
    sentence += 'This meeting will start in {0} hours.'.format(int(duetime.total_seconds() / 3600))
    speak(sentence)


# The code is open source, but the url, username and password are not.
# The url and username are stored in a separate config file.
config = ConfigParser.RawConfigParser()
config.read('example.cfg')
url = unicode(config.get('Section1', 'ExchangeServerUrl'))
username = unicode(config.get('Section1', 'UserName'))
# The password is read at startup of the program.
PASSWORD = getpass.getpass('Password: ')
TITLE = 'Master'

try:
    eventList = getCalendarEvents(url=url,
                                  username=username,
                                  password=PASSWORD,
                                  startdate=datetime.now(),
                                  duration=timedelta(days=1))
except:
    speak('I am sorry '+ TITLE + ' , but I have no access to your calendar.')
    exit()

if eventList.count == 0:
    speak('You are so lucky today '+ TITLE + '.  There are no meetings scheduled for you.')

for event in eventList.events:
    s = "{start} {stop} - {subject} - {location}".format(
        start=event.start,
        stop=event.end,
        subject=event.subject,
        location=event.location)
    print s
    if (validEvent(event)):
        speakEvent(event)
