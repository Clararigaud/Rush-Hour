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

# ------------------------------------------------------------------------------

class Graphic:
    
  def __init__(self,grid,window):
      self.grid = grid
      nb_blocs = 6
      self.largeur_bloc = 50
      largeur_bordure = 100
      self.fenetre = window
      self.canvas = Canvas(self.fenetre,bg="grey",height = nb_blocs * self.largeur_bloc,width = nb_blocs * self.largeur_bloc + largeur_bordure)
     
      y0 = - self.largeur_bloc
      y1 = 0
      i = -1

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
          self.car[key] = self.cars(grid.cars[key])
          
          

      self.canvas.focus_set()
      self.canvas.bind("<Button-1>",self.clic)
    
  def printGrid():
      """affiche la grille de jeu"""
      pass
      
  def colorCars(self,key):
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
      return color[key]
    

  def cars(self,key):
      """affiche les voitures"""
      x0 = key.x * self.largeur_bloc
      y0 = key.y*self.largeur_bloc
      x1 = key.width*self.largeur_bloc + x0
      y1 = key.height*self.largeur_bloc + y0
      
      color = self.colorCars(key.name)
      rectangle = self.canvas.create_rectangle(x0,y0,x1,y1,fill=color)
      car = [x0,y0,x1,y1,key.name,rectangle]

      #logo = PhotoImage(file='up.gif') # ne pas supprimer cette référence
      #Label(image=logo).grid()""

      #logo = BitmapImage(file = "D:\programmation ED\graphique\up.xbm", foreground='red')

      

      #faire fonction pour les bitmap pour les avoir quelque part pour quand on bouge les rectangles, ça doit bouger aussi
      bitmap = self.canvas.create_bitmap(x0+self.largeur_bloc/2, y0+self.largeur_bloc/2, activebitmap = "question")
      bitmap2 = self.canvas.create_bitmap(x1-self.largeur_bloc/2, y1-self.largeur_bloc/2, bitmap = "question")
      
      self.canvas.create_text(x0+key.width*self.largeur_bloc/2, y0+key.height*self.largeur_bloc/2, text=key.name, font="Arial 16 italic", fill="black")
      return car

  def mooveCar(self,car):
    pass

  def clic(self,event):
    X = event.x
    Y = event.y
    print(("x = %i et y =%i") % (X,Y))
    
    for key in self.car:
      
      x0 = self.car[key][0]
      y0 = self.car[key][1]
      x1 = self.car[key][2]
      y1 = self.car[key][3]
      carName = self.car[key][4]
      rectangle = self.car[key][5]
      
      if x0 <= X <= x1 and y0 <= Y <= y1:
        if self.grid.cars[carName].vertical == True: #voiture verticale
          print("vertical")
          if y0 <= Y <= y0 + self.largeur_bloc:
            print("tab vertical: ",self.car[key])
            y0 -= self.largeur_bloc
            y1 -= self.largeur_bloc
            self.canvas.coords(rectangle, x0, y0, x1, y1)
            print("tab vertical: ",self.car[key])
          elif y1 - self.largeur_bloc <= Y <= y1:
            y0 += self.largeur_bloc
            y1 += self.largeur_bloc
            self.canvas.coords(rectangle, x0, y0, x1, y1)
        else:
          if x0 <= X <= x0 + self.largeur_bloc:
            x0 -= self.largeur_bloc
            x1 -= self.largeur_bloc
            self.canvas.coords(rectangle, x0, y0, x1, y1)
          elif x1 - self.largeur_bloc <= X <= x1:
            x0 += self.largeur_bloc
            x1 += self.largeur_bloc
            self.canvas.coords(rectangle, x0, y0, x1, y1)

        self.car[key] = [x0,y0,x1,y1,carName,rectangle]
            
        print("voiture %s"%self.car[key][4])

##    #pour z
##    x0 = 100
##    y0 = 100
##    x1 = 200
##    y1 = 150
##    if x0 <= X <= x0+50 and y0 <= Y <= y1:
##      self.canvas.coords(self.car, x0-50, y0, x1-50, y1)
##    elif x0+50 <= X <= x1 and y0 <= Y <= y1:
##      self.canvas.coords(self.car, x0+50, y0,x1+50, y1)

    


##  def clavier(event):
##    touche = event.keysym
##    print(touche)
##
##canvas = Canvas(fenetre, width=500, height=500)
##canvas.focus_set()
##canvas.bind("<Key>", clavier)
##canvas.pack()
##
##<Button-1>
  
    
    

      


if __name__ == "__main__":

  ngrid = 15
  grid = Grille(ngrid)
  graphe = Graphic(grid)

