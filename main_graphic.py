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

# -----------------------------------------------------------------------------
         
class Start_Level:
  def __init__(self, top , player , ngrid):
    self.ngrid = ngrid
    self.top = top
    self.player = player
    self.gameGrid = Grille(self.ngrid)    
    self.content = Frame(bg="#fff", width=800)
    self.content.pack()
    self.header = Frame(self.content,bg="#fff",width=800)
    self.header.pack()
    RushLabel(self.header, text="GRILLE " + str(self.gameGrid.key)).pack(side=LEFT,ipadx=100)
    Menubutton(self.header, text="MENU PRINCIPAL", command = lambda : Main_menu(self.top, self.player)).pack(side=RIGHT, padx=100)
    graphGrid = graphique.Graphic(self.gameGrid,self.top, self.content, player, ngrid)
    graphGrid.canvas.pack()
    self.footer = Frame(self.content,bg="#fff",width=800)
    self.footer.pack(pady=50)
    Menubutton(self.footer, text="NIVEAU SUIVANT", command = lambda : self.skip()).pack(side=LEFT,ipadx=30)
    Menubutton(self.footer, text="CHANGER DE NIVEAU", command = lambda : Grid_Choice(self.top, self.player)).pack(side=RIGHT, padx=30)
    self.top.update(self.content)

  def skip(self):
    if self.ngrid == 40 :
      Main_menu(self.top, self.player)
    else:
      Start_Level(self.top, self.player, self.ngrid+1)

class Player_Choice: 
  def __init__(self, prev, action):
    self.top = prev.top
    self.prev = prev
    self.players = playernames()
    self.player = prev.player
    self.action = action   
    self.content = Frame(bg="#fff")
    self.content.pack()
    self.top.update(self.content)
    
    for player in self.players : Menubutton (self.content, text=player, command = lambda i=player: self.playerchosen(i)).pack()
    Menubutton(self.content, text="ANNULER", command = lambda : Main_menu(self.top, self.player)).pack()
  def playerchosen(self, player):
    self.player = Player(player)
    eval(self.action)

class Grid_Choice:
  def __init__(self, cw, player):
    self.top = cw
    self.player = player
    self.content = Frame(bg="#fff")
    self.content.pack()
    self.top.update(self.content)
    lines = []
    cases=[]
    scores=[]
    for j in range(0,4):
      cases.append([])
      scores.append([])
      if j == 0:
        RushLabel(self.content,text="FACILE").pack()
      elif j==1:
        RushLabel(self.content,text="MOYEN").pack()
      elif j==2:
        RushLabel(self.content,text="DIFFICILE").pack()
      elif j==3:
        RushLabel(self.content,text="EXPERT").pack()      
      lines.append(Frame(self.content, bg="#fff"))
      lines[j].pack()    
      for i in range (j*10+1,(j+1)*10+1):
        scores[j].append([])
        if player.hasplayed(i):
          played = True
          scores[j][i-1-10*j]= str(player.get_player_grid_score(i))+" moves"
        else :
          played = False
          scores[j][i-1-10*j]=""

        cases[j].append([])
        cases[j][i-1-10*j]=(Frame(lines[j], width = 58, height = 70, bg="#fff"))
        cases[j][i-1-10*j].pack(side=LEFT)
        Minigridbutton(i, played, cases[j][i-1-10*j],command = lambda ngrid=i: Start_Level(self.top, self.player, ngrid)).pack(padx=10)
        Label(cases[j][i-1-10*j], text= scores[j][i-1-10*j], bg="#fff", font=("courrier",9)).pack()
    Menubutton(self.content, text="RETOUR", command = lambda : Main_menu(self.top, self.player)).pack()

class Score_List:
  def __init__(self, top , player):
    self.top = top
    self.d = sorted(get_players_points(), key=lambda scores: scores[1],reverse=True)
    self.player = player
    self.content = Frame(bg="#fff")
    self.content.pack()
    self.top.update(self.content)
    
    i = 1
    for item in self.d:
      RushLabel(self.content, text=str(i) + ". " + str(item[0]) +" : " +str(item[1]) + " points").pack()
      i+=1
    Menubutton(self.content, text="RETOUR", command = lambda : Main_menu(self.top, self.player)).pack()

class New_Player:
  def __init__(self, prev, action):
    self.top = prev.top
    self.player = prev.player
    self.prev = prev
    self.action = action
    self.players = playernames()
    
    self.content = Frame(bg="#fff")
    self.content.pack(pady=50)
    self.top.update(self.content)
    self.e = Entry(self.content,justify=CENTER,font=("Courier",30), bg="#fff")
    RushLabel(self.content, text="Pseudo :").pack()
    self.e.pack()
    Menubutton(self.content,text="VALIDER", command = lambda : self.validate(self.e.get())).pack()
    Menubutton(self.content,text="ANNULER", command = lambda : Main_menu(self.top, self.player)).pack()

    
  def validate(self, entree):
    if entree in self.players:
      self.top.show_error(" Ce nom est déjà pris ... :( ")
      self.e.delete(0, END)
    else :
      self.player.setname(entree)
      eval(self.action)
      
class Save:
  def __init__(self, prev, action="Main_menu(self.top, self.player)"):
    self.top = prev.top
    self.player = prev.player
    self.action = action
    if self.player.islogged():
      self.saveandleave()
    else:
      self.content =Frame(bg="#fff")
      self.content.pack()
      self.top.update(self.content)
      RushLabel(self.content, text="Avez-vous déjà une partie d'enregistrée?").pack()
      Menubutton(self.content, text="OUI", command= lambda : self.getexisting()).pack()
      Menubutton(self.content, text="NON", command= lambda :  self.getnew()).pack()

      
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

class AskForSave:
  def __init__(self, top, player):
    self.top = top
    self.player = player
    self.content = Frame(bg="#fff")
    self.content.pack()
    self.top.update(self.content)
    RushLabel(self.content,text="Voulez vous sauvegarder votre partie ?").pack()
    Menubutton(self.content,text="OUI", command= lambda : Save(self, action = "self.top.close()")).pack()
    Menubutton(self.content,text="NON", command= lambda : self.top.close()).pack()
  
    
class Win_Menu:
  def __init__(self, top , player, ngrid, trials):
    self.top = top
    self.player = player
    self.ngrid = ngrid
    self.trials = trials   
    self.content = Frame(bg="#fff")
    self.content.pack()
    self.top.update(self.content)

    Label(self.content, text="Winner !", height=3,fg = "#333", bg = "#fff",font =("Courier", 40)).pack()
    RushLabel(self.content, text="Nombre de coups : %i" % self.trials).pack()
    Menubutton(self.content, text = "CHOISIR UNE GRILLE", command = lambda : Grid_Choice(self.top, self.player)).pack()
    Menubutton(self.content, text = "MENU PRINCIPAL", command = lambda : Main_menu(self.top, self.player)).pack()

    if (ngrid != 40):
      Menubutton(self.content, text = "GRILLE SUIVANTE", command = lambda : Start_Level(self.top, self.player, self.ngrid+1)).pack() 
    
class Main_menu:
  def __init__(self, cw, player):
    self.top = cw
    self.player = player
    self.content = Frame(bg="#fff")
    self.content.pack()
    Menubutton (self.content, text= "JOUER", command = lambda : Start_Level(self.top, self.player, 1)).pack()
    Menubutton (self.content, text= "CHOISIR UN NIVEAU", command = lambda : Grid_Choice(self.top, self.player)).pack()
    Menubutton (self.content, text= "CHARGER UNE PARTIE", command = self.loadplayer_callback).pack()
    Menubutton (self.content, text= "SAUVEGARDER", command = lambda : Save(self)).pack()
    Menubutton (self.content, text= "MEILLEURS SCORES", command = lambda : Score_List(self.top,self.player)).pack()
    Menubutton (self.content, text= "QUITTER", command = lambda : self.quit_callback()).pack()
    self.top.update(self.content)
      
  def loadplayer_callback(self):
    Player_Choice(self, "Grid_Choice(self.top, self.player)")
    
  def quit_callback(self):
    AskForSave(self.top, self.player)
    
class content_window :
  def __init__(self, top):
    self.photo=PhotoImage(file="images/rushhour.gif")
    self.header = Label(image = self.photo, bg="#FFF")
    self.body = None
    self.top = top
    self.header.pack()
    self.error = None
  def clear(self):
    if self.body:
      self.body.pack_forget()
      self.body = None
    if self.error:
      self.error.pack_forget()
      self.error = None

  def update(self,content):
    self.clear()
    self.body = content
    
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
    Label.__init__(self, 
                   height=2,
                   fg = "#333",
                   bg = "#fff",
                   font =("Courier", 20),
                   *args, **kwargs)
                   
                  
class Minigridbutton(Button):
  def __init__(self, grid, played, *args, **kwargs):
    playedchar = ""
    if played:
      playedchar="p"
    stri = "images/minigrille-"+str(grid)+str(playedchar)+".gif"
    self.photo=PhotoImage(file=stri)
    Button.__init__(self,  
                    height=58,
                    width = 58,
                    image=self.photo,
                    fg = "#333",
                    activeforeground = "#F55",
                    bg = "#fff",
                    activebackground="#fff",
                    font =("Courier", 20),
                    
                    overrelief = FLAT,
                    highlightthickness=0,
                    borderwidth=0,
                    *args, **kwargs)
    
def main():#---------> OK
  # INIT
  fenetre = Tk()
  fenetre.geometry("800x900")
  fenetre.configure(background="#fff")
  fenetre.title("Rush Hour, by Clara Rigaud and Gwaldys Léré")
  content = content_window(fenetre)
  Main_menu(content, Player())
  fenetre.mainloop()

  
# ==============================================================================
if __name__ == '__main__':
  main()
# ==============================================================================
