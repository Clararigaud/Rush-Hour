# ==============================================================================
"""RUSH HOUR : get your car out of this mess !"""
# ==============================================================================
__author__  = "Gwladys Léré, Clara Rigaud"
__version__ = "3.0"
__date__    = "2015-12-13"
__usage__   = """"""
# ==============================================================================
from ezCLI import *
from grid import *
import json
# ------------------------------------------------------------------------------
def error_msg(code):
  """ methode d'affichage des messages d'erreur """
  assert isinstance(code, (str)), "<code> must be an str"
  if code == "outofstreet":
    print("Il faut rester sur la route !")
  elif code == "occupied":
    print("Deja une voiture ici !")
  elif code == "wrongdir":
    print("Cette voiture ne peut pas rouler dans cette direction")
  elif code == "nocar":
    print("Il n'y a pas de voiture à ce nom")
   
def game(ngrid, player):
  """ gère les fonctions appelées pour le déplacement d'une voiture"""
    gdicts = json.load(open('grilles.json'))
    gdict = gdicts[str(ngrid)]
    gameGrid = Grid(gdict, ngrid)

    trials = 0              #trials iterator
    while(True):
      trials +=1            #à chaque tour de boucle, un essai supplémentaire 
      print(grid(["GRILLE " + str(gameGrid.key)],inner=False))
      print(grid(gameGrid.toArray(), size=3))
      command = ""
      while len(command) != 2: #redemande tant que l'utilisateur ne rentre pas 2 lettres
        command = input("Entrez le mouvement (nom de la voiture et nom de la direction en anglais (ex: ZU, ZD, ZL, ZR)) : \n OP pour acceder aux options\n> ")
      if command == "OP":
        if(option_menu(player, gameGrid.key)==False):
          break   
      else:  
        carName = command[0].upper()
        direc = command[1].upper()
        if carName in gameGrid.cars:
          car = gameGrid.cars[carName]  #Vérifie si le nom entré par l'utilisateur correspond bien à une voiture
        else:
          car = None #si l'utilisateur n'a pas écrit le nom d'une voiture sur la grille, vaut None
        result = gameGrid.move(car, direc) #renvoie une str avec le nom de l'erreur s'il y en a
        error_msg(result)
        if result == "win":
          win_menu(ngrid, player, trials)
          break
          

def playerchoice(): #TODO
  print("\n --- indisponible pour le moment ---\n")
  entree = input("Quel est votre pseudo ?")
  return -1 

def gridchoice(player):  #OK
  """ Permet à l'utilisateur de choisir une grille, renvoie le numero de grille choisi """
  mapNum = ["%s" %i for i in range(1,41)]
  gridnumber = int(input("Quelle grille souhaitez-vous utiliser? (de 1 à 40) :"))

  while str(gridnumber) not in mapNum:
    print("Il y a 40 grilles donc rentrez un numéro compris entre 1 et 40")
    gridnumber = int(input("Quelle grille souhaitez-vous utiliser? (de 1 à 40) :"))
  return gridnumber

def scoreslist(player): #TODO
  print("\n --- indisponible pour le moment ---\n")
  main_menu(player)
   
def savegame(player, ngrid, trials): #TODO
  return True

def savenewgame(): #TODO
  print("\n --- indisponible pour le moment ---\n") 
  #pseudo = input("Pseudo : ")  
  quitgame(player)
  
def quitgame(player):  #OK
  if player == -1:
    entree = input("Voulez vous sauvegarder votre partie ?\n> ")
    if entree == "oui":
      savenewgame() 
  print("Au revoir !")

def win_menu(ngrid, player, trials): #OK
  """ S'affiche lorsqu'une grille est terminée, choix de passer au niveau suivant, choisir un autre niveau ou retourner au menu principal"""
  print("WINNER !! \nNombre de coups :", trials)
  savegame(player, ngrid, trials)
  
  if (ngrid == 40):
    entree = input("Bravo ! Vous avez terminé le jeu !\n" + grid([["CHOISIR UN NIVEAU","choixniveau"],["MENU PRINCIPAL","menu"]]) + "\n>") 
  else:
    entree = input(grid([["GRILLE SUIVANTE","next"],["CHOISIR UN NIVEAU","choixniveau"],["MENU PRINCIPAL","menu"]]) +"\n> ")

  if entree=="next":
    game(ngrid+1, player)
  elif entree=="choixniveau":
    game(gridchoice(player), player)
  elif entree=="menu":
    main_menu(player)

def option_menu(player, ngrid):  #OK
  """ Choix de,  retourner au menu principal, sauter le niveau, choisir un autre niveau, retour à la grille"""
  choixaction = ""
  while choixaction not in ["menu", "passer", "choixniveau","retour"]:
    choixaction= input(grid(["OPTIONS"], inner=False)+"\n"+
	grid([["ACTION","Entrez"],
    ["PASSER CE NIVEAU","passer"],
    ["MENU PRINCIPAL","menu"],
    ["CHOISIR UN AUTRE NIVEAU","choixniveau"],
    ["RETOUR","retour"]], inner=False)+"\n> ")
  if choixaction == "menu":
    main_menu(player)
    return False
  elif choixaction == "passer":
    if ngrid == 40 :
      main_menu(player)
    else:
      game(ngrid+1,player)
    return False
  elif choixaction == "choixniveau":
    game(gridchoice(player), player)
    return False
  elif choixaction == "retour":
    return True

def main_menu(player):  #OK
  """ Choix de retourner jouer la première grille, choisir un niveau, charger une partie, voir les scores, quitter"""
  choixaction = ""
  #Verification de saisie
  while choixaction not in ["jouer","choixniveau","charger", "scores","quit"]:
    choixaction = input(grid([
    ["ACTION","Entrez"],
    ["JOUER","jouer"],
    ["CHOISIR UN NIVEAU","choixniveau"],
    ["CHARGER UNE PARTIE","charger"],
    ["MEILLEURS SCORES","scores"],
    ["QUITTER","quit"]], inner=False)+"\n> ")
  if choixaction == "jouer" :
    game(1, player)
  elif choixaction == "choixniveau":
    game(gridchoice(player), player)
  elif choixaction == "charger" :
    player = playerchoice()
    game(gridchoice(player), player)
  elif choixaction == "scores" :
    scoreslist(player)
  elif choixaction == "quit":
    quitgame(player)
    
def main():
  print(grid(["     RUSH HOUR     "], inner=False))
  # INIT
  player = -1 #nouveau joueur
  main_menu(player) 

# ==============================================================================
if __name__ == '__main__':
  main()
# ==============================================================================
