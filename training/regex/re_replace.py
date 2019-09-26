import re
name = '123abcjw:, .@! eiw'

print(re.sub('\W+', '', name))

# Multiple String replace

def replace(string, char):
    pattern = char + '{2,}'
    string = re.sub(pattern, char, string)
    return string


# Driver code
string = 'Geeksforgeeks'
char = 'e'
print(replace(string, char))