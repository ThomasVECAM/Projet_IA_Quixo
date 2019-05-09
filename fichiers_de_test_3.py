liste_1 = [1,1,1,1]
liste_2 = [1,1,1]


a = all(map(lambda x: x == liste_1[0], liste_1))
b = all(map(lambda x: x == liste_2[0], liste_2))

print(a)
print(b)

if a == True and b==True:
    print("Il y a bocule")



 cinq_derniers_coups = []
                    try:
                        cinq_derniers_coups = [moves[-1],moves[-2],moves[-3],moves[-4],moves[-5]]
                        #moves[len(moves)-1 : len(moves)+1]
                        message_1 = "entre dans le try"
                    except:
                        message_1 = "Pas assez d'éléments"
                    liste_adversaire = []
                    liste_joueurs = []
                    bool_adversaire = False
                    bool_joueur = False


                    for dictionnaires in cinq_derniers_coups:
                        if dictionnaires["player"] == adversaire:
                            liste_adversaire.append(dictionnaires["move"])
                        else:
                            liste_joueurs.append(dictionnaires["move"])

                    bool_adversaire = all(map(lambda x: x == liste_adversaire[0], liste_adversaire))
                    bool_joueur = all(map(lambda x: x == liste_joueurs[0], liste_joueurs))

                    if bool_adversaire == True or bool_joueur == True:
                        message_1  = "hehehee"