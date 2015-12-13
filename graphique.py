# ==============================================================================
"""RUSH HOUR : get your car out of this mess !"""
# ==============================================================================
__author__  = "Gwladys Léré, Clara Rigaud"
__version__ = "3.0"
__date__    = "2015-12-13"
__usage__   = """"""
# ==============================================================================
from tkinter import *
from grid import *
from car import *
from main_graphic import Win_Menu

# ------------------------------------------------------------------------------

class Graphic:
    
  def __init__(self,grid, top, window, player, ngrid):
    self.ngrid = ngrid
    self.player = player
    self.grid = grid
    self.nb_blocs = 6
    self.largeur_bloc = 80
    self.mainwin = top
    self.fenetre = window
    self.trials = 0
    self.canvas = Canvas(self.fenetre,bg="grey",height = self.nb_blocs * self.largeur_bloc, width = self.nb_blocs * self.largeur_bloc)
   
    y0 = - self.largeur_bloc
    y1 = 0
    i = -1

    #On remplit le canvas avec un dammier, avant les voitures
    for row in range(6):
        i += 1
        x0 = 0
        x1 = self.largeur_bloc
        y0 += self.largeur_bloc
        y1 += self.largeur_bloc
        for column in range (6):
            
            if i%2 == 0:
                color = "dark grey"
            else:
                color = "light grey"

            self.canvas.create_rectangle(x0,y0,x1,y1,fill=color)
            x0 += self.largeur_bloc
            x1 += self.largeur_bloc
            i+=1
        
    
    self.canvas.pack()
    self.car = {}
    for key in grid.cars:
        #On ajoute les voitures dans le canvas en fonction du numéro de grille de jeu
        self.car[key] = self.cars(grid.cars[key])

    #on récupère l'événement clic gauche et on appelle self.clic avec
    self.canvas.focus_set()
    self.canvas.bind("<Button-1>",self.clic)
    
  def colorCars(self,car):
    """ détermne la couleur de chaque voiture"""
    color = {"A" : "purple",
             "B" : "light green",
             "C" : "dark blue",
             "D" : "green",
             "E" : "orange",
             "F" : "blue",
             "G" : "yellow",
             "H" : "cyan",
             "I" : "black",
             "J" : "pink",
             "K" : "white",
             "L" : "turquoise",
             "M" : "brown",
             "Z" : "red"}
    return color[car]
    

  def cars(self,car):
    """affiche les voitures dans le canvas"""
    
    x0 = car.x * self.largeur_bloc
    y0 = car.y*self.largeur_bloc
    x1 = car.width*self.largeur_bloc + x0
    y1 = car.height*self.largeur_bloc + y0
    
    color = self.colorCars(car.name)
    rectangle = self.canvas.create_rectangle(x0,y0,x1,y1,fill=color)
    #le tableau carGraph nous permettra de faire bouger les voitures en gardant les coordonnées du rectangle
    carGraph = [x0,y0,x1,y1,car.name,rectangle]

    #enlever le commentaire si on veut voir quel rectangle correspond à quelle voiture
    #text = self.canvas.create_text(x0+car.width*self.largeur_bloc/2, y0+car.height*self.largeur_bloc/2, text=car.name, font="Arial 16 italic", fill="black")
   
    return carGraph

  def clic(self,event):
    """Fait un mouvement selon l'endroit cliqué par l'utilisateur sur le canvas"""
    X = event.x
    Y = event.y
    
    for key in self.car:
      self.moveCar(key,X,Y)

  def outOfGrid(self,x0,y0,x1,y1):
    """Vérifie si la voiture est en dehors de la grille"""
    
    taille = self.nb_blocs*self.largeur_bloc
    
    if x0 < 0 or x1 > taille or y0 < 0 or y1 > taille:
      return True
    else:
      return False
    
  def crashes(self,x0,y0,x1,y1,key):
    """Vérifie s'il y a un crash entre 2 voitures"""
    if x1 <= self.car[key][0] or \
       x0 >= self.car[key][2] or \
       y0 >= self.car[key][3] or \
       y1 <= self.car[key][1] :
      return False
    else:
      return True
      
  def isRoadFree(self,x0,y0,x1,y1,carName):
    """Vérifie la voiture bougée en chevauche une autre"""

    for key in self.car:
      if carName == self.car[key][4]:
        continue
      if self.crashes(x0,y0,x1,y1,key):
        return False
    return True
        
  def moveCar(self, key, X, Y):
    """Effectue le mouvement de la voiture"""

    #La deuxième variable permet de garder en mémoire les coordonnées de départ afin d'annuler si le mouvement n'est pas valable
    x0 = x00 = self.car[key][0]
    y0 = y00 = self.car[key][1]
    x1 = x01 = self.car[key][2]
    y1 = y01 = self.car[key][3]
    carName = self.car[key][4]
    rectangle = self.car[key][5]

    #Trouve la voiture sur laquelle est le clic
    if x0 <= X <= x1 and y0 <= Y <= y1:
      #Met à jour les coordonnées du rectangle selon le mouvement voulu
      
      if self.grid.cars[carName].vertical == True: #voiture verticale
        if y0 <= Y <= y0 + self.largeur_bloc: #Up
          y0 -= self.largeur_bloc
          y1 -= self.largeur_bloc
         
        elif y1 - self.largeur_bloc <= Y <= y1: #Down
          y0 += self.largeur_bloc
          y1 += self.largeur_bloc
    
      else:
        if x0 <= X <= x0 + self.largeur_bloc: #Left
          x0 -= self.largeur_bloc
          x1 -= self.largeur_bloc
       
        elif x1 - self.largeur_bloc <= X <= x1: #Right
          x0 += self.largeur_bloc
          x1 += self.largeur_bloc
       
      #Le tableau des coordonnées du rectangle est mis à jour    
      self.car[key] = [x0,y0,x1,y1,carName,rectangle]
      
      if self.outOfGrid(x0,y0,x1,y1) == False and self.isRoadFree(x0,y0,x1,y1,carName):
        #Si le mouvement est bon, le rectangle est bougé selon ses nouvelles coordonnées
        self.canvas.coords(rectangle, x0, y0, x1, y1)
        self.trials += 1
      else:
        #Sinon le tableau de coordonnées est remis à zéro en reprenant ses anciennes valeurs
        self.car[key] = [x00,y00,x01,y01,carName,rectangle]

      #Si c'est la voiture Z, on regarde si on a gagné
      if self.car[key][4] == "Z":
        self.win(x1)
        
  def win(self,x1):
    """Vérifie si le joueur a gagné"""
    if x1 == self.nb_blocs*self.largeur_bloc + self.largeur_bloc:
      Win_Menu(self.mainwin, self.player, self.ngrid, self.trials)


##if __name__ == "__main__":
##
##  ngrid = 15
##  grid = Grille(ngrid)
##  graphe = Graphic(grid)

