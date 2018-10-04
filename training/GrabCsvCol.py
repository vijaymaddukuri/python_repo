def csv_columns(csv, indices):
    indices = sorted(set(indices))
    print indices
    lines = csv.splitlines()
    print lines

    result = []

    for line in lines:
        values = line.split(',')

        result.append(','.join(values[i] for i in indices if i < len(values)))
        print result

    return '\n'.join(result).strip()

a= csv_columns( "1,2,3\n4,5,6" , [0, 1] )
print a