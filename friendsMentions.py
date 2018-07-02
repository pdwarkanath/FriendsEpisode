#! python3

# import modules

import os
import re

# Universal variables

allFilesInDir = os.listdir()

allFilesInDirString = ' '.join(allFilesInDir)

numberOfSeasons = 10

characters = ['Chandler', 'Joey', 'Monica', 'Phoebe','Rachel', 'Ross']

numberOfCharacters = len(characters)

FINAL_FILE = 'friendsMentions.csv'

# Convert episode/season number to 2 digit number

def convertTo2Digit(n):
	return "{0:0=2d}".format(n)

# Get nuumber of episodes in a season

def getNumberOfEpisodes(seasonNumber):
	seasonNumberRegex = re.compile(r'S'+convertTo2Digit(seasonNumber))
	numberOfEpisodes = len(seasonNumberRegex.findall(allFilesInDirString))
	return(numberOfEpisodes)


# Read files by season

def readScripts(seasonNumber):
	text = ""
	seasonWord = "S"+convertTo2Digit(seasonNumber)
	numberOfEpisodes = getNumberOfEpisodes(seasonNumber)
	for i in range(numberOfEpisodes):
		episodeNumber = seasonWord+"E"+convertTo2Digit(i+1)
		try:
			text += open(episodeNumber + ".txt").read()
		except FileNotFoundError:
			continue
	return(text)


# Delete lines in brackets

def removeBracketText(text):
	inBracketsRegex = re.compile(r'\(.*?\)')
	text = re.sub(inBracketsRegex,"", text)
	return(text)

# Define similar words regex for all characters

def similarWords(characterName):
	if characterName == 'Monica':
		similarWordsRegex = re.compile(r'(Mon(ica)?)')
	elif characterName == 'Phoebe':
		similarWordsRegex = re.compile(r'(Ph(o|e)eb(e|s))')
	elif characterName == 'Joey':
		similarWordsRegex = re.compile(r'(Jo(e(y)?)|Joseph)')
	elif characterName == 'Ross':
		similarWordsRegex = re.compile(r'(Ross)')
	elif characterName == 'Rachel':
		similarWordsRegex = re.compile(r'(Rach(el)?)')
	elif characterName == 'Chandler':
		similarWordsRegex = re.compile(r'(Chandler)')
	return(similarWordsRegex)

# Get all sentences by a character

def getLines(characterName, text):
	linesRegex = re.compile(characterName+r': .*')
	lines = linesRegex.findall(text)
	return(lines)

# Get count of mentions of a character from lines

def getCount(mentionedName, line):
	count = 0
	similarWordsRegex = similarWords(mentionedName)
	line = removeBracketText(line)
	count += len(similarWordsRegex.findall(line))
	return(count)

# Get number of mentions of one character by another in a season

def getMentions(speakerName, mentionedName, seasonNumber):
	mentions = 0
	text = readScripts(seasonNumber)
	lines = getLines(speakerName, text)
	for line in lines:
		mentions += getCount(mentionedName, line)
	return(mentions)

f = open(FINAL_FILE, 'w+')
f.write('seasonNumber,speakerName,mentionedName,mentions\n')
for seasonNumber in range(numberOfSeasons):
	for speakerName in characters:
		for mentionedName in characters:
			if speakerName == mentionedName:
				continue
			else:
				f.write('{},{},{},{}\n'.format(str(seasonNumber+1),speakerName, mentionedName, str(getMentions(speakerName, mentionedName, seasonNumber+1))))


f.close()


