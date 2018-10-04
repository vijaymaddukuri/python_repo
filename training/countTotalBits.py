def countTotalBits(num):
    bits = bin(num)[2:]
    return len(bits)

# Driver program
if __name__ == "__main__":
    num = 13
    len = countTotalBits(num)
    print(len)

