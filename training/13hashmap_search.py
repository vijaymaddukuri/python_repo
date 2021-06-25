"""
Complete the checkMagazine function in the editor below.
It must print Yes if the note can be formed using the magazine, or No.
"""

def checkMagazine(magazine, note):
    for i in note:
        try:
            del magazine[magazine.index(i)]
        except ValueError:
            print('No')
            return
    print('Yes')
    return

mag = "give me one grand today night give".split()
note = 'give one grand today'.split()
checkMagazine(mag, note)