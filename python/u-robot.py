#!/usr/bin/env python3
#
# Info
#	Python Exchange Web services library: https://pyexchange.readthedocs.org/en/latest/
# Installation:
#	sudo apt install libxml2 libxml2-dev libxslt1-dev python3-pip python-dev zlib1g-dev && pip install lxml pyexchange tzlocal configparser
#
from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from datetime import datetime, timedelta
from tzlocal import get_localzone
import configparser, getpass, subprocess, sys


def speak(sentence):
    print(sentence)
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
        start=startdate.astimezone(),
        end=(startdate + duration).astimezone(),
        details=True
    )
    return events


def validEvent(event):
    return not str(event.subject).startswith('Canceled')


def speakEvent(event, TITLE):
    if str(event.location) == 'None':
        return
    sentence = TITLE + ', you have a ' + event.subject + ' meeting.\n'
    startseconds = (event.start - datetime.now(get_localzone())).total_seconds()
    endseconds = (event.end - datetime.now(get_localzone())).total_seconds()
    minutes = int(round(startseconds / 60, 0))
    hours = int(round(startseconds / 3600, 0))
    if startseconds < 0 and endseconds > 0:
        sentence += 'This started {0} minutes ago.'.format(-minutes)
    elif startseconds > 0 and startseconds < 3600:
        sentence += 'This meeting will start in {0} minutes.'.format(minutes)
    elif startseconds > 3600:
        sentence += 'This meeting will start in {0} hours.'.format(hours)
    else:
        return
    speak(sentence)


def giveFiveMinuteWarning(fiveminuteeventlist, TITLE):
    for event in fiveminuteeventlist:
        duetime = event.start - datetime.now(get_localzone())
        if duetime.total_seconds() < 300:
            if validEvent(event):
                speakEvent(event, TITLE)
                s = "{start} {stop} - {subject} - {location}".format(
                    start=event.start,
                    stop=event.end,
                    subject=event.subject,
                    location=event.location)
                print(s)
            fiveminuteeventlist.remove(event)

def main(argv):
    # The code is open source, but the url, username and password are not.
    # The url and username are stored in a separate config file.
    config = configparser.RawConfigParser()
    config.read('outlook.live.cfg')
    url = str(config.get('Section1', 'ExchangeServerUrl'))
    username = str(config.get('Section1', 'UserName'))

    # The password is read at startup of the program.
    # PASSWORD = getpass.getpass('Password: ')
    PASSWORD = str(config.get('Section1', 'Password'))

    TITLE = 'master'

    speak('Hello, ' + TITLE)
    try:
        eventList = getCalendarEvents(url=url,
                                      username=username,
                                      password=PASSWORD,
                                      startdate=datetime.utcnow()-timedelta(hours=1),
                                      duration=timedelta(days=1))
    except Exception as ex:
        speak('I am sorry ' + TITLE + ', but I have no access to your calendar.')
        print(ex)
        exit()
    print("You have " + str(eventList.count) + " events to handle today")

    if eventList.count == 0:
        speak('You are so lucky today ' + TITLE + '.  There are no meetings scheduled for you.')
    else:
        fiveMinuteWarningList = eventList.events[:]
        while True:
            giveFiveMinuteWarning(fiveMinuteWarningList, TITLE)

if __name__ == '__main__':
    main(sys.argv[1:])