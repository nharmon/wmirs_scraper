# Nathan Harmon, nharmon@gatech.edu
# https://github.com/nharmon/wmirs_scraper
# 
# Mission Alert Agent
# Every 30 seconds the agent will check WMIRS for new missions. If it finds 
# a new "actual" mission (denoted by 'M' in the mission number), it will 
# trigger message via GroupMe.
# 
import time
import urllib
import urllib2
from wmirs import WMIRS

### Settings ###

# eServices username and password
username = "Valid CAPID"
password = "eServices Password for CAPID above"

# GroupMe Bot ID (obtain from https://dev.groupme.com/bots)
groupme_botid = "Bot ID"

### End of Settings ###


def sendGroupmeMsg(botid, msg):
    """Sends the given message to GroupMe
    
    :param botid (str): Bot ID from GroupMe Developer's API
    :param msg (str): Message to be sent
    :returns (bool): True if message send successfully, otherwise False
    """
    groupme_url = "https://api.groupme.com/v3/bots/post"
    header = {
                "User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
             }
    data = {
              "text": msg,
              "bot_id": botid
           }
    body = urllib.urlencode(data)
    req = urllib2.Request(groupme_url, body, header)
    resp = urllib2.urlopen(req)
    if resp.code == 202:
        return True
    
    return False


### Main ###

if __name__ == '__main__':
    wmirs = WMIRS(username, password)
    while True:
        for mission in wmirs.getNewMissions():
            if mission[3:4] == 'M':
                msg = "New Actual Mission in WMIRS: %s" % mission
                sendGroupmeMsg(groupme_botid, msg)

        time.sleep(30)
