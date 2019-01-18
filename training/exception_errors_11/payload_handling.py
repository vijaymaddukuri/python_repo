def median(arr):
    items = sorted(arr)
    if len(items) == 0:
        raise ValueError("Median() arg is an empty sequence")

    median_index = (len(items)-1)//2

    if len(items) % 2 != 0:
        return items[median_index]
    return (items[median_index] + items[median_index+1])/2.0

def main():
    try:
       value = median([])
       return value

    except ValueError as e:
        print('payload:', str(e))

if __name__ == '__main__':
    print(main())