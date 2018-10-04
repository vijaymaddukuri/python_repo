def longestEvenWord(arr):
    longest = 0
    result ='00'
    for word in arr:
        if len(word)%2==0 and len(word)>longest:
            longest=len(word)
            result =word
    return result

a = ['is', 'a', 'vija', 'vijaya']
a=['hey']
print(longestEvenWord(a))
