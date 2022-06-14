

import configparser
import logging
import sys
import datetime
from tzlocal import get_localzone
from CalendarExchangeLib import CalendarExchangeLib

def main(argv):
    config = configparser.RawConfigParser()
    config.read('example.cfg')
    myCalendar = CalendarExchangeLib(config)
    start = datetime.datetime.now(get_localzone())
    items = myCalendar.getCalendarEvents(start, datetime.timedelta(weeks = 2))
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
