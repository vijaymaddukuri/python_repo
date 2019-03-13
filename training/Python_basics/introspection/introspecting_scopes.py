globals()['vj'] = [123]

print(vj)
print(type(vj))

name = 'vijay'
city = 'Bangalore'
country = "India"

print("{name} works in {city}, which is located in {country}".format(**locals()))
