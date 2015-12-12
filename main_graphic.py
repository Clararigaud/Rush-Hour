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
from tkinter import *
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
         
class Start_Level:
  def __init__(self, top , player , ngrid):
    self.ngrid = ngrid
    self.top = top
    self.player = player
    self.gameGrid = Grille(self.ngrid)
    self.content = [Label(text="GRILLE " + str(self.gameGrid.key)),
                    Label(text=grid(self.gameGrid.toArray(), size=3)),
                    Button(text="Niveau suivant", command = lambda : self.skip()),
                    Button(text="Menu principal", command = lambda : Main_menu(self.top, self.player)),
                    Button(text="Changer de niveau", command = lambda : Grid_Choice(self.top, self.player))]
                    
    self.trials = 0              #trials iterator
    self.top.update(self.content)
##    while(True):
##      command = ""
##      while len(command) != 2: #redemande tant que l'utilisateur ne rentre pas 2 lettres
##        command = input("Entrez le mouvement (nom de la voiture et nom de la direction en anglais (ex: ZU, ZD, ZL, ZR)) : \n OP pour acceder aux options\n> ")
##      carName = command[0].upper()
##      direc = command[1].upper()
##      if carName in gameGrid.cars:
##        car = gameGrid.cars[carName]  #Vérifie si le nom entré par l'utilisateur correspond bien à une voiture
##      else:
##        car = None #si l'utilisateur n'a pas écrit le nom d'une voiture sur la grille, vaut None
##        result = gameGrid.move(car, direc) #renvoie une str avec le nom de l'erreur s'il y en a
##        error_msg(result)
##        if result == "win":
##          Win_Menu(self.top, self.player, self.ngrid, self.trials)
##          break
##      self.trials +=1            #à chaque tour de boucle, un essai supplémentaire
##
    
  def skip(self):
    if self.ngrid == 40 :
      Main_menu(self.top, self.player)
    else:
      Start_Level(self.top, self.player, self.ngrid+1)

class Player_Choice: #---------> OK
  def __init__(self, prev, action):
    self.top = prev.top
    self.prev = prev
    self.players = playernames()
    self.player = prev.player
    self.action = action
    self.content = []
    for player in self.players : self.content.append(Button (text=player, command = lambda i=player: self.playerchosen(i)))
    self.top.update(self.content)
    
  def playerchosen(self, player):
    self.player = Player(player)
    eval(self.action)
    
class Grid_Choice:#---------> OK
  def __init__(self, cw, player):
    self.top = cw
    self.player = player
    self.content = []
    for i in range (1,41):
      self.content.append(Button(text = i, command = lambda ngrid=i: Start_Level(self.top, self.player, ngrid)))
    self.top.update(self.content)
    
def classement():
  d = get_players_points()
  d = sorted(d, key=lambda scores: scores[1],reverse=True)
  d.insert(0, ("NOM","SCORE"))
  print(grid(["     CLASSEMENT     "], inner=False))
  print(grid(d,size=19, inner=False))

def scoreslist(player): #TODO
  classement()
  if player.islogged():
    entree = input("Pour retourner au menu : <retour>\n> ")
  if entree == "retour":
    main_menu(player)

class Score_List:
  def __init__(self, top , player):
    self.top = top
    self.d = sorted(get_players_points(), key=lambda scores: scores[1],reverse=True)
    self.player = player
    self.content = []
    i = 1
    for item in self.d:
      self.content.append(Label(text=str(i) + ". " + str(item[0]) +" : " +str(item[1]) + " points"))
      i+=1
    self.content.append(Button(text="Retour", command = lambda : Main_menu(self.top, self.player)))  
    self.top.update(self.content)

class New_Player:#---------> OK
  def __init__(self, prev, action):
    self.top = prev.top
    self.player = prev.player
    self.prev = prev
    self.action = action
    self.players = playernames()
    self.e = Entry()
    self.content = [Label(text="Pseudo :"),
                    self.e,
                    Button(text="Valider", command = lambda : self.validate(self.e.get()))]
    self.top.update(self.content)
    
  def validate(self, entree):
    if entree in self.players:
      self.top.show_error(" Ce nom est déjà pris ... :( ")
      self.e.delete(0, END)
    else :
      self.player.setname(entree)
      eval(self.action)
      
class Save:#---------> OK
  def __init__(self, prev, action="Main_menu(self.top, self.player)"):
    self.top = prev.top
    self.player = prev.player
    self.action = action
    if self.player.islogged():
      self.saveandleave()
    else:
      self.content = [Label(text="Avez-vous déjà une partie d'enregistrée?"),Button(text="oui", command= lambda : self.getexisting()), Button(text="non", command= lambda :  self.getnew())]
      self.top.update(self.content)
      
  def getexisting(self):
    Player_Choice(self, "self.prev.syncandsave(self.player)")

  def syncandsave(self, player2):
    self.player.sync(player2)
    self.saveandleave()
    
  def getnew(self):
    New_Player(self, "self.prev.saveandleave()") 

  def saveandleave(self):
    self.player.saveinfile()
    eval(self.action)

class AskForSave:#---------> OK
  def __init__(self, top, player):
    self.top = top
    self.player = player
    self.content = [Label(text="Voulez vous sauvegarder votre partie ?"),
                    Button(text="Oui", command= lambda : Save(self, action = "self.top.close()")),
                    Button(text="Non", command= lambda : self.top.close())]
    self.top.update(self.content)  
    
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
    
class Win_Menu:
  def __init__(self, top , player, ngrid, trials):
    self.top = top
    self.player = player
    self.ngrid = ngrid
    self.trials = trials   
    self.content = [Label(text="Winner !  \nNombre de coups :" + self.trials),
                    Button(text = "Choisir une grille", command = lambda : Grid_Choice(self.top, self.player)),
                    Button(text = "Menu principal", command = lambda : Main_menu(self.top, self.player))]
    if (ngrid != 40):
      self.content.append(Button(text = "Grille suivante", command = lambda : Start_Level(self.top, self.player, self.ngrid+1)))
    self.top.update(self.content)  
    
class Main_menu:#---------> OK
  def __init__(self, cw, player):
    self.top = cw
    self.player = player
    self.content = [Button (text= "Jouer", command = lambda : Start_Level(self.top, self.player, 1)),
                    Button (text= "Choisir un niveau", command = lambda : Grid_Choice(self.top, self.player)),
                    Button (text= "Charger une partie", command = self.loadplayer_callback),
                    Button (text= "Sauvegarder la partie", command = lambda : Save(self)),
                    Button (text= "Meilleurs scores", command = lambda : Score_List(self.top,self.player)),
                    Button (text= "Quitter", command = lambda : self.quit_callback())]
    self.top.update(self.content)  
      
  def loadplayer_callback(self):
    Player_Choice(self, "Grid_Choice(self.top, self.player)")
    
  def quit_callback(self):
    AskForSave(self.top, self.player)
    
class content_window :
  def __init__(self, top):
    self.header = Label(text = "RUSH HOUR")
    self.body = None
    self.top = top
    self.header.pack()
    self.error = None
  def clear(self):
    if self.body:
      for item in self.body:
          item.pack_forget()
      self.body = None
    if self.error:
      self.error.pack_forget()
      self.error = None
  def update(self,content):
    self.clear()
    self.body = content
    for item in self.body:
        item.pack()

  def show_error(self, string):
    if self.error:
      self.error.pack_forget()
    self.error = Label(text=string)
    self.error.pack()

  def close(self):
    self.top.destroy()

def main():#---------> OK
  # INIT
  fenetre = Tk()
  Main_menu(content_window(fenetre), Player())
  fenetre.mainloop()

  
# ==============================================================================
if __name__ == '__main__':
  main()
# ==============================================================================
