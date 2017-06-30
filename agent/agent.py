#!/usr/bin/env python
# Mission Alert Agent
# Nathan Harmon, nharmon@gatech.edu
# https://github.com/nharmon/wmirs_scraper
# 
# Periodically check WMIRS for new REDCAP missions and trigger GroupMe message
# when one is found.
# 
import time
import urllib
import urllib2
from groupme import sendGroupmeMsg
from wmirs import WMIRS

### Settings ###

# Interval to wait between checks (in seconds)
refresh_interval = 60

# eServices username and password
username = "Valid CAPID"
password = "eServices Password for CAPID above"

# GroupMe Bot ID (obtain from https://dev.groupme.com/bots)
groupme_botid = "Bot ID"

### End of Settings ###

### Main ###

if __name__ == '__main__':
    wmirs = WMIRS(username, password)
    while True:
        for mission in wmirs.getNewMissions():
            if mission[2:5] == '-M-':
                print("New mission (%s)" % mission)
                msg = ("New REDCAP Mission: %s. Please " % mission) + \
                       "reply with availability only. Instructions " + \
                       "will follow if you are needed."
                sendGroupmeMsg(groupme_botid, msg)

        time.sleep(refresh_interval)
