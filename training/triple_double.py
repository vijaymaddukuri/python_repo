def triple_double(song):
    import re
    a=re.sub('WUB'," ",song)
    a=a.split(' ')
    a=filter(None,a)
    return ' '.join(a)

a=triple_double('AWUBWUBWUBBWUBWUBWUBC')
print(a)


