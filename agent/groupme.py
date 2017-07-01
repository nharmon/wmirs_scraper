#!/usr/bin/env python
# GroupMe Sending Module
# Nathan Harmon, nharmon@gatech.edu
# https://github.com/nharmon/wmirs_scraper
#
import urllib
import urllib2

def sendGroupmeMsg(botid, msg):
    """Sends the given message through GroupMe via the given BotID
    
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
