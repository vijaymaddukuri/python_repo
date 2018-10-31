def count_words(doc):
    normilised_doc = ''.join(c.lower() if c.isalpha() else ' ' for c in doc)

    freq= {}

    for word in normilised_doc.split():
        freq[word] = freq.get(word, 0) + 1
    return freq

documents = ['Hi my name is vijay', 'hi my name is vicky', 'I am VJ', "my place is yanam", "my country is India"]

counts = map(count_words, documents)

def combine_counts(d1, d2):
    d = d1.copy()
    for word, count in d2.items():
        d[word] = d.get(word, 0) + count
    return d

from functools import reduce

total_count = reduce(combine_counts, counts)

print(total_count)