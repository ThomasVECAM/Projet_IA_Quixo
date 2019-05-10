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

        self.game = body["game"]
        self.moi = body["you"]
        self.joueurs = body["players"]
        self.moves = body['moves']

        if self.joueurs[0] == self.moi:
            self.player = 0
            self.adversaire = 1
        else:
            self.player = 1
            self.adversaire = 0

        return {"move": self.mouvement()}

    def analyse_dico(self, dictionary):
        liste_result_player = []
        liste_result_adversaire = []
        for liste in dictionary:
            liste_principal = (dictionary[liste])
            for sous_liste in liste_principal:
                tot_player = 0
                tot_adversaire = 0
                for e in sous_liste:
                    if e == self.player:
                        tot_player += 1
                    elif e == self.adversaire:
                        tot_adversaire += 1
                liste_result_player.append(tot_player)
                liste_result_adversaire.append(tot_adversaire)

        maximum_player = max(liste_result_player)
        maximum_adversaire = max(liste_result_adversaire)
        return {"maximum_player": maximum_player, "maximum_adversaire": maximum_adversaire}

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

        dico = {"vertical": build_vertical(liste_a_convertir), "horizontal": build_horizontal(liste_a_convertir),
                "diagonale": build_diag(liste_a_convertir)}
        return self.analyse_dico(dico)

    def check_move(self, cube):
        if self.game[cube] == self.adversaire:
            return False
        return True

    def preview(self, jeu_list_original, cube, direction):
        jeu_list = jeu_list_original.copy()
        jeu_list[cube] = self.player
        if direction == "E":
            jeu_list.insert(cube + (4 - (cube % 5)), jeu_list.pop(cube))
        elif direction == "W":
            jeu_list.insert(cube - (cube % 5), jeu_list.pop(cube))
        elif direction == "N":
            # niveau = cube%5
            for elements in range(cube // 5):  # for elements in range(niveau):
                copy_list = jeu_list.copy()
                jeu_list[cube] = copy_list[5 * elements + cube % 5]
                jeu_list[5 * elements + cube % 5] = copy_list[cube]
        elif direction == "S":
            elements = 4
            for e in range(4 - cube // 5):  # for elements in range(niveau):
                copy_list = jeu_list.copy()
                jeu_list[cube] = copy_list[5 * elements + cube % 5]
                jeu_list[5 * elements + cube % 5] = copy_list[cube]
                elements -= 1
        return jeu_list

    def mouvement(self):
        maximum_player = 0
        maximum_adversaire = 5
        liste_coup_autorise = [(0, 'S'), (0, 'E'), (1, 'S'), (1, 'E'), (1, 'W'), (2, 'S'), (2, 'E'), (2, 'W'), (3, 'S'),
                               (3, 'E'), (3, 'W'), (4, 'S'), (4, 'W'), (5, 'N'), (5, 'S'), (5, 'E'), (9, 'N'), (9, 'S'),
                               (9, 'W'), (10, 'N'), (10, 'S'), (10, 'E'), (14, 'N'), (14, 'S'), (14, 'W'), (15, 'N'),
                               (15, 'S'), (15, 'E'), (19, 'N'), (19, 'S'), (19, 'W'), (20, 'N'), (20, 'E'), (21, 'N'),
                               (21, 'E'), (21, 'W'), (22, 'N'), (22, 'E'), (22, 'W'), (23, 'N'), (23, 'E'), (23, 'W'),
                               (24, 'N'), (24, 'W')]
        for element in liste_coup_autorise:
            a, b = element
            if self.check_move(a) == True:
                liste_preview = self.preview(self.game, a, b)
                dico = self.build_dictionnary(liste_preview)

                bool_continue = True
                try:
                    cinq_derniers_coups = [moves[-1], moves[-2], moves[-3], moves[-4], moves[-5]]

                    liste_adversaire = []
                    liste_joueurs = []
                    bool_adversaire = False
                    bool_joueur = False

                    for dictionnaires in cinq_derniers_coups:
                        if dictionnaires["player"] == self.adversaire:
                            liste_adversaire.append(dictionnaires["move"])
                        else:
                            liste_joueurs.append(dictionnaires["move"])

                    liste_joueurs.append({'cube': a, 'direction': b})

                    bool_adversaire = all(map(lambda x: x == liste_adversaire[0], liste_adversaire))
                    bool_joueur = all(map(lambda x: x == liste_joueurs[0], liste_joueurs))

                    if bool_adversaire == True and bool_joueur == True and dico['maximum_adversaire'] <= 4:
                        bool_continue = False
                except:
                    pass

                if bool_continue == True:

                    if dico['maximum_player'] > maximum_player and not (dico['maximum_adversaire'] >= 4):
                        maximum_player = dico['maximum_player']
                        maximum_adversaire = dico['maximum_adversaire']
                        coup = {"cube": a, "direction": b}

                    elif dico['maximum_player'] == maximum_player and dico['maximum_adversaire'] < maximum_adversaire:
                        maximum_adversaire = dico['maximum_adversaire']
                        coup = {"cube": a, "direction": b}

        return coup


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())