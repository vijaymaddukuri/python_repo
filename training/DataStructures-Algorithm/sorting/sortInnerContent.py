def sort_the_inner_content(words):
    finalWord=[]
    words=words.split(' ')
    for i in words:
        if len(i)>3:
            temp=i[1:-1]
            word=''.join(sorted(temp))
            temp=''
            for j in range(len(word),0,-1):
                temp=temp+word[j-1]

            word = i[0]+temp+i[-1]
        else:
            word=i
        finalWord.append(word)
    return " ".join(finalWord)

a=sort_the_inner_content('sort the inner content in descending order')
print(a)
