def palindromes(text):
    text = text.lower()
    results = []

    for i in range(len(text)):
        for j in range(0, i):
            print i
            print j
            chunk = text[j:i + 1]

            if chunk == chunk[::-1]:
                results.append(chunk)
    print results

    return text.index(max(results, key=len)), results

bigstrng='lirilisdkoddsiodjisodjisodjsoidjsiodjosdjsdJjjssjasjjsunssnnxndsnandjsdjnjnsjsainaisundaidniasaddsdsdsdsdadcxcssdsdadddddADSADSWADZXADWEEDWFRDSADFDDDDDDDDDDDDDDFSDAAAAAAAAAAAAAAADAQDSDDDDDDDDDDDDDDDFFFFFFFFFFFFFFFFSADXCXCXCXCXCXCXCXCXCXCXC'
result=palindromes(bigstrng)
print result