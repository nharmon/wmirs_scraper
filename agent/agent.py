#!/usr/bin/env python
# Mission Alert Agent
# Nathan Harmon, nharmon@gatech.edu
# https://github.com/nharmon/wmirs_scraper
# 
# Periodically check WMIRS for new REDCAP missions and trigger GroupMe message
# when one is found.
# 
import ConfigParser
import os
import sys
import time
from groupme import sendGroupmeMsg
from wmirs import WMIRS

### Main ###

if __name__ == '__main__':
    # Allow an alternate configuration file be specified.
    if len(sys.argv) > 1:
        configfile = sys.argv[1]
    else:
        configfile = "agent.conf"
    
    # Parse the configuration file
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    refresh_interval = int(Config.get("agent","refresh-interval"))
    wuser = Config.get("wmirs","username")
    wpass = Config.get("wmirs","password")
    groupmeid = Config.get("groupme","botid")
    
    # Write the current PID to agent.pid
    with open(Config.get("agent","pidfile"), 'w') as pidfile:
        pidfile.write(str(os.getpid()))
    
    # Setup WMIRS connection
    wmirs = WMIRS(wuser, wpass)
    
    # Start checking for new missions
    while True:
        for mission in wmirs.getNewMissions():
            if mission[2:5] == '-M-':
                print("New mission (%s)" % mission)
                msg = "New REDCAP Mission: %s. Please reply with " + \
                      "availability only. Instructions will follow " + \
                      "if activated."
                sendGroupmeMsg(groupmeid, msg % mission)

        time.sleep(refresh_interval)
