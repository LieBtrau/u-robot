#!/usr/bin/env python3
#
# Info
#	Python Exchange Web services library: https://pyexchange.readthedocs.org/en/latest/
# Installation:
#	sudo apt install libxml2 libxml2-dev libxslt1-dev python3-pip python-dev zlib1g-dev && pip install configparser lxml pyexchange pyserial tzlocal
#
from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection
from datetime import datetime, timedelta, timezone
from tzlocal import get_localzone
import configparser
import logging
import pyttsx3
import serial
import sys
import time


def getCalendarEvents(url, username, password, startdate, duration):
    ''' Set up the connection to Exchange
    Keyword arguments:
    url -- link to the .asmx file on the exchange server
    username -- your domain name\\username
    password -- password
    startdate -- events will be returned that are ongoing on or started after this date
    duration -- events will be returned that are ongoing during this period, counting from the start date

    Returns: a list of events, with their timestamps set to UTC time zone.  The trailing +00:00 means that it's UTC.  Without
                the trailing +00:00 it would mean that the datetime object is agnostic.
    '''
    if startdate.tzinfo is None or startdate.tzinfo.utcoffset(startdate) is None:
        raise ValueError('startdate must have time zone info attached')
    # Convert to UTC
    startdate = startdate.astimezone(timezone.utc)
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
    # When there's no location, this is likely to be some reminder instead of a real meeting
    return not str(event.subject).startswith('Canceled') and str(event.location) != 'None'


def speakEvent(event, TITLE):
    meetingTitle = str(event.subject)
    # Avoid to say the word 'meeting' twice.
    if meetingTitle.find('meeting') == -1:
        sentence = TITLE + ', you have a ' + meetingTitle + ' meeting.  '
    else:
        sentence = TITLE + ', you have a ' + meetingTitle + '.  '
    # Could be any time zone, let's stick to UTC here
    current_utc = datetime.now(timezone.utc)
    due_time = event.start - current_utc
    if event.start < current_utc and current_utc < event.end:
        # Meeting is ongoing
        if due_time.total_seconds() > 60:
            sentence += 'This started {0} minutes ago.'.format(
                int(-due_time.total_seconds()/60))
        else:
            sentence += 'This starts now! '
    elif current_utc > event.end:
        # Meeting has ended
        return
    elif due_time < timedelta(hours=1):
        sentence += 'This meeting will start in {0} minutes.'.format(
            int(due_time.total_seconds()/60))
    elif due_time > timedelta(hours=1):
        sentence += 'This meeting will start in {0} hours.'.format(
            int(due_time.total_seconds()/3600))
    else:
        return
    speak(sentence)


def speak(sentence):
    logging.info('Robot says: ' + sentence)
    serialPort = serial.Serial(port='COM15', baudrate=9600)
    serialPort.write(b'audio 0\r\n')    # Robosapien audio output = PC audio
    engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 1 for female
    engine.setProperty('rate', 150)
    engine.say(sentence)
    engine.runAndWait()
    engine.stop()
    # Robosapien audio output  = Robosapien's own voice
    serialPort.write(b'audio 1\r\n')
    serialPort.close()


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
    SERVER_POLL_INTERVAL_MINUTES = 25
    speak('Hello ' + TITLE + '.  How can I be of your service today?')
    while True:
        try:
            eventList = getCalendarEvents(url=url,
                                          username=username,
                                          password=PASSWORD,
                                          startdate=datetime.now(
                                              get_localzone()),
                                          duration=timedelta(minutes=SERVER_POLL_INTERVAL_MINUTES))
        except Exception as ex:
            speak('I am sorry ' + TITLE +
                  ', but I have no access to your calendar.')
            logging.info(ex)
            exit()

        if eventList.count == 0:
            # No events found, sleep the default time
            due_time = timedelta(
                minutes=SERVER_POLL_INTERVAL_MINUTES)
        else:
            logging.info('You have ' + str(eventList.count) +
                         ' events in the list.')
            # Only take into account the first event on the list
            firstEvent = eventList.events[0]
            if validEvent(firstEvent):
                event_info = "{start} {stop} - {subject} - {location}".format(
                    start=firstEvent.start,
                    stop=firstEvent.end,
                    subject=firstEvent.subject,
                    location=firstEvent.location)
                logging.info('Event info: ' + event_info)
                if(datetime.now(timezone.utc) < firstEvent.start):
                    # Meeting will be starting soon
                    speakEvent(firstEvent, TITLE)
                    due_time = firstEvent.start - datetime.now(timezone.utc)
                elif firstEvent.start < datetime.now(timezone.utc) and datetime.now(timezone.utc) < firstEvent.end:
                    # Meeting is already ongoing
                    ongoing_time = datetime.now(
                        timezone.utc) - firstEvent.start
                    if(ongoing_time < timedelta(minutes=SERVER_POLL_INTERVAL_MINUTES)):
                        # You're not very late yet.  It would still be polite to join.
                        speakEvent(firstEvent, TITLE)
                    # Wait until this meeting is over before polling the server again.
                    due_time = firstEvent.end - datetime.now(timezone.utc)
                else:
                    # Event already done, sleep the default time
                    due_time = timedelta(minutes=SERVER_POLL_INTERVAL_MINUTES)
        logging.info('Polling server again in ' +
                     str(int(due_time.total_seconds()))+' seconds.')
        time.sleep(int(due_time.total_seconds()))


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