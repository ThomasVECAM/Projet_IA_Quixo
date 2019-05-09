liste_1 = [1,1,1,1]
liste_2 = [1,1,1]


a = all(map(lambda x: x == liste_1[0], liste_1))
b = all(map(lambda x: x == liste_2[0], liste_1))

print(a)
print(b)

if a == True and b==True:
    print("Il y a bocule")