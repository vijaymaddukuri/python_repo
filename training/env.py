import os
import sys
import os.path
os.getcwd()
#os.chdir(r'/etc/')
os.chdir(r'D:\new')
id_rsa_key="""export id_rsa = MIIEpAIBAAKCAQEA4rX8bguzaX3F5Pm+2ExBim6GGTsrf0eguBTyTBrCpr/dwEp6
dF2y1Uk4LbYzXI2imHUkz7ih6s9CoVWRPhie6fu7iabwfxEATSF98rUtTIhqmPYA
IdM8baTg/XiFZ+pE6oEutK6m/sznOOb2OCMbdjI4Y6vPKEq/fQkCQkictxsU2IDK
2vzYVQgK3CTE0B93Erw+Hj9k1j9//urBx8jWKgFaVruJS/tEzy8N5CRNbKZPgS/N
SUw+sfCgwgqd1ygpL1GL+Zf+XgafUsgx3WP1MamFttEBMiukYi8j4vmJ1UchLayM
l2olJPFsOfq49bTJJZSyyzGhJzRbZlzAgvxoUwIDAQABAoIBAAoVdCPk61b+3CWC
IkX2plek8NwAcL/ZjMGDVP+jlRLbp95csbOpU0H/XrtRxlkQh7HmS/vdR35tN5Z7
etlbOP5JTx8hSMMuG2hS3ApGmrwzuSISlxDqF179HXDIwo5LskMH+e7Zcd4VeRdj
1oHKtfb85tswEifFo1zJYMtX9XiDa2pju/0RFdKzeSo9zwaYAmqWXtHJp6KBUjB2
NkHAfA754kkJNrDpkLGcEJpdv3yihSueDTFsIzHmtjQyf0bNi3bmCI2Uw9k3o0Nm
UXLRr/xtiVPA8E1UznaD961l9WqRibedvxu+oYYrOyadU7Mf5tOQLdpqN1y3Jjwm
C38J0KkCgYEA99BBuGOkkrbBBkRCRl2L0w5adISE6L9fCzLmjz/k8ze5Oyub2ebi
FJJjWeBZ+jlKy/XbHTG1dFIDtF9+KWOPCt87kholXJyLKjaiS31ilHq+pPHNa6Gp
1Xv14cC0D9ZVC/H8KEfVebdNiKwEArIvn15viVlBTzPUSZlQtlQ9d6cCgYEA6jNE
C3U7CXqvAq+vzCJkesa/+/8IbubuGG18L7lExTjlNi9LnrKfU50+uxcrB412Oo1r
RlA0dsPf6qLyubdpfuCvL2Pa1qA+NB5hXlPJRuKE2c5jN5JXfwqLREwbQCm4AfyX
pnw3jh0KnLIxLG6Wd+X4VhgXVR5GbhNHnTBMn3UCgYEAkfA4M+GicrBjnlAmg4/l
n0aNqJ6+Mt84lrzEIMptB3rif+EfqESbEahgD/bapkyFKvY/ssKqbLU770ZpYvB5
tdpfF5yEMjUSk6qXC0PtASoECdlIs0ECZnHZDLjSkZ0UerNoX0RmiIaVh45d0kSj
XQRdRRKmLoGEXE+Iw8d6Z3MCgYBBx0paSX/eZrXW9E9U72f3T/FGLthIhdXjyIRz
xv54wkUmldwQY6z6SBUBaT1trp7BTU0O/6HspZEzjrbL0KbxutuZXNtvIqy16L6C
Rtgmb6LOpfgZ+KFYjjaVZSbWO6Fx9WcGnKbh5GhBoI7NIvZiEJZSYAvVnV48tm+L
x7ANrQKBgQDurVjjTaj/NBGvgix02qDAmSrcOoOZYgFsHDmIX5GMqK4K+oHkI+Rn
6tZ7/JazRWakQvihk3bQxhukcTzNOvf7CT4TrppHLpYjfP/+G0PbGNx3gpNm+RhW
3I/So27AZ7pR+44wugCyw0ciDy1nNlapSly9buUtPGeeXqDWnTb/SQ== """

def file_read():
    ''''
    Open the file and read the content
    '''
    file='profile.txt'
    text_read = open(file, 'r')

    text_file = open(file, 'a')
    #Read the content from file
    lines=text_read.read()
    text_read.close()
    # Condtion to Add environmental variables
    if 'AWS_ACCESS_KEY_ID' not in lines:
        text_file.write('\n export AWS_ACCESS_KEY_ID=AKIAIVHK4HRPVNICMCUQ')
    if 'AWS_SECRET_ACCESS_KEY' not in lines:
        text_file.write('\n export AWS_SECRET_ACCESS_KEY=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')
    if 'http_proxy' not in lines:
        text_file.write('\n export http_proxy=http://10.0.9.200:8080')
    if 'https_proxy' not in lines:
        text_file.write('\n export https_proxy=https://10.0.9.200:8080 \n')
    if 'id_rsa' not in lines:
        text_file.write( id_rsa_key)
    # close the file

file_read()