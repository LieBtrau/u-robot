#!/usr/bin/env python3
#
# Info
#	Python Exchange Web services library: https://pyexchange.readthedocs.org/en/latest/
# Installation:
#	sudo apt install libxml2 libxml2-dev libxslt1-dev python3-pip python-dev zlib1g-dev && pip install lxml pyexchange tzlocal configparser
#
from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from datetime import datetime, timedelta, timezone
from tzlocal import get_localzone
import configparser, getpass, subprocess, sys


def getCalendarEvents(url, username, password, startdate, duration):
    ''' Set up the connection to Exchange
    Keyword arguments:
    url -- link to the .asmx file on the exchange server
    username -- your domain name\\username
    password -- password
    startdate -- events will be returned that are ongoing on or started after this date
    duration -- events will be returned that are ongoing during this period after the start date

    Returns: a list of events, with their timestamps set to UTC time zone.  The trailing +00:00 means that it's UTC.  Without
                the trailing +00:00 it would mean that the datetime object is agnostic.
    '''
    if startdate.tzinfo is None or startdate.tzinfo.utcoffset(startdate) is None:
        raise ValueError('startdate must have time zone info attached')
    #Convert to UTC
    startdate=startdate.astimezone(timezone.utc)
    connection = ExchangeNTLMAuthConnection(url=url,
                                            username=username,
                                            password=password)
    service = Exchange2010Service(connection)
    events = service.calendar().list_events(
        start=startdate,
        end=startdate + duration,
        details=True
    )
    return events


def validEvent(event):
    #When there's no location, this is likely to be some reminder instead of a real meeting
    return not str(event.subject).startswith('Canceled') and str(event.location) != 'None'


def speakEvent(event, TITLE):
    meetingTitle = str(event.subject)
    if meetingTitle.find('meeting') == -1:
        sentence = TITLE + ', you have a ' + meetingTitle + ' meeting.  '
    else:
        sentence = TITLE + ', you have a ' + meetingTitle + '.  '
    current_utc = datetime.now(timezone.utc) #Could be any time zone, let's stick to UTC here
    due_time = event.start - current_utc
    if event.start < current_utc and current_utc < event.end:
        sentence += 'This started {0} minutes ago.'.format(int(-due_time.total_seconds()/60))
    elif due_time < timedelta(hours=1):
        sentence += 'This meeting will start in {0} minutes.'.format(int(due_time.total_seconds()/60))
    elif due_time > timedelta(hours=1):
        sentence += 'This meeting will start in {0} hours.'.format(int(due_time.total_seconds()/3600))
    else:
        return
    speak(sentence)


def speak(sentence):
    print(sentence)
    p = subprocess.Popen('pico2wave -w lookdave.wav \'' + sentence + '\' && aplay lookdave.wav', shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()
    return retval


def main(argv):
    # The code is open source, but the url, username and password are not.
    # The url and username are stored in a separate config file.
    config = configparser.RawConfigParser()
    config.read('example.cfg')
    url = str(config.get('Section1', 'ExchangeServerUrl'))
    username = str(config.get('Section1', 'UserName'))

    # The password is read at startup of the program.
    # PASSWORD = getpass.getpass('Password: ')
    PASSWORD = str(config.get('Section1', 'Password'))

    TITLE = 'Master'

    speak('Hello, ' + TITLE)
    try:
        eventList = getCalendarEvents(url=url,
                                      username=username,
                                      password=PASSWORD,
                                      startdate=datetime.now(get_localzone()),
                                      duration=timedelta(days=1))
    except Exception as ex:
        speak('I am sorry ' + TITLE + ', but I have no access to your calendar.')
        print(ex)
        exit()

    if eventList.count == 0:
        speak('You are so lucky today ' + TITLE + '.  There are no meetings scheduled for you.')
    else:        
        print('You have ' + str(eventList.count) + ' events to handle today')
        fiveMinuteWarningList = eventList.events[:]
        while True:
            for event in fiveMinuteWarningList:
                duetime = event.start - datetime.now(timezone.utc)
                if duetime < timedelta(minutes = 5):
                    if validEvent(event):
                        speakEvent(event, TITLE)
                        s = "{start} {stop} - {subject} - {location}".format(
                            start=event.start,
                            stop=event.end,
                            subject=event.subject,
                            location=event.location)
                        print('Event info: ' + s)
                    fiveMinuteWarningList.remove(event)

if __name__ == '__main__':
    main(sys.argv[1:])