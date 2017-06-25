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

class WMIRS:
    """Provides a interface to WMIRS as well as keeping track of missions
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
        """Get a list of missions in WMIRS
        
        :return missions (set): Missions numbers
        """
        resp = self.browser.open(data_url)
        soup = bs4.BeautifulSoup(resp.read(), "html5lib")
        missions = set()
        try:
            missions_table = soup.findAll('table', id='gvMissions')[0]
        except:
            self.__init__()
            return missions
        
        for row in mission_table.findAll('tr'):
            cols = row.findAll('td')
            if len(cols) > 0:
                atags = cols[0].findAll('a')
                if len(atags) > 0:
                    for mission in atags[0].findAll(text=True):
                        missions.add(mission)
        
        return missions

    def getNewMissions(self):
        """Look for new missions that have been added to WMIRS
        
        :returns new_missions (set): Mission numbers that were added
        """
        cur_missions = self.getMissions()
        new_missions = cur_missions.difference(self.missions)
        self.missions = cur_missions
        return new_missions
