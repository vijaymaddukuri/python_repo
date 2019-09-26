import re
"""
Conditions for a valid password are:

Should have at least one number.
Should have at least one uppercase and one lowercase character.
Should have at least one special symbol.
Should be between 6 to 20 characters long.
"""

def main():
    passwd = 'Vijaykumar@1234567890'
    # reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{6,})"
    # reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W){6,20}"
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W)[A-Za-z\d\W]{6,20}$"
    # compiling regex
    pat = re.compile(reg)

    # searching regex
    mat = re.search(pat, passwd)

    # validating conditions
    if mat:
        print("Password is valid.")
    else:
        print("Password invalid !!")

    # Driver Code


if __name__ == '__main__':
    main()