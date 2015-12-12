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
from players import *
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
    print("Il n'y a pas de voiture de ce nom")
   
def start_level(ngrid, player):
  """ Boucle pour un niveau de jeu"""
  gameGrid = Grille(ngrid)
  trials = 0              #trials iterator
  while(True):
    trials +=1            #à chaque tour de boucle, un essai supplémentaire 
    print(grid(["GRILLE " + str(gameGrid.key)],inner=False))
    print(grid(gameGrid.toArray(), size=3))
    command = ""
    while len(command) != 2: #redemande tant que l'utilisateur ne rentre pas 2 lettres
      command = input("Entrez le mouvement (nom de la voiture et nom de la direction en anglais (ex: ZU, ZD, ZL, ZR)) : \n OP pour acceder aux options\n> ")
    if command == "OP":
      if(level_option_menu(player, gameGrid.key)==False):
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
        
def playerchoice(player): #OK
  """charger un joueur existant, renvoie l'objet joueur associé au nom entré"""
  players = playernames()
  for player in players : print("- "+player) 
  entree = input("Quel est votre pseudo ? \n> ")
  while entree not in players:
    entree = input("Il n'y a pas de joueur de ce nom ... \nQuel est votre pseudo ?\n> ")
  return Player(entree)
  
def gridchoice(player):  #OK   #implémenter une option retourmenu pourrait être cool
  """ Permet à l'utilisateur de choisir une grille, renvoie le numero de grille choisi """
  mapNum = ["%s" %i for i in range(1,41)]
  gridnumber=0
  display = [[],[]]
  for i in range (1,41):
    if player.hasplayed(i):
      score = str(player.get_player_grid_score(i))
    else:
      score = "X"
    display[0].append(i)
    display[1].append(score)
    if i==10:
      print("FACILE")
      print(grid([display[0][0:10],display[1][0:10]], size=3))
    if i==20:
      print("MOYEN")
      print(grid([display[0][10:20],display[1][10:20]], size=3))
    if i==30:
      print("DIFFICILE")
      print(grid([display[0][20:30],display[1][20:30]], size=3))
    if i==40:
      print("EXPERT")
      print(grid([display[0][30:40],display[1][30:40]], size=3))
  while str(gridnumber) not in mapNum:
    gridnumber = int(input("Quelle grille souhaitez-vous utiliser? (de 1 à 40) :\n> "))
  return gridnumber

def classement():
  d = get_players_points()
  d = sorted(d, key=lambda scores: scores[1],reverse=True)
  d.insert(0, ("NOM","SCORE"))
  print(grid(["     CLASSEMENT     "], inner=False))
  print(grid(d,size=19, inner=False))

def scoreslist(player): #TODO
  classement()
  if player.islogged():
    print("Pour voir vos scores par grille <monscore>")
  entree = input("Pour retourner au menu : <retour>\n> ")
  if entree == "retour":
    main_menu(player)

def newplayer(player):  #OK
  pseudo = input("Pseudo :\n> ")
  players = playernames()
  while (pseudo in players):
    pseudo = input("Désolée, ce nom est déjà pris ... :'( \nPseudo :\n> ")
  player.setname(pseudo)
  
def save(player): #OK
  if not(player.islogged()):
    entree = input("Avez vous vous déjà une partie d'enregistrée? <Oui/non>\n> ")
    if entree== "oui":
      player2 = playerchoice(player)
      player.sync(player2)
    else:
      newplayer(player)
  player.saveinfile()
  return True
  
def quitgame(player):  #OK
  entree = input("Voulez vous sauvegarder votre partie ?  <oui>/<non>\n> ")
  if entree == "oui":
    save(player)
    print("sauvegardé !")
  if player.islogged():
    print("Au revoir " + player.name +" !")
  else :
    print("Au revoir !")

def win_menu(ngrid, player, trials): #OK
  """ S'affiche lorsqu'une grille est terminée, choix de passer au niveau suivant, choisir un autre niveau ou retourner au menu principal"""
  print("WINNER !! \nNombre de coups :", trials)
  player.set_player_grid_score(ngrid, trials)
  
  if (ngrid == 40):
    entree = input("Bravo ! Vous avez terminé le jeu !\n" + grid([["CHOISIR UN NIVEAU","choixniveau"],["MENU PRINCIPAL","menu"]]) + "\n>") 
  else:
    entree = input(grid([["GRILLE SUIVANTE","next"],["CHOISIR UN NIVEAU","choixniveau"],["MENU PRINCIPAL","menu"]]) +"\n> ")

  if entree=="next":
    start_level(ngrid+1, player)
  elif entree=="choixniveau":
    start_level(gridchoice(player), player)
  elif entree=="menu":
    main_menu(player)

def level_option_menu(player, ngrid):  #OK
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
      start_level(ngrid+1,player)
    return False
  elif choixaction == "choixniveau":
    start_level(gridchoice(player), player)
    return False
  elif choixaction == "retour":
    return True

def main_menu(player):  #OK
  """ Choix de retourner jouer la première grille, choisir un niveau, charger une partie, voir les scores, quitter"""
  print(grid(["     RUSH HOUR     "], inner=False))
  choixaction = ""
  #Verification de saisie
  while choixaction not in ["jouer","choixniveau","charger","sauver", "scores","quit"]:
    choixaction = input(grid([
    ["ACTION","Entrez"],
    ["JOUER","jouer"],
    ["CHOISIR UN NIVEAU","choixniveau"],
    ["CHARGER UNE PARTIE","charger"],
    ["SAUVGARDER LA PARTIE","sauver"],
    ["MEILLEURS SCORES","scores"],
    ["QUITTER","quit"]], inner=False)+"\n> ")




  if choixaction == "jouer" :
    start_level(1, player)
    
  elif choixaction == "choixniveau":
    start_level(gridchoice(player), player)
  elif choixaction == "charger" :
    player = playerchoice(player)
    start_level(gridchoice(player), player)
  elif choixaction == "sauver":
    if save(player):
      print("Sauvegardé !")
      main_menu(player)
  elif choixaction == "scores" :
    scoreslist(player)
  elif choixaction == "quit":
    quitgame(player)
    
def main():
  # INIT
  player = Player()
  main_menu(player)

# ==============================================================================
if __name__ == '__main__':
  main()
# ==============================================================================
