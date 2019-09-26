import re

regex = re.compile("""^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])\.)
(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.
(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.
(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])
""", re.VERBOSE)

VERBOSEregex = re.compile("""^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9]\.)(?=.{3})
(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[1-9])
""", re.VERBOSE)


def check(Ip):
    # pass the regular expression
    # and the string in search() method
    if (re.search(regex, Ip)):
        print("Valid Ip address")

    else:
        print("Invalid Ip address")

# Enter the Ip address
Ip = "192.168.01.1"

# calling run function
check(Ip)