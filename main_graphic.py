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
from car import *
import graphique
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

    graphGrid = graphique.Graphic(self.gameGrid, self.top, player, ngrid)
    self.content = [RushLabel(text="GRILLE " + str(self.gameGrid.key)),
                    graphGrid.canvas,
                    Menubutton(text="NIVEAU SUIVANT", command = lambda : self.skip()),
                    Menubutton(text="MENU PRINCIPAL", command = lambda : Main_menu(self.top, self.player)),
                    Menubutton(text="CHANGER DE NIVEAU", command = lambda : Grid_Choice(self.top, self.player))]
                    
    self.trials = graphGrid.trials              #trials iterator
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

#class carscale(scale)    
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
    for player in self.players : self.content.append(Menubutton (text=player, command = lambda i=player: self.playerchosen(i)))
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
    self.content.append(Menubutton(text="RETOUR", command = lambda : Main_menu(self.top, self.player)))  
    self.top.update(self.content)
    
class Score_List:#---------> OK
  def __init__(self, top , player):
    self.top = top
    self.d = sorted(get_players_points(), key=lambda scores: scores[1],reverse=True)
    self.player = player
    self.content = []
    i = 1
    for item in self.d:
      self.content.append(RushLabel(text=str(i) + ". " + str(item[0]) +" : " +str(item[1]) + " points"))
      i+=1
    self.content.append(Menubutton(text="RETOUR", command = lambda : Main_menu(self.top, self.player)))  
    self.top.update(self.content)

class New_Player:#---------> OK
  def __init__(self, prev, action):
    self.top = prev.top
    self.player = prev.player
    self.prev = prev
    self.action = action
    self.players = playernames()
    self.e = Entry()
    self.content = [RushLabel(text="Pseudo :"),
                    self.e,
                    Menubutton(text="VALIDER", command = lambda : self.validate(self.e.get())),
                    Menubutton(text="RETOUR", command = lambda : Main_menu(self.top, self.player))]
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
      self.content = [RushLabel(text="Avez-vous déjà une partie d'enregistrée?"),
                      Menubutton(text="OUI", command= lambda : self.getexisting()),
                      Menubutton(text="NON", command= lambda :  self.getnew())]
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
    self.content = [RushLabel(text="Voulez vous sauvegarder votre partie ?"),
                    Menubutton(text="OUI", command= lambda : Save(self, action = "self.top.close()")),
                    Menubutton(text="NON", command= lambda : self.top.close())]
    self.top.update(self.content)  
    
class Win_Menu:#---------> OK
  def __init__(self, top , player, ngrid, trials):
    self.top = top
    self.player = player
    self.ngrid = ngrid
    self.trials = trials   
    self.content = [RushLabel(text="Winner !  \nNombre de coups : %i" % self.trials),
                    Menubutton(text = "CHOISIR UNE GRILLE", command = lambda : Grid_Choice(self.top, self.player)),
                    Menubutton(text = "MENU PRINCIPAL", command = lambda : Main_menu(self.top, self.player))]

    if (ngrid != 40):
      self.content.append(Menubutton(text = "GRILLE SUIVANTE", command = lambda : Start_Level(self.top, self.player, self.ngrid+1)))
    self.top.update(self.content)  
    
class Main_menu:#---------> OK
  def __init__(self, cw, player):
    self.top = cw
    self.player = player
    self.content = [Menubutton (text= "JOUER", command = lambda : Start_Level(self.top, self.player, 1)),
                    Menubutton (text= "CHOISIR UN NIVEAU", command = lambda : Grid_Choice(self.top, self.player)),
                    Menubutton (text= "CHARGER UNE PARTIE", command = self.loadplayer_callback),
                    Menubutton (text= "SAUVEGARDER", command = lambda : Save(self)),
                    Menubutton (text= "MEILLEURS SCORES", command = lambda : Score_List(self.top,self.player)),
                    Menubutton (text= "QUITTER", command = lambda : self.quit_callback())]
    self.top.update(self.content)  
      
  def loadplayer_callback(self):
    Player_Choice(self, "Grid_Choice(self.top, self.player)")
    
  def quit_callback(self):
    AskForSave(self.top, self.player)
    
class content_window :
  def __init__(self, top):
    self.header = Label(text = "RUSH HOUR", font=("Courier", 60, "bold"), fg="#333", bg="#FFF")
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




#-----------------------Customized widgets-------------------------#    
class Menubutton(Button):
  def __init__(self, *args, **kwargs):
    Button.__init__(self,  
                    height=2,
                    width = 30,
                    fg = "#333",
                    activeforeground = "#F55",
                    bg = "#fff",
                    activebackground="#fff",
                    font =("Courier", 20),
                    relief = FLAT,
                    overrelief = FLAT,
                    highlightthickness=0,
                    borderwidth=0,
                    *args, **kwargs)
    
class RushLabel(Label):
  def __init__(self, *args, **kwargs):
    Label.__init__(self, *args, **kwargs,
                   height=2,
                   fg = "#333",
                   bg = "#fff",
                   font =("Courier", 20))
                   
                  

    
def main():#---------> OK
  # INIT
  fenetre = Tk()
  fenetre.geometry("800x800")
  fenetre.configure(background="#fff")
  fenetre.title("Rush Hour, by Clara Rigaud and Gwaldys Léré")
  content = content_window(fenetre)
  Main_menu(content, Player())
  fenetre.mainloop()

  
# ==============================================================================
if __name__ == '__main__':
  main()
# ==============================================================================
