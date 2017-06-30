#!/usr/bin/env python
# Mission Alert Agent
# Nathan Harmon, nharmon@gatech.edu
# https://github.com/nharmon/wmirs_scraper
# 
# Every 30 seconds the agent will check WMIRS for new missions. If it finds 
# a new "actual" mission (denoted by 'M' in the mission number), it will 
# trigger a message via GroupMe.
# 
import time
import urllib
import urllib2
from groupme import sendGroupmeMsg
from wmirs import WMIRS

### Settings ###

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
            if mission[3:4] == 'M':
                msg = "New Actual Mission in WMIRS: %s" % mission
                sendGroupmeMsg(groupme_botid, msg)

        time.sleep(30)
