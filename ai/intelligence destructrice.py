import cherrypy
import sys

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

        return {"move":{"cube": 3, "direction": "S"}}



        self.body = cherrypy.request.json
        self.game = body["game"]
        self.moi = body["you"]
        self.joueurs = body["players"]

        if joueurs[0] == self.moi:
            self.player = 0
            self.adversaire = 1
        else:
            self.player = 1
            self.adversaire = 0

        #return {"move": self.moves()}


    def check_move (self, cube, direction):
        if self.game[cube] == self.adversaire:
            return False
        return True

    def analyse_dico(self,dictionary):
        analytic_dictionary = dict()
        liste_result = []
        for liste in dictionary:
            liste_principal = (dictionary[liste])
            for sous_liste in liste_principal:
                tot = 0
                for e in sous_liste:
                    if e == self.player:
                        tot += 1
                liste_result.append(tot)
        maximum = max(liste_result)
        total = sum(liste_result)
    #------------------------------------------------

        liste_result = []
        for liste in dictionary:
            liste_principal = (dictionary[liste])
            for sous_liste in liste_principal:
                tot = 0
                for e in sous_liste:
                    if e == self.adversaire:
                        tot += 1
                liste_result.append(tot)
        maximum_adversaire = max(liste_result)
        total_adversaire = sum(liste_result)

        return {"moi":{"maximum": maximum,"total": total,"score": total*maximum},
                "adversaire":{"maximum": maximum_adversaire,"total":total_adversaire,"score": total_adversaire*maximum_adversaire}}

    def build_dictionnary(self, liste_a_convertir):
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

        def build_vertical(liste):
            avancement_liste = 0
            coefficient_avancement = 0
            liste_vertical = []
            a = 0
            while a < 5:
                colonne = []
                i = 0
                while i < 5:
                    colonne.append(liste[5 * i + coefficient_avancement])
                    i += 1
                liste_vertical.append(colonne)
                coefficient_avancement += 1
                a += 1

            return liste_vertical

        def build_diag(game_list):
            return [[game_list[0], game_list[6], game_list[12], game_list[18], game_list[24]],
                    [game_list[4], game_list[8], game_list[12], game_list[16], game_list[20]]]

        dico =  {"vertical": build_vertical(liste_a_convertir), "horizontal": build_horizontal(liste_a_convertir), "diagonale": build_diag(liste_a_convertir)}

        return self.analyse_dico(dico)

    def preview (self, cube, direction):
        jeu_list = self.game
        jeu_list[cube] = self.player

        if direction == "E":
            jeu_list.insert(cube +(4-(cube%5)),jeu_list.pop(cube))
        elif direction == "W":
            jeu_list.insert(cube - (cube%5),jeu_list.pop(cube))
        elif direction =="N":
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
        return self.build_dictionnary(jeu_list)

    def moves(self):
        maximum = 0
        score = 0
        liste_coup_possible = [(0, 'S'), (0, 'E'), (1, 'S'), (1, 'E'), (1, 'W'), (2, 'S'), (2, 'E'), (2, 'W'), (3, 'S'), (3, 'E'),
         (3, 'W'), (4, 'S'), (4, 'W'), (5, 'N'), (5, 'S'), (5, 'E'), (9, 'N'), (9, 'S'), (9, 'W'), (10, 'N'),
         (10, 'S'), (10, 'E'), (14, 'N'), (14, 'S'), (14, 'W'), (15, 'N'), (15, 'S'), (15, 'E'), (19, 'N'),
         (19, 'S'), (19, 'W'), (20, 'N'), (20, 'E'), (21, 'N'), (21, 'E'), (21, 'W'), (22, 'N'), (22, 'E'),
         (22, 'W'), (23, 'N'), (23, 'E'), (23, 'W'), (24, 'N'), (24, 'W')]

        for elements in liste_coup_possible:
            a,b = elements

            authorized = self.check_move(a,b)

            if authorized == True:
                dico = self.preview(a, b)
                if dico["moi"]['maximum'] > maximum:

                    if dico["adversaire"]["maximum"] == 5:
                        pass
                    else:
                        coup = {"cube": a, "direction": b}
                        maximum = dico["moi"]['maximum']

        return coup"""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())