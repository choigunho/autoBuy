#-*- coding: utf-8 -*-

import urllib
import re
from BeautifulSoup import *
from twilio.rest import TwilioRestClient

url = "http://cafe985.daum.net/_c21_/bbs_list?grpid=tdBX&fldid=79XF" 
keywords = [u"미즈노"]

html = urllib.urlopen(url)
soup = BeautifulSoup(html)


def sendSMS(msg):
	# Download the twilio-python library from http://twilio.com/docs/libraries
	# Find these values at https://twilio.com/user/account
	account_sid = "xxxxx"
	auth_token = "xxxxx"
	client = TwilioRestClient(account_sid, auth_token)
	 
	message = client.sms.messages.create(to="+821085611186", from_="+14344736169", body=msg)

def extractAttribute(node, classname):
	target = node.find('td', {'class':classname})

	if classname == 'nick':
		return target.find('a').string

	if classname == 'subject':
		if node.find('a').string == None:
			return target.find('a').findNext().nextSibling.string
		return target.find('a').string

	return target.string

def findItem(node):
	
	


if __name__ == '__main__':

	table = soup('table', {'class':'bbsList'})
	rows = table[0].find('tbody').findAll('tr')

	for row in rows:
		if extractAttribute(row, 'num') != None:
			
			subject = extractAttribute(row, 'subject')

			for word in keywords:
				if subject.find(word) == 1:
					print extractAttribute(row, 'num'), extractAttribute(row, 'subject'), extractAttribute(row, 'nick'), extractAttribute(row, 'date')
					#sendSMS(subject)
			

			# print extractAttribute(row, 'num'), extractAttribute(row, 'subject'), extractAttribute(row, 'nick'), extractAttribute(row, 'date')