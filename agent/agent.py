# Mission Alert Agent for Civil Air Patrol's WMIRS Application
# Written By: Nathan Harmon, nharmon@gatech.edu
# 
# This agent monitors WMIRS for new missions and then sends a GroupMe message.
# 
# Python modules required:
#   - Beautiful Soup (https://pypi.python.org/pypi/beautifulsoup4)
#   - Mechanize (https://pypi.python.org/pypi/mechanize/)
#   - Six (https://pypi.python.org/pypi/six)
# 
import datetime
from wmirs import WMIRS

### Settings ###

# The URL for the WMIRS Mission Search/Display
data_url = "https://www.capnhq.gov/WMIRS/Default.aspx"

# The eServices login webform
login_url = "https://www.capnhq.gov/CAP.eServices.Web/Default.aspx"

# eServices username and password
username = "Valid CAPID"
password = "eServices Password for CAPID above"

# GroupMe API Key
gmapikey = "Supplied by Groupme"


### Main ###

if __name__ == '__main__':
    wmirs = WMIRS()
    while True:
        for mission in wmirs.getNewMissions():
            if mission[3] == 'M':
                pass
                print "%s - New Mission: %s" % \
                      (datetime.datetime.utcnow(), mission)

        time.sleep(30)
