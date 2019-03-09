def binary_gap(binary):
    return len(max(str(binary[0:]).split('1')))

print(binary_gap('10100'))

