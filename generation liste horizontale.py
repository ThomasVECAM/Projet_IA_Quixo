def build_horizontal(liste):
    avancement_liste = 0
    coefficient_avancement = 1
    liste_ligne = []
    while avancement_liste < 25:
        ligne = []
        while avancement_liste < (coefficient_avancement * 5) and avancement_liste < 25:
            ligne.append(liste[avancement_liste])
            avancement_liste += 1
        coefficient_avancement += 1
        liste_ligne.append(ligne)


    return liste_ligne


liste = []

print(str(25))
for e in range(25):
    text = "list_to_convert[",e,"]"
    liste.append(str(text))

print(liste)

