def longWord(wlist):
    wordLen=[]
    for n in wlist:
        wordLen.append((len(n),n))
    wordLen.sort()
    print wordLen
    return wordLen[-1][1]

words=['vijay','Ajay','vicky']
word=longWord(words)
print word