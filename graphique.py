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
    
  def __init__(self,grid,window, player, ngrid):
      self.ngrid = ngrid
      self.player = player
      self.grid = grid
      self.nb_blocs = 6
      self.largeur_bloc = 50
      self.fenetre = window.top
      self.window = window
      self.trials = 0
      #self.textCar = {}
      self.canvas = Canvas(self.fenetre,bg="grey",height = self.nb_blocs * self.largeur_bloc,width = self.nb_blocs * self.largeur_bloc)
     
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
      #self.bitmaps = {}
      for key in grid.cars:
          #(self.car[key],self.bitmaps[key]) = self.cars(grid.cars[key])
          self.car[key] = self.cars(grid.cars[key])
      print(self.car["A"])

      self.canvas.focus_set()
      self.canvas.bind("<Button-1>",self.clic)
    
  def colorCars(self,car):
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
      """affiche les voitures"""
      x0 = car.x * self.largeur_bloc
      y0 = car.y*self.largeur_bloc
      x1 = car.width*self.largeur_bloc + x0
      y1 = car.height*self.largeur_bloc + y0
      
      color = self.colorCars(car.name)
      rectangle = self.canvas.create_rectangle(x0,y0,x1,y1,fill=color)
      carGraph = [x0,y0,x1,y1,car.name,rectangle]

      #logo de voiture à mettre sur les blocs
      #logo = PhotoImage(file="voiture.gif")
      #self.canvas.create_image(x1,y0,image=logo)

      #logo = BitmapImage(file = "D:\programmation ED\graphique\up.xbm", foreground='red')
      #bitmaps = self.bitmap(x0,y0,x1,y1)
      
      text = self.canvas.create_text(x0+car.width*self.largeur_bloc/2, y0+car.height*self.largeur_bloc/2, text=car.name, font="Arial 16 italic", fill="black")
      #self.textCar[key] = [x0+key.width*self.largeur_bloc/2, y0+key.height*self.largeur_bloc/2, text]
      #return (car,bitmaps)
      return carGraph

##  def bitmap(self,x0,y0,x1,y1):
##    x0 += self.largeur_bloc/2
##    y0 += self.largeur_bloc/2
##    x1 -= self.largeur_bloc/2
##    y1 -= self.largeur_bloc/2
##    bitmap1 = self.canvas.create_bitmap(x0, y0, activebitmap = "question")
##    posBitmap1 = [x0,y0,bitmap1]
##    bitmap2 = self.canvas.create_bitmap(x1, y1, bitmap = "question")
##    posBitmap2 = [x1,y1,bitmap2]
##
##    bitmaps = [posBitmap1, posBitmap2]
##    return (bitmaps)

  def clic(self,event):
    X = event.x
    Y = event.y
    print(("x = %i et y =%i") % (X,Y))
    for key in self.car:
      self.moveCar(key,X,Y)

  def outOfGrid(self,x0,y0,x1,y1):
    taille = self.nb_blocs*self.largeur_bloc
    
    if x0 < 0 or x1 > taille or y0 < 0 or y1 > taille:
      return True
    else:
      return False
    
  def crashes(self,x0,y0,x1,y1,key):
      #print("x0%s, y0%s, x1%s, y1%s,keyname%s, xokey%s, y0key%s, x1key%s, y1key%s"%(x0,y0,x1,y1,self.car[key][4],self.car[key][0],self.car[key][1],self.car[key][2],self.car[key][3]))
      if x1 <= self.car[key][0] or \
         x0 >= self.car[key][2] or \
         y0 >= self.car[key][3] or \
         y1 <= self.car[key][1] :
        return False
      else:
        return True
      
  def isRoadFree(self,x0,y0,x1,y1,carName):

    for key in self.car:
      if carName == self.car[key][4]:
        continue
      if self.crashes(x0,y0,x1,y1,key):
        return False
    return True
        
  def moveCar(self, key, X, Y):
    x0 = x00 = self.car[key][0]
    y0 = y00 = self.car[key][1]
    x1 = x01 = self.car[key][2]
    y1 = y01 = self.car[key][3]
    carName = self.car[key][4]
    rectangle = self.car[key][5]
    
    if x0 <= X <= x1 and y0 <= Y <= y1:
      if self.grid.cars[carName].vertical == True: #voiture verticale
        print("vertical")
        if y0 <= Y <= y0 + self.largeur_bloc: #Up
          print("tab vertical: ",self.car[key])
          y0 -= self.largeur_bloc
          y1 -= self.largeur_bloc
          #move = "up"
          print("tab vertical: ",self.car[key])
        elif y1 - self.largeur_bloc <= Y <= y1: #Down
          y0 += self.largeur_bloc
          y1 += self.largeur_bloc
          #move = "down"
      else:
        if x0 <= X <= x0 + self.largeur_bloc: #Left
          x0 -= self.largeur_bloc
          x1 -= self.largeur_bloc
          #move = "left"
        elif x1 - self.largeur_bloc <= X <= x1: #Right
          x0 += self.largeur_bloc
          x1 += self.largeur_bloc
          #move = "right"
          
      self.car[key] = [x0,y0,x1,y1,carName,rectangle]
      
      if self.outOfGrid(x0,y0,x1,y1) == False:
        if self.isRoadFree(x0,y0,x1,y1,carName):
          self.canvas.coords(rectangle, x0, y0, x1, y1)
          self.trials += 1
        else:
          self.car[key] = [x00,y00,x01,y01,carName,rectangle]
      else:
        self.car[key] = [x00,y00,x01,y01,carName,rectangle]

      if self.car[key][4] == "Z":
        self.win(x1)
        
      #self.textCarMove(key,move)
      #self.bitmaps[key] = self.bitmapPostionChange(move,key)
          
      print("voiture %s"%self.car[key][4])
  def win(self,x1):
    if x1 == self.nb_blocs*self.largeur_bloc + self.largeur_bloc:
      self.win == True
      Win_Menu(self.window, self.player, self.ngrid, self.trials)
      #self.canvas.create_window(0,36,text = "vous avez gagné!")

##  def textCarMove(self,key,move):
##    x0 = self.textCar[key][0]
##    y0 = self.textCar[key][1]
##    text = self.textCar[key][2]
##    if move == "right":
##      x0 += self.largeur_bloc
##    elif move == "left":
##      x0 -= self.largeur_bloc
##    elif move == "up":
##      y0 += self.largeur_bloc
##    elif move == "down":
##      y0 -= self.largeur_bloc
##    self.canvas.coords(text,x0,y0)
##    self.textCar[key] = [x0,y0,text]
    

# pour bouger le bitmap, à reprendre si temps sinon on vire le bitmap, pas très grave
##  def bitmapPostionChange(self,move,key):
##    x0 = self.bitmaps[key][0][0]
##    y0 = self.bitmaps[key][0][1]
##    x1 = self.bitmaps[key][1][0]
##    y1 = self.bitmaps[key][1][1]
##    bitmap1 = self.bitmaps[key][0][2]
##    bitmap2 = self.bitmaps[key][1][2]
##    
##    if move == "right":
##      x0 += self.largeur_bloc
##      x1 += self.largeur_bloc
##    elif move == "left":
##      x0 -= self.largeur_bloc
##      x1 -= self.largeur_bloc
##    elif move == "up":
##      y0 += self.largeur_bloc
##      y1 += self.largeur_bloc
##    elif move == "down":
##      y0 -= self.largeur_bloc
##      y1 -= self.largeur_bloc
##
##    self.canvas.coords(bitmap1,x0,y0)
##    self.canvas.coords(bitmap2,x1,y1)
##    
##    self.bitmaps[key][0] = [x0, y0, bitmap1]
##    print(self.bitmaps[key][0], "bitmap1")
##    self.bitmaps[key][1] = [x1, y1, bitmap2]
##    print(self.bitmaps[key][1], "bitmap2")
      

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

