import requests, bs4
import re
import unicodedata

PARENT_LINK ='http://www.livesinabox.com/friends/'


def convertTo2Digit(n):
	return "{0:0=2d}".format(n)

def getElems(res):
	scriptsPage = bs4.BeautifulSoup(res.text, 'lxml')
	elems = scriptsPage.select('li')
	return elems


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


def getEpisodeLink(elem):
	linkRegex = re.compile(r'(href=\".*\")>')
	m = linkRegex.search(str(elem))
	x = m.group().index('">')
	episodeLink = PARENT_LINK+m.group()[6:x]
	return episodeLink

def getEpisodeScript(episodeLink):
	episodePage = requests.get(episodeLink)
	episodeSoup = bs4.BeautifulSoup(episodePage.text, 'lxml')
	episodeScript = episodeSoup.find_all('p')

	return episodeScript

final_file = 'texts.txt'
def writeEpisodeScript(episodeScript, final_file):
	f = open(final_file, 'a+')
	for line in episodeScript:
		try:
			pattern = re.compile(r'Written by\: .*|\{.*|Transcribed by\: .*')
			if not(bool(pattern.match(line.getText()))):
				f.write(line.getText().replace('\n',' ')+'\n')
		except UnicodeEncodeError:
			x = unicodedata.normalize('NFKD', line.getText()+'\n').encode('ascii','ignore')
			f.write(x.decode("utf-8").strip())
	f.close()
	return






res = requests.get(PARENT_LINK+'scripts.shtml')
elems = getElems(res)

for elem in elems:
	filename = getFileName(elem)
	cache = filename
	
	episodeLink = getEpisodeLink(elem)
	episodeScript = getEpisodeScript(episodeLink)
		
	try:
		writeEpisodeScript(episodeScript, final_file)  # There is an episode without any number after season 7 episode 23. Hence this error-handling
		print('{} Downloaded!'.format(filename[0:6]))
	except TypeError:
		continue
		
"""


filename = getFileName(elems[94])
episodeLink = getEpisodeLink(elems[94])
episodeScript = getEpisodeScript(episodeLink)

writeEpisodeScript(episodeScript, filename)  # There is an episode without any number after season 7 episode 23. Hence this error-handling
print('{} Downloaded!'.format(filename[0:6]))


"""