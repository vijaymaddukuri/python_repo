def longest_repetition1(word):
    if len(word)>1:
        dict={}
        for i in word:
            dict[i]=dict.get(i,0) + 1

        max_value= max(dict.values())
        for key,value in dict.items():
            if value==max_value:
                max_key=key
        return max_key, max_value
    else:
        return 0

def longest_repetition2(word):
    if len(word)>1:
        count=1
        maxCount=0
        Snum=word[0]
        Fnum=Snum
        for item in word[1:]:
            if item == Snum:
                count+=1
            else:
                if count>maxCount:
                    maxCount=count
                    Fnum=Snum
                count=1
            Snum=item
        if count > maxCount:
            maxCount = count
            Fnum = Snum
        return Fnum, maxCount

    else:
        return '', 0

def longest_repetition(chars):
    if chars == "": return ("", 0)
    fCount, count = 1, 1
    char = chars[0]
    for i, c in enumerate(chars[1:]):
        if c == chars[i]:
            count += 1
            if count > fCount:
                fCount = int(count)
                char = str(c)
        else: count = 1
    return (char, fCount)

print(longest_repetition('beabbeefeab'))
print(longest_repetition([1, 1, 2, 1, 2, 2]))