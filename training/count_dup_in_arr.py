def count_duplicates(arr, n):
    return arr.count(n)

print(count_duplicates([1,2,3],4))


def rev_words(word):
    return " ".join((word.split(" "))[::-1])

print(rev_words("Hi I am Vijay"))

def remove_repeated_char(word):
    word = word.split(',')
    lst = ''
    for i in word:
        if i not in lst:
            lst+=i
    return lst
print(remove_repeated_char('1,2,3,4,5,3,0'))
