import cherrypy
import sys
import random

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

#Lire les fonctions dans l'ordre suivant
      #  1) Move
      #  2) check move()
      #  3) qui_suis je pas















    #Informations sur le jeu (déà retirée du dico par facilité)
        game = body["game"]
        moi = body["you"]
        joueurs = body["players"]

        #Informations sur moi et joueurs : le premier de la liste joueurs est le joeur '0" dans la liste de
        # l'état du jeu : game = body['game']. L'autre est le joueur 1.




        def qui_suis_je_pas (): #il ne faut pas jouer les jetons de l'autre... utilisé plus loin
            if joueurs[0]== moi: #où joueurs est la liste des joueurs et donc si le premier élement de cette liste
                                    #est moi, alors je ne suis pas le joueur 1. (logique inversée
                                    #qui au début dans ma manière de réfléchir avait du sens
                return 1
            return 0

        def check_move (cube, direction):
            forbidden_moves = {"cube": [6, 7, 8, 11, 12, 13, 16, 17, 18],
                               "direction": {"N": [0, 1, 2, 3, 4], "S": [20, 21, 22, 23, 24], "E": [4, 9, 14, 19, 24],
                                             "W": [0, 5, 10, 15, 20]}}

            if cube in forbidden_moves["cube"]:  #vérifier qu'on déplace bien un cube sur les bords
                return False

            elif game[cube] == qui_suis_je_pas(): #vérifier qu'on déplace bien son cube. Le truc c'est que le joueur
                #qu'on est on le garde jusqu'à la fin... C'est pas optimisé ici. il refait à chaque tour
                return False

            elif cube in forbidden_moves["direction"][direction]:
                return False

            return True

        def move():
            recherche = True
            while recherche == True:
                a = random.choice(list(range(25)))
                b = random.choice(["N", "S", "E", "W"])

                authorized = check_move(a,b)
                if authorized==True:
                    return {"cube": a,"direction": b}

        return {"move": move(),"message":"Coucou"}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())
