def palindromes(text):
    text = text.lower()
    results = []

    for i in range(len(text)):
        for j in range(0, i):
            chunk = text[j:i + 1]

            if chunk == chunk[::-1]:
                results.append(chunk)
    print(results)

    return text.index(max(results, key=len)), results

def palindromes1(text):
    if text == text[::-1]:
        return len(text)
    return max(palindromes(text[:-1]), palindromes(text[1:]))

bigstrng='attract'
result=palindromes(bigstrng)
print(result)