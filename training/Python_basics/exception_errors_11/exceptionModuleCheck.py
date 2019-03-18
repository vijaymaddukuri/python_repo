from customRangeException import check_range, RangeError

try:
    check_range(.13)

except RangeError as err:
    print(err)