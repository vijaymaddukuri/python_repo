def shortPalindrome(text):
    text = text.lower()
    results = []

    for i in range(len(text)):
        for j in range(0, i):
            chunk = text[j:i + 1]

            if chunk == chunk[::-1]:
                results.append(chunk)
    return len(results)

res = shortPalindrome('akakak')
print(res)