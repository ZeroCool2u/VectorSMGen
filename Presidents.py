# 22c16 Project 2: Presidents
# Theo Linnemann
#22C:016:A05
# Based on code provided by Professor Alberto Maria Sergre
# Project repository can be found at: https://github.com/ZeroCool2u/VectorSMGen
# Uses the purepython implementation of the SnowBall stemming libarary. Note: This purepython implementation is ~100x slower than python wrapped C implementations and should not be used in prod code.

__author__ = 'Theo Linnemann'

#importing os and files modules for directory navigation
import files
#importing math module for arithmetic
import math
#importing matplotlib for plotting features
import matplotlib.pyplot as plt
#importing secondary stemmer library for stronger stemming feature set. Comment out if weak stemmer is preferred.
import stemming.porter2 as porter2

#Tuple container of stop words
SW = (
	'a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at',
	'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever',
	'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i',
	'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must',
	'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said',
	'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these',
	'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which',
	'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your' )
CC = (("aren't", "are not"), ("can't", "can not"), ("could've", "could have"), ("couldn't", "could not"),
      ("couldn't've", "could not have"), ("didn't", "did not"), ("doesn't", "does not"), ("don't", "do not"),
      ("hadn't", "had not"), ("hadn't've", "had not have"), ("hasn't", "has not"), ("haven't", "have not"),
      ("he'd", "he had"), ("he'd've", "he would have"), ("he'll", "he will"), ("he's", "he is"), ("how'd", "how did"),
      ("how'll", "how will"), ("how's", "how has"), ("I'd", "I had"), ("I'd've", "I would have"), ("I'll", "I will"),
      ("I'm", "I am"), ("I've", "I have"), ("isn't", "is not"), ("it'd", "it had"), ("it'd've", "it would have"),
      ("it'll", "it will"), ("it's", "it is"), ("let's", "let us"), ("ma'am", "madam"), ("mightn't", "might not"),
      ("mightn't've", "might not have"), ("might've", "might have"), ("mustn't", "must not"), ("must've", "must have"),
      ("needn't", "need not"), ("not've", "not have"), ("o'clock", "of the clock"), ("shan't", "shall not"),
      ("she'd", "she had"), ("she'd've", "she would have"), ("she'll", "she will"), ("she's", "she is"),
      ("should've", "should have"), ("shouldn't", "should not"), ("shouldn't've", "should not have"),
      ("that's", "that is"), ("there'd", "there had"), ("there'd've", "there would have"), ("there're", "there are"),
      ("there's", "there is"), ("they'd", "they had"), ("they'd've", "they would have"), ("they'll", "they will"),
      ("they're", "they are"), ("they've", "they have"), ("wasn't", "was not"), ("we'd", "we had"),
      ("we'd've", "we would have"), ("we'll", "we will"), ("we're", "we are"), ("we've", "we have"),
      ("weren't", "were not"), ("what'll", "what will"), ("what're", "what are"), ("what's", "what is"),
      ("what've", "what have"), ("when's", "when is"), ("where'd", "where did"), ("where's", "where is"),
      ("where've", "where have"), ("who'd", "who had"), ("who'll", "who will"), ("who're", "who are"),
      ("who's", "who is"), ("who've", "who have"), ("why'll", "why will"), ("why're", "why are"), ("why's", "why is"),
      ("won't", "will not"), ("would've", "would have"), ("wouldn't", "would not"), ("wouldn't've", "would not have"),
      ("y'all", "you all"), ("y'all'd've", "you all would have"), ("you'd", "you had"), ("you'd've", "you would have"),
      ("you'll", "you will"), ("you're", "you are"), ("you've", "you have"), ("-", " ") )

contractions = dict(CC)

corpusTerms = {}


def extractTerms(fileName, corpusTerms):
	'''extractTerms takes two inputs and outputs a Term Frequency Dictionary. fileName is simply the file names and corpus terms is an empty dictionary.'''
	files = fileName
	tfds = []
	for file in files:
		tfds.append(readInput(file))
	for termBank in tfds:
		for term in termBank:
			#print(term, termBank[term])
			if term in corpusTerms:
				corpusTerms[term] += 1
			else:
				corpusTerms[term] = 1
	if verbose == 1:
		print(tfds)
	return (tfds)


#Speech file input.
def readInput(filename):
	'''readInput handles opening and closing of files, in addition to invoking the parse function. Returns a dictionary with the fully parsed speech content.'''
	D = {}
	speechfile = open(filename, 'r')
	for line in speechfile:
		parse(line, D)
	speechfile.close()
	return (D)


#Parsing function, prepares word data for stemmer use.
def parse(documentString, D):
	"""Parse is invoked by readInput and invokes the stemmer function to completely clean up the speech text."""
	contractionDict = dict(CC)
	stringAccum = ''
	for word in [word.strip('".,:;!?') for word in documentString.lower().split()]:
		if word in contractionDict:
			stringAccum = stringAccum + ' ' + contractionDict[word]
	#Replace 'porter2.stem' with 'stemmer' if weak stemmer is preferred.
	for word in [porter2.stem(word) for word in [word.strip('".,:;!?') for word in documentString.lower().split()] if
	             (word not in SW) and (word not in contractionDict.keys())]:
		if word in D:
			D[word] = D[word] + 1
		else:
			D[word] = 1


# #Stemmer function, strips down words to consolidate roots to a single value in preparation for vector mapping
# def stemmer(word):
#     '''Stemmer takes each word in the text file as input and strips it down fairly close to its root. Consistency is the primary objective. Note: This is a very weak stemmer and should not be used in production code.'''
#     endingList = ['able','al','ance','ant','ar','ary','ate','ement','ence','ent','er','ess','ible','ic','ify','ine','ion','ism','iti','ity','ive','ize','ly','ment','or','ou','ous','th','ure']
#
#     #Stemmer exceptions code.
#     if word[-3:] == 'ies' and word [-4:] not in ['eies', 'aies']:
#         word = word[:-3] + 'y'
#     if word[-2:] == 'es' and word[-3:] not in ['aes', 'ees', 'oes']:
#         word = word[:-1]
#     if word[-1:] == 's' and word[-2:] not in ['us', 'ss', 'ys']:
#         word = word[:-1]
#
#     #Primary stripping mechanics.
#     for i in range(1,5):
#         if word[-i:] in endingList:
#             word = word[:-i]
#     return(word)


def topK(D, k):
	'''Simple function used only for finding the top K terms in a given speech.'''
	L = [(item, D[item]) for item in D.keys()]
	return (sorted(L, reverse=True, key=lambda x: x[1])[0:k])


def createModels(tfds, cfd, k):
	'''Create models takes the TFDS, Corpus Frequency Dictionary (CFD), and k (number of most common terms requested) as inputs. Its output of words and models are used by the barGraph function to create a histogram. '''
	words = topK(cfd, k)
	words = tuple([term for term, frequency in words])
	lengthList = [sum(tfds[i].values()) for i in range(len(tfds))]

	models = []

	for wordbanks in range(len(tfds)):
		#Note most IDE's will evaluate w as type list containing None, because of line 107. Upon execution list w will contain type float.
		w = [None] * len(words)
		for k in range(len(words)):

			#Computation for term frequency
			term = words[k]
			if term in tfds[wordbanks]:
				numerator = tfds[wordbanks][term]
			else:
				numerator = 0
			denominator = lengthList[wordbanks]
			tf = numerator / denominator

			#Tf computation complete. Beginning computation for log expression.
			rightNum = len(lengthList)
			rightDen = 1 + cfd[term]

			w[k] = tf * math.log(rightNum / rightDen)

		#Begin normalization. Note w[i] will be evaluated as empty by most IDE's. It is safe to ignore this warning instance.
		u = math.sqrt(sum([w[i] ** 2 for i in range(len(w))]))
		for i in range(len(w)):
			#Note w[i] will be evaluated by most IDE's as type empty until execution. It is safe to ignore this warning instance.
			w[i] = w[i] / u
		models.append(tuple(w))
	if verbose == 1:
		print(words, models)
	return (words, models)


def dotProduct(tuple1, tuple2):
	'''dotProduct takes 2 tuples (vectors) as inputs and computes their dotproduct.'''
	#Simple accumulator structure to compute the dot product of 2 vectors.
	dotproduct = 0
	for currentindex in range(len(tuple1)):
		if verbose == 1:
			print(tuple1)
		dotproduct += tuple1[currentindex] * tuple2[currentindex]
	return (dotproduct)


def averagedotproducts(models):
	'''Computes the average of two dotproducts, takes the list models as an input, outputs a list of averaged dotproducts. Note: This function assumes 4 speech samples per president.'''
	listofaverages = []
	#Any data set with a different number of speeches per speaker will need to modify the step value of the first range method. This change should be mirrored in presidents+step in the rest of the function.
	for president in range(0, len(models), 4):
		dpList = []
		#i is used as an index handle.
		for i in range(president, president + 3):
			#j is used as an index handle that's by definition i+1.
			for j in range(i + 1, president + 4):
				dpList.append(dotProduct(models[i], models[j]))
		listofaverages.append(sum(dpList) / len(dpList))
	return (listofaverages)


def barGraph(presidentNames, listofaverages):
	'''Generates a histogram of averaged normalized vectors and plots them for each president.'''
	plt.title('Presidential Speech Comparison')
	plt.xlabel('Presidents Averaged Normalized Vector')
	plt.ylabel('Presidents')
	plt.yticks(range(len(presidentNames), 0, -1), presidentNames)
	plt.barh(range(len(listofaverages), 0, -1), listofaverages)
	plt.show()


# def histogram(listofaverages):
#     '''Generates a histogram. This differs only in the formatting of how our data is represented, compared to barGraph() function.'''
#     plt.title('Presidential Speech Comparison')
#     plt.xlabel('Normalized Vector Value')
#     plt.ylabel("Frequency of Presidents at a Vector Value")
#     #Note the hardcoded bin steps. The bin argument may be removed if you'd like bin steps generated automatically.
#     plt.hist(listofaverages, bins=(.45, .50, .55, .60, .65, .70, .75, .80, .85, .90, .95, 1), histtype='bar', orientation='vertical')
#     plt.show()

def compareUknowns(k, fileName, models):
	tfds = extractTerms(fileName, corpusTerms)
	unknowns = createModels(tfds, corpusTerms, k)[1]
	listOfPresidentsAverageVectors = []

	def vectorAverage(president):
		"""computes an average vector for a single speakers corpus."""
		presidentAverage = k * [0]
		for index in range(k):
			for vector in president:
				presidentAverage[index] += vector[index] / 4
		return (presidentAverage)

	for president in range(0, len(models), 4):
		singleVectorList = []
		for i in range(president, president + 4):
			singleVectorList.append(models[i])
		if verbose == 1:
			print(singleVectorList)
		singleVector = vectorAverage(singleVectorList)
		if verbose == 1:
			print(singleVector)
		#Creates list of average presidential vectors. [president1 = [vectorvalue1,vectorvalue2,...], ...]
		if verbose == 1:
			print(listOfPresidentsAverageVectors)
		listOfPresidentsAverageVectors.append(singleVector)

	#init bestscore at high value out of bounds
	bestScore = 1000

	def compare(index, unknown, bestscore, competitor):
		"""Comapres the difference between 2 vector values."""
		if abs(unknown - competitor) > abs(unknown - bestscore[0]):
			if verbose == 1:
				print(bestscore)
			return bestscore
		else:
			if verbose == 1:
				print(competitor, index)
			return competitor, index

	listOfBestScores = [[(bestScore, -1) for x in range(k)] for u in unknowns]

	for unknown in range(len(unknowns)):
		for wordScoreIndex in range(k):
			for index in range(len(listOfPresidentsAverageVectors)):
				if verbose == 1:
					print(index)
				listOfBestScores[unknown][wordScoreIndex] = compare(index, unknowns[unknown][index],
				                                                    listOfBestScores[unknown][wordScoreIndex],
				                                                    listOfPresidentsAverageVectors[index][
					                                                    wordScoreIndex])

	return zip(fileName, [[files.P[b] for a, b in columns] for columns in listOfBestScores])


if __name__ == "__main__":
	#Debug option. Set to 1 to print debug information:
	verbose = 1

	#Change 'corpus' to 'unknowns' if comparing unknown speeches. This is only necessary if comparing unknowns.
	#os.chdir(os.getcwd() + '\\corpus/')
	#os.chdir(os.getcwd() + '\\unknowns/')
	#files = [f for f in os.listdir('.') if os.path.isfile(f)]
	#print(len(files))

	#These lines execute on file open to generate a histogram/barchart of normalized vectors. Enable only 1 of the last 2 lines.
	A = extractTerms(files.F, corpusTerms)
	B = createModels(A, corpusTerms, 100)
	averages = averagedotproducts(B[1])
	barGraph(files.P, averages)
	#histogram(averages)

	# #These four lines are used to evaluate unknown speeches.
	# A = extractTerms(files.F, corpusTerms)
	# B = createModels(A, corpusTerms, 100)
	# models = B[1]
	# Estimates = compareUknowns(100, files.U, models)
	# for line in Estimates:
	# 	print (line[0] + ": "+str(line[1]))