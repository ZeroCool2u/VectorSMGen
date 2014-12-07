#22c16 Project 2: Presidents
# Theo Linnemann
#22C:016:A05
# Based on code provided by Professor Alberto Maria Sergre

__author__ = 'Theo Linnemann'

import os
import math
import matplotlib.pyplot as plt

#Tuple container of stop words
SW = ( 'a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your' )
CC = ( ("aren't","are not"),("can't","can not"),("could've","could have"),("couldn't","could not"),("couldn't've","could not have"),("didn't","did not"),("doesn't","does not"),("don't","do not"),("hadn't","had not"),("hadn't've","had not have"),("hasn't","has not"),("haven't","have not"),("he'd","he had"),("he'd've","he would have"),("he'll","he will"),("he's","he is"),("how'd","how did"),("how'll","how will"),("how's","how has"),("I'd","I had"),("I'd've","I would have"),("I'll","I will"),("I'm","I am"),("I've","I have"),("isn't","is not"),("it'd","it had"),("it'd've","it would have"),("it'll","it will"),("it's","it is"),("let's","let us"),("ma'am","madam"),("mightn't","might not"),("mightn't've","might not have"),("might've","might have"),("mustn't","must not"),("must've","must have"),("needn't","need not"),("not've","not have"),("o'clock","of the clock"),("shan't","shall not"),("she'd","she had"),("she'd've","she would have"),("she'll","she will"),("she's","she is"),("should've","should have"),("shouldn't","should not"),("shouldn't've","should not have"),("that's","that is"),("there'd","there had"),("there'd've","there would have"),("there're","there are"),("there's","there is"),("they'd","they had"),("they'd've","they would have"),("they'll","they will"),("they're","they are"),("they've","they have"),("wasn't","was not"),("we'd","we had"),("we'd've","we would have"),("we'll","we will"),("we're","we are"),("we've","we have"),("weren't","were not"),("what'll","what will"),("what're","what are"),("what's","what is"),("what've","what have"),("when's","when is"),("where'd","where did"),("where's","where is"),("where've","where have"),("who'd","who had"),("who'll","who will"),("who're","who are"),("who's","who is"),("who've","who have"),("why'll","why will"),("why're","why are"),("why's","why is"),("won't","will not"),("would've","would have"),("wouldn't","would not"),("wouldn't've","would not have"),("y'all","you all"),("y'all'd've","you all would have"),("you'd","you had"),("you'd've","you would have"),("you'll","you will"),("you're","you are"),("you've","you have"),("-"," ") )

contractions = dict(CC)

def extractTerms(fileName, corpusTerms):

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
    return(tfds)


#Speech file input. Investigate opening multiple files
def readInput(filename):
    D = {}
    speechfile = open(filename, 'r')
    for line in speechfile:
        parse(line, D)
    speechfile.close()
    return(D)

#Parsing function, prepares word data for stemmer use.
def parse(documentString, D):
    contractionDict = dict(CC)
    stringAccum = ''
    for word in [word.strip('".,:;!?') for word in documentString.lower().split()]:
        if word in contractionDict:
            stringAccum = stringAccum + ' ' + contractionDict[word]
    for word in [stemmer(word) for word in [word.strip('".,:;!?') for word in documentString.lower().split()] if (word not in SW) and (word not in contractionDict.keys()) ]:
        if word in D:
            D[word] = D[word] + 1
        else:
            D[word] = 1

#Stemmer function, strips down words to consolidate roots to a single value in preparation for vector mapping
def stemmer(word):

    endingList = ['able','al','ance','ant','ar','ary','ate','ement','ence','ent','er','ess','ible','ic','ify','ine','ion','ism','iti','ity','ive','ize','ly','ment','or','ou','ous','th','ure']

    if word[-3:] == 'ies' and word [-4:] not in ['eies', 'aies']:
        word = word[:-3] + 'y'
    if word[-2:] == 'es' and word[-3:] not in ['aes', 'ees', 'oes']:
        word = word[:-1]
    if word[-1:] == 's' and word[-2:] not in ['us', 'ss', 'ys']:
        word = word[:-1]

    for i in range(1,5):
        if word[-i:] in endingList:
            word = word[:-i]
    return(word)

def topK(D,k):
    L = [(item,D[item]) for item in D.keys() ]
    return(sorted(L, reverse = True, key = lambda x: x[1]) [0:k])

def createModels(tfds, cfd, k):
    words = topK(cfd,k)
    words = tuple([term for term,frequency in words])
    lengthList = [sum(tfds[i].values()) for i in range(len(tfds))]

    models=[]

    for wordbanks in range(len(tfds)):
        w = [None]*len(words)
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

            w[k] = tf * math.log(rightNum/rightDen)

        #Begin normalization
        u = math.sqrt(sum([  w[i]**2 for i in range(len(w)) ]))
        for i in range(len(w)):
            w[i] = w[i] / u
        models.append(tuple(w))
    #[name{:-5} for name in files]
    return(words, models)

def dotProduct(tuple1, tuple2):
    dotproduct = 0
    for currentindex in range(len(tuple1)):
        print(tuple1)
        dotproduct += tuple1[currentindex] * tuple2[currentindex]
    return(dotproduct)

def averagedotproducts(models):
    listofaverages = []
    for president in range(0, len(models), 4):
        dpList = []
        for i in range(president, president+4):
            for j in range(i+1, president + 4):
                dpList.append(dotProduct(models[i],  models[j]))
        listofaverages.append(sum(dpList)/len(dpList))
    return(listofaverages)

def barGraph(presidentNames, listofaverages):
    plt.title('Presidential Speech Comparison')
    plt.xlabel('Presidents Averaged Normalized Vector')
    plt.ylabel('Presidents')
    plt.yticks(range(len(presidentNames), 0, -1), presidentNames)
    plt.barh(range(len(listofaverages), 0,-1), listofaverages)
    plt.show()

if __name__ == "__main__":
    corpusTerms = {}
    import files
    os.chdir(os.getcwd() + '\\unknowns/')
    #files = [f for f in os.listdir('.') if os.path.isfile(f)]
    #print(len(files))


    #A = extractTerms(files.F, corpusTerms)
    #B = createModels(A, corpusTerms, 100)
    #averages = averagedotproducts(B[1])
    #barGraph(files.P, averages)

    A = extractTerms(files.U, corpusTerms)
    B = createModels(A, corpusTerms, 100)
    averages = averagedotproducts(B[1])
    barGraph(files.U, averages)
