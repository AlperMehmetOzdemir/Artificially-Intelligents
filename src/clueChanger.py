from random import shuffle

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Resources
from wordnet import search_wordnet
#from merriamParser import getWordFromMerriam
#from oxford import getWordFromOxford
#from urbanParser import getWordFromUrban
#from didyoumean import did_you_mean
#from wikipediaParser import search_wikipedia
from googleDictionary import getWordFromGoogleDictionary

# All resources to be searched
RESOURCES = [#{'name': 'Wikipedia', 'func': search_wikipedia},
			 {'name': 'Wordnet', 'func': search_wordnet},
             #{'name': 'Merriam', 'func': getWordFromMerriam},
			 #{'name': 'Oxford', 'func': getWordFromOxford},
			 #{'name': 'Urban', 'func': getWordFromUrban},
             {'name': 'Google Dict', 'func': getWordFromGoogleDictionary}]

# For finding the stem (root) of the word
ps = PorterStemmer()

'''
	Changing the given word with its original clue
	according to the given replace policy:
	
	:param str word - the given word
	:param str clue - the original clue for the given word
	:param int replace_policy: 
				0 -> definition
				1 -> synonym
				2 -> antonym
				3 -> example sentence
	:return the given word + the new clue + source of new clue
'''


def changeClue(word, clue, replace_policy, trace = False):

	# Checking the word in Google's 'Did You Mean'
	'''
    did_you_mean_result = did_you_mean(word, trace)
	if did_you_mean_result is not None:
		word = did_you_mean_result
    '''
	# Getting the stem of the word
	# word = ps.stem(word)

	# Replace policy
	if replace_policy == 0:
		replaced = 'def'
	elif replace_policy == 1:
		replaced = 'syn'
	elif replace_policy == 2:
		replaced = 'ant'
	elif replace_policy == 3:
		replaced = 'examples'

	# New Clue
	new_clue = None
	is_found = False
	source = None

	# Checking the resources
	for resource in RESOURCES:
		results = resource['func'](word, trace)[replaced]

		if results is not None and len(results) != 0:
			# If the original clue returned as a new clue
			if clue in results:
				results.remove(clue)

			# Shuffling for randomness
			shuffle(results)

			for result in results:
				# If definition contains the word itself
				if replaced == 'def' and (word.lower() in word_tokenize(result.lower())):
					continue
				# If policy wants example sentence
				elif replaced == 'examples':
					if word.lower() not in result.lower():
						continue
					else:
						new_clue = result.lower().replace(word.lower(), '___').strip()
						is_found = True
						break
				else:
					new_clue = result.strip()
					is_found = True
					break

		# Found
		if is_found is True:
			source = resource['name']
			break

	# Returning
	return {
		'word': word,
		'new_clue': new_clue,
		'source': source
	}