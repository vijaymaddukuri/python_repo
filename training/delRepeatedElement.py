# Delete occurrences of an element if it occurs more than n times

def delete_nth(order,max_e):
    return [item for index, item in enumerate(order) if order[:index].count(item)< max_e]

print delete_nth([20,37,20,21,20], 2)