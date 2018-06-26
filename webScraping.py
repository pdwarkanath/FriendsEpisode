import requests, bs4
import re
import unicodedata


PARENT_LINK ='http://www.livesinabox.com/friends/'

def convertTo2Digit(n):
	return "{0:0=2d}".format(n)

def getElems(res):
	scriptsPage = bs4.BeautifulSoup(res.text)
	elems = scriptsPage.select('li')
	return elems




def getEpisodeLink(elem):
	linkRegex = re.compile(r'(href=\".*\")>')
	m = linkRegex.search(str(elem))
	x = m.group().index('">')
	episodeLink = PARENT_LINK+m.group()[6:x]
	return episodeLink

def getEpisodeScript(episodeLink):
	episodePage = requests.get(episodeLink)
	episodeSoup = bs4.BeautifulSoup(episodePage.text)
	episodeScript = episodeSoup.select('p')
	return episodeScript


def writeEpisodeScript(episodeScript, filename):
	f = open(filename, "w+")
	for j in range(len(episodeScript)):
		try:
			f.write(episodeScript[j].getText()+'\n')
		except UnicodeEncodeError:
			x = unicodedata.normalize('NFKD', episodeScript[j].getText()+'\n').encode('ascii','ignore')
			f.write(x.decode("utf-8").strip())
	f.close()
	return


def getFileName(elem):
	episodeName = elem.getText()
	colonIndex = episodeName.index(":")
	
	seasonEpisodeNumber = episodeName[len("Episode "):colonIndex].strip()
	try:
		if(len(seasonEpisodeNumber)==3):
			seasonNumber = convertTo2Digit(int(seasonEpisodeNumber[0]))
		else:
			seasonNumber = int(seasonEpisodeNumber[0:2])
		episodeNumber = seasonEpisodeNumber[-2:]
	except ValueError:
		return
	filename = 'S'+str(seasonNumber)+'E'+str(episodeNumber)+'.txt'
	return filename

res = requests.get(PARENT_LINK+'scripts.shtml')
elems = getElems(res)

for i in range(len(elems)):
	filename = getFileName(elems[i])
	episodeLink = getEpisodeLink(elems[i])
	episodeScript = getEpisodeScript(episodeLink)
	
	try:
		writeEpisodeScript(episodeScript, filename)  # There is an episode without any number after season 7 episode 23. Hence this error-handling
	except TypeError:
		continue
	print('{} Downloaded!'.format(filename[0:6]))


