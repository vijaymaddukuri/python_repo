import re
def is_pangram(s):
    print(set(s.lower()))
    # reg=re.findall('[a-zA-Z]+',s.lower())
    # print len(set("".join(re.findall('[a-zA-Z]+',s.lower()))))
    return True if len(set("".join(re.findall('[a-zA-Z]+',s.lower())))) == 26 else False

print(is_pangram("Tthe quick, brown fox jumps over the lazy dog!"))