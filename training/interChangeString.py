def change(word):
    first=word[-1]
    last=word[0]
    newWord=first+word[1:-1]+last
    return newWord

word='vijay'
new=change(word)
print(new)