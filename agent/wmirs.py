# Nathan Harmon, nharmon@gatech.edu
# https://github.com/nharmon/wmirs_scraper
#
# WMIRS Access Module
# 
# Python modules required:
#   - Beautiful Soup (https://pypi.python.org/pypi/beautifulsoup4)
#   - Mechanize (https://pypi.python.org/pypi/mechanize/)
#   - Six (https://pypi.python.org/pypi/six)
# 
import bs4
import mechanize
import six

### Settings ###

data_url = "https://www.capnhq.gov/WMIRS/Default.aspx"
login_url = "https://www.capnhq.gov/CAP.eServices.Web/Default.aspx"

### End of Settings ###

class WMIRS:
    """An interface to WMIRS for keeping track of missions
    """
    def __init__(self, username, password):
        """Initialize the scrapper by logging into WMIRS
        
        :param username (str): CAP eServices username
        :param password (str): CAP eServices password
        :inst self.username (str): From username
        :inst self.password (str): From password
        :inst self.data_url (str): URL where WMIRS lists missions
        :inst self.login_url (str): URL for logging into eServices
        :inst self.browser (mechanize.Browser): Browser instance
        :inst self.missions (set): Current snapshot of missions in WMIRS
        """
        self.username = username
        self.password = password
        self.data_url = data_url
        self.login_url = login_url
        self.browser = mechanize.Browser()
        self.loginEservices()
        self.missions = self.getMissions()
    
    def getMissions(self):
        """Get a list of missions in WMIRS
        
        :return missions (set): Missions numbers
        """
        resp = self.browser.open(self.data_url)
        soup = bs4.BeautifulSoup(resp.read(), "html5lib")
        missions = set()
        try:
            missions_table = soup.find('table', id='gvMissions')
        except:
            self.loginEservices()
            return missions
        
        for row in missions_table.findAll('tr'):
            for col in row.findAll('td')[:1]:
                for atag in col.findAll('a')[:1]:
                    missions.add(atag.findAll(text=True)[0])
        
        return missions

    def getNewMissions(self):
        """Look for new missions that have been added to WMIRS
        
        :returns new_missions (set): Mission numbers that were added
        """
        cur_missions = self.getMissions()
        new_missions = cur_missions.difference(self.missions)
        self.missions = cur_missions
        return new_missions
    
    def loginEservices(self):
        """Login to eServices
        """
        self.browser.open(self.login_url)
        self.browser.select_form('form1')
        self.browser.form['Login1$UserName'] = self.username
        self.browser.form['Login1$Password'] = self.password
        self.browser.submit()
        return True
