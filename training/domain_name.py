def domain_name(url):
    import re
    matchObj = re.search('\/*[w]*\.*([A-Za-z-]+)\.', url)
    if matchObj != None:
        return matchObj.group(1)
    else:
        return matchObj

#url="www.xakep.ru"
#url="http://github.com/carbonfive/raygun"
#url="http://www.zombie-bites.com"
url="https://www.cnet.com"

u =domain_name(url)
print u
