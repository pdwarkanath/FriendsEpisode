#! python3

# import modules

import os
import re

# Universal variables

allFilesInDir = os.listdir()

allFilesInDirString = ' '.join(allFilesInDir)

numberOfSeasons = 10

characters = ["Joey", "Ross", "Chandler", "Rachel", "Monica", "Phoebe"]

numberOfCharacters = len(characters)

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
	if characterName == "Monica":
		similarWordsRegex = re.compile(r'(Mon(ica)?)')
	elif characterName == "Phoebe":
		similarWordsRegex = re.compile(r'(Ph(o|e)eb(e|s))')
	elif characterName == "Joey":
		similarWordsRegex = re.compile(r'(Jo(e(y)?)|Joseph)')
	elif characterName == "Ross":
		similarWordsRegex = re.compile(r'(Ross)')
	elif characterName == "Rachel":
		similarWordsRegex = re.compile(r'(Rach(el)?)')
	elif characterName == "Chandler":
		similarWordsRegex = re.compile(r'(Chandler)')
	return(similarWordsRegex)

# Get all sentences by a character

def getLines(characterName, text):
	linesRegex = re.compile(characterName+r': .*')
	lines = linesRegex.findall(text)
	return(lines)

# Get count of mentions of a character from lines

def getCount(mentionedName, lines):
	count = 0
	similarWordsRegex = similarWords(mentionedName)
	for line in lines:
		count += len(similarWordsRegex.findall(line))
	return(count)

# Get total count of mentions of one character by another

def getAllMentions(speakerName, mentionedName):
	mentions = []
	for i in range(numberOfSeasons):
		text = readScripts(i+1)
		text = removeBracketText(text)
		lines = getLines(speakerName, text)
		mentions.append(getCount(mentionedName, lines))
	return(mentions)

for speakerName in characters:
	for mentionedName in characters:
		if speakerName == mentionedName:
			continue
		else:
			print("{} mentions {}'s name by season: ".format(speakerName, mentionedName) + str(getAllMentions(speakerName, mentionedName)))






