import requests, bs4
import re
import os
import unicodedata


def convertTo2Digit(n):
	return "{0:0=2d}".format(n)

episodeNumber = convertTo2Digit(4)
seasonNumber = convertTo2Digit(1)

filename = 'S'+str(seasonNumber)+'E'+str(episodeNumber)+'.txt'
print(filename)

episodeLink = 'http://www.livesinabox.com/friends/season1/104towgs.htm'
episodePage = requests.get(episodeLink)
episodeSoup = bs4.BeautifulSoup(episodePage.text)
episodeScript = episodeSoup.select('p')
f = open(filename, "w+")
for j in range(len(episodeScript)):
	try:
		f.write(episodeScript[j].getText()+'\n')
	except UnicodeEncodeError:
		x = unicodedata.normalize('NFKD', episodeScript[j].getText()+'\n').encode('ascii','ignore')
		f.write(x.decode("utf-8").strip())
f.close()
