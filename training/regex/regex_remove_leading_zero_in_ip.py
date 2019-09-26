import re


# function to remove leading zeros
def removeZeros(ip):
    new_ip = re.sub(r'\b0+(\d)', r'\1', ip)
    # splits the ip by "."
    # converts the words to integeres to remove leading removeZeros
    # convert back the integer to string and join them back to a string
    # \1 is first group match

    return new_ip


# driver code
# example1
ip = "100.020.003.400"
print(removeZeros(ip))

# example2
ip = "001.200.001.004"
print(removeZeros(ip))