import pickle
fileLocation=r'D:\new\vijay.txt'
myfav={"cricketer":"sachin", "place":"Yanam", "pet": "cherry"}
pickle.dump(myfav,open(fileLocation,"wb"))
myfav = pickle.load( open( fileLocation, "rb" ) )
print(myfav)