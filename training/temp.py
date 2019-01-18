import re


output = """
{"links":[{"href":"https://100.66.113.102:9090/nwrestapi/v1",
"title":"NetWorker REST API v1"},{"href":"https://100.66.113.102:9090/nwrestapi/v2","title":"NetWorker REST API v2"}]
,"version":"9.1.1.5.Build.
"""

nw_exp_version='9.0'

matchObj = re.search("\"version\":\S+", output)

if matchObj:
    print('Networker Version -', matchObj.group())
    # Validate the version
    if nw_exp_version in matchObj.group():
        print('Expected Networker version is installed')
    else:
        message = ('Networker version mismatch, expected version {}'
                   'found version {}').format(nw_exp_version, matchObj.group())
        print(message)
        raise Exception(message)
else:
    message = 'Unable to fetch the Networker version'
    print(message)
    raise Exception(message)