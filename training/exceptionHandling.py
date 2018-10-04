from sys import exc_info
def safe_float(value):
    try:
        result=None
        return float(value[0])
    except ValueError as err:
        print(err)

    except (IndexError, KeyError) as err:
        print(err)
    except:
        print('internal script error')
        print(exc_info())
    finally:
        print('finally block of the code')
        return result
print(safe_float('vijay'))