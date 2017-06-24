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
import bs4
import datetime
import mechanize
import six
import time

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

### End of Settings ###

class WMIRS:
    """
    """
    def __init__(self):
        """Initialize the scrapper by logging into WMIRS
        
        :inst self.browser (mechanize.Browser): Browser instance
        :inst self.missions (set): Current snapshot of missions in WMIRS
        """
        self.browser = mechanize.Browser()
        self.browser.open(login_url)
        self.browser.select_form('form1')
        self.browser.form['Login1$UserName'] = username
        self.browser.form['Login1$Password'] = password
        self.browser.submit()
        self.missions = self.getMissions()
    
    def getMissions(self):
        """
        """
        resp = self.browser.open(data_url)
        soup = bs4.BeautifulSoup(resp.read(), "html5lib")
        mission_table = soup.findAll('table')[35] # TODO: find right table
        missions = set()
        for row in mission_table.findAll('tr'):
            cols = row.findAll('td')
            if len(cols) > 0:
                atags = cols[0].findAll('a')
                if len(atags) > 0:
                    for mission in atags[0].findAll(text=True):
                        missions.add(mission)
        
        return missions

    def getNewMissions(self):
        """
        """
        cur_missions = self.getMissions()
        new_missions = cur_missions.difference(self.missions)
        self.missions = cur_missions
        return new_missions


### Main ###

if __name__ == '__main__':
    wmirs = WMIRS()
    while True:
        new_missions = wmirs.getNewMissions()
        # TODO: Filter new missions and Send GroupMe Message
        #       accordingly
        #if len(new_missions) > 0:
        #    Send Function?
        
        for mission in new_missions:
            print "%s - New Mission: %s" % \
                  (datetime.datetime.utcnow(), mission)
        
        time.sleep(30)
