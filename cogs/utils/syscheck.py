import sys
import time


def syscheck():
    if sys.version_info <= (3, 6):
        print('Need Python 3.6 or greater to run this bot. Exiting...')
        time.sleep(3)
        sys.exit()
