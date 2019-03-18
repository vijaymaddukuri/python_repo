def is_valid_IP(strng):
    import re
    result=True
    matchObj=re.search('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$',strng)
    print matchObj
    if matchObj:
        result = True
    else:
        result=False
    return result

ip=is_valid_IP('90.111.216.98')
print(ip)