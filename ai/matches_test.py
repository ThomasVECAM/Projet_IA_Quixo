import cherrypy
import sys
import random


#test

class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''

        body = cherrypy.request.json

    #Informations sur le jeu (déà retirée du dico par facilité)
        game = body["game"]
        moi = body["you"]
        joueurs = body["players"]

        if joueurs[0] == moi:
            signe = 'X'
            player = 0
            adversaire = 1
        else:
            signe = 'O'
            player = 1
            adversaire = 0

        def check_move (cube, direction):
            #forbidden_moves = {"cube": [6, 7, 8, 11, 12, 13, 16, 17, 18],
             #                  "direction": {"N": [0, 1, 2, 3, 4], "S": [20, 21, 22, 23, 24], "E": [4, 9, 14, 19, 24],
              #                               "W": [0, 5, 10, 15, 20]}}

            #if cube in forbidden_moves["cube"]:  #vérifier qu'on déplace bien un cube sur les bords
             #   return False

            if game[cube] == adversaire:
                return False

            #elif cube in forbidden_moves["direction"][direction]:
            #    return False
            return True

# ---------------------------------

        def analyse_dico(dictionary): #dictionnaire de type : {"horizontal" : ... , "vertical" ... , "diagonal"
            analytic_dictionary = dict()
            liste_result = []
            liste_clé = ["vertical","horizontal","diagonale"]
            for liste in liste_clé:
                liste_principal = (dictionary[liste])
                for sous_liste in liste_principal:
                    tot = 0
                    for e in sous_liste:
                        if e == player:
                            tot += 1
                    liste_result.append(tot)
            maximum = max(liste_result)
            total = sum(liste_result)

            return {"maximum": maximum,"total": total,"score": total*maximum,"move":dictionary["move"]}

        def build_horizontal(liste):
            avancement_liste = 0
            coefficient_avancement = 1
            liste_ligne=[]
            while avancement_liste < 25:
                ligne = []
                while avancement_liste < (coefficient_avancement*5) and avancement_liste<25:
                    ligne.append(liste[avancement_liste])
                    avancement_liste += 1
                coefficient_avancement += 1
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

        def build_dictionnary(liste_a_convertir, cube, direction):
            dico =  {"vertical": build_vertical(liste_a_convertir), "horizontal": build_horizontal(liste_a_convertir), "diagonale": build_diag(liste_a_convertir),"move":{"cube":cube, "direction":direction}}
            return analyse_dico(dico)
            #print(liste_a_convertir)
            # print(dico)


        def preview (jeu_list_original, cube, direction):
            jeu_list = jeu_list_original.copy()
            jeu_list[cube] = player
            if direction == "E":
                jeu_list.insert(cube +(4-(cube%5)),jeu_list.pop(cube))
            elif direction == "W":
                jeu_list.insert(cube - (cube%5),jeu_list.pop(cube))
            elif direction =="N":
                #niveau = cube%5
                for elements in range(cube//5): # for elements in range(niveau):
                    copy_list = jeu_list.copy()
                    jeu_list[cube] = copy_list[5*elements + cube%5]
                    jeu_list[5*elements + cube%5] = copy_list[cube]
            elif direction == "S":
                elements= 4
                for e in range(4 - cube // 5):  # for elements in range(niveau):
                    copy_list = jeu_list.copy()
                    jeu_list[cube] = copy_list[5 * elements + cube % 5]
                    jeu_list[5 * elements + cube % 5] = copy_list[cube]
                    elements -= 1
            return build_dictionnary(jeu_list, cube, direction)

# ---------------------------

        def move():
            maximum = 0
            score = 0
            liste_coup_possible = [(0, 'S'), (0, 'E'), (1, 'S'), (1, 'E'), (1, 'W'), (2, 'S'), (2, 'E'), (2, 'W'), (3, 'S'), (3, 'E'),
             (3, 'W'), (4, 'S'), (4, 'W'), (5, 'N'), (5, 'S'), (5, 'E'), (9, 'N'), (9, 'S'), (9, 'W'), (10, 'N'),
             (10, 'S'), (10, 'E'), (14, 'N'), (14, 'S'), (14, 'W'), (15, 'N'), (15, 'S'), (15, 'E'), (19, 'N'),
             (19, 'S'), (19, 'W'), (20, 'N'), (20, 'E'), (21, 'N'), (21, 'E'), (21, 'W'), (22, 'N'), (22, 'E'),
             (22, 'W'), (23, 'N'), (23, 'E'), (23, 'W'), (24, 'N'), (24, 'W')]

            for elements in liste_coup_possible:
                a,b = elements

                authorized = check_move(a,b)
                if authorized == True:
                    dico = preview(game, a, b)
                    # print(dico)
                    if dico['maximum'] > maximum:
                        maximum = dico['maximum']
                        coup = {"cube": a, "direction": b}
                        maximum = dico['maximum']

            return coup

        print({"move": move()})
        return {"move": move(),"message":signe}





if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())
