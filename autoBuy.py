#-*- coding: utf-8 -*-


import urllib
import urllib2, httplib2
import json
import re, time
from BeautifulSoup import *
from twilio.rest import TwilioRestClient

url = "http://cafe985.daum.net/_c21_/bbs_list?grpid=tdBX&fldid=79XF" 
keywords = [u"롤링스"]

# Download the twilio-python library from http://twilio.com/docs/libraries
def sendSMS(msg):

	# Find these values at https://twilio.com/user/account
	account_sid = "xxx"
	auth_token = "yyy"
	client = TwilioRestClient(account_sid, auth_token)
	 
	message = client.sms.messages.create(to="+821085611186", from_="+14344736169", body=msg)

def extractAttribute(node, classname):
	target = node.find('td', {'class':classname})

	if classname == 'nick':
		return target.find('a').string

	if classname == 'subject':
		if node.find('a').string == None:
			# link = node.find('a').get('href')
			return target.find('a').findNext().nextSibling.string
		return target.find('a').string

	return target.string

def extractUrl(node):
	target = node.find('td', {'class':'subject'})

	return target.find('a').get('href')

def is_duplicated(item, url):
	if item not in wishItems:
		wishItems.append(item)

		fullurl = "http://cafe985.daum.net" + url
		# print fullurl

		link = shorternUrl(fullurl)
		# print link

		result_dic = json.loads(link)
		# print result_dic['id']

		sendSMS(num + ',' + subject + ',' + result_dic['id'])

def shorternUrl(url):
    API_KEY = "AIzaSyCvhcU63u5OTnUsdYaCFtDkcutNm6lIEpw"
    apiUrl = 'https://www.googleapis.com/urlshortener/v1/url'
    longUrl = url
    headers = {"Content-type": "application/json"}

    data = {"longUrl": longUrl}
    h = httplib2.Http('.cache')
    
    try:
        headers, response = h.request(apiUrl, "POST", json.dumps(data), headers)
        return response

    except Exception, e:
        return "unexpected error %s" % e



if __name__ == '__main__':

	wishItems = []

	while True:
		html = urllib.urlopen(url)
		soup = BeautifulSoup(html)

		table = soup('table', {'class':'bbsList'})
		rows = table[0].find('tbody').findAll('tr')

		for row in rows:
			if extractAttribute(row, 'num') != None:
				
				num = extractAttribute(row, 'num')
				subject = extractAttribute(row, 'subject')
				nick = extractAttribute(row, 'nick')
				date = extractAttribute(row, 'date')
				url = extractUrl(row)

				# print url

				for word in keywords:
					if subject.find(word) == 1:
						print num, subject, nick, date
						is_duplicated(num, url)

		# print wishItems
		time.sleep(60)
