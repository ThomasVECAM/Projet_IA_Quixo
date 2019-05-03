def build_horizontal(liste):

    avancement_liste = 0
    coefficient_avancement = 1
    liste_ligne=[]

    while avancement_liste < 25:
        ligne = []
        while avancement_liste < (coefficient_avancement*5) and avancement_liste<25:
            ligne.append(liste[avancement_liste])
            avancement_liste +=1
        coefficient_avancement +=1
        liste_ligne.append(ligne)

    return liste_ligne
def build_vertical(liste):

    avancement_liste = 0
    coefficient_avancement = 0
    liste_vertical = []

    a=0

    while a <5:
        colonne = []
        i = 0
        while i < 5:
            colonne.append(liste[5*i + coefficient_avancement])
            i +=1
        liste_vertical.append(colonne)
        coefficient_avancement +=1
        a+=1

    return liste_vertical
def build_diag (game_list):
    return [[game_list[0],game_list[6],game_list[12],game_list[18],game_list[24]],
            [game_list[4],game_list[8],game_list[12],game_list[16],game_list[20]]]
def build_dictionnary(liste_a_convertir):
    dico =  {"vertical": build_vertical(liste_a_convertir), "horizontal": build_horizontal(liste_a_convertir), "diagonale": build_diag(liste_a_convertir)}
    print(dico["vertical"])

def preview (cube, direction):

    jeu_list = list(range(25))
    build_dictionnary(jeu_list)
    if direction == "E":
        jeu_list.insert(cube +(4-(cube%5)),jeu_list.pop(cube))
        build_dictionnary(jeu_list)

    if direction == "W":
        jeu_list.insert(cube - (cube%5),jeu_list.pop(cube))
        build_dictionnary(jeu_list)

    elif direction =="N":
        #niveau = cube%5
        for elements in range(cube//5): # for elements in range(niveau):

            copy_list = jeu_list.copy()
            jeu_list[cube] = copy_list[5*elements + cube%5]
            jeu_list[5*elements + cube%5] = copy_list[cube]

            build_dictionnary(jeu_list)

    elif direction == "S":
        elements= 4
        for e in range(4 - cube // 5):  # for elements in range(niveau):
            copy_list = jeu_list.copy()
            jeu_list[cube] = copy_list[5 * elements + cube % 5]
            jeu_list[5 * elements + cube % 5] = copy_list[cube]
            elements +=(-1)

        build_dictionnary(jeu_list)



preview(17,"S")