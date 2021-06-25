wordList=['I','am','bangalore','from','is','not']

word='IamFromBangalore'

for item in sorted(wordList, key=len):
    print(item)
    word=word.lower()
    item=item.lower()
    word=word.replace(item,'')
if len(word):
    print ("Few words are missing")
else:
    print ("All words are present")
