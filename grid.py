# ==============================================================================
"""RUSH HOUR : get your car out of this mess !"""
# ==============================================================================
__author__  = "Gwladys Léré, Clara Rigaud"
__version__ = "2.0"
__date__    = "2015-1-26"
__usage__   = """"""
# ==============================================================================
from ezCLI import *
from car import *
# ------------------------------------------------------------------------------
class Grid:

  def __init__(self, dic):
    self.cars = {}
    for key in dic:
      self.cars[key] = Car(dic[key], key)

  def toArray(self):
    """ renvoie un tableau pour afficher avec grid (ezCLI) """
    
    gameArray = [["" for j in range(6)] for i in range(6)]
    
    for key in self.cars:
      car = self.cars[key]
      if car.vertical:
        for i in range (car.y, car.y + car.height):
          gameArray[i][car.x] = car.name
      else:
        for i in range (car.x, car.x + car.width):
          gameArray[car.y][i] = car.name
          
    return gameArray

  def move(self, car, direction):
    if car.canMove(direction) == False:
      return "wrongdir"
    car.movement(direction)  #effectue le déplacement de la voiture
    if self.win():
      return "win"
    if self.carIsOutOfGrid(car):
      car.movement(direction, True) #effectue le déplacement inverse de la voiture pour la remettre à sa place puisque déplacement impossible
      return "outofstreet"
    if self.isRoadFree(car) == False:
      car.movement(direction, True)
      return "occupied"
    
  def carIsOutOfGrid(self, car):
    if car.x < 0 or car.x + car.width > 6 or car.y < 0 or car.y + car.height > 6:
      return True  #retourne vrai si la voiture est en dehors de la grille
    else:
      return False

  def isRoadFree(self, car):
    for key in self.cars:
      if key == car.name:
        continue
      if car.crashes(self.cars[key]):
        return False       #retourne faux si on a une collision, donc route pas libre
    return True
  
  def win(self):
    car = self.cars["Z"]
    if car.x + car.width == 7:
      return True
    else :
      return False
        
  
# ==============================================================================
