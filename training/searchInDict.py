def searchInDict(wordsList,word):
    temp=[]
    wordTemp=word.lower()
    wordsList=sorted(wordsList,reverse=True)
    for i in wordsList:
        if i.lower() in wordTemp:
            temp.append(i)
            wordTemp = wordTemp.replace(i, "")
    if len(word)==len("".join(temp)):
        return 1
    else:
        return 0

wList=["I","am","vijay","from",'yanam','software','job']
word='vijayIamYanam'
new=searchInDict(wList,word)
print new