# ==============================================================================
"""BINO : compute the binomial coefficient C(n,p)"""
# ==============================================================================
__author__  = "Christophe Schlick"
__version__ = "2.0" # use 'for' loop to generate string
__date__    = "2015-09-01"
__usage__   = """
User input: <n>, <p> (where n:int > 0, p:int >=0)
App output: binomial coefficient C(n,p)"""
# ==============================================================================
from ezCLI import *
from car import *
# ------------------------------------------------------------------------------
class Grid:

  def __init__(self, dic):
    self.cars = {}
    for key in dic:
      self.cars[key] = Car(dic[key], key) #rentre les données des différentes voitures sur la grille


  def toArray(self):
    """ renvoie un tableau pour afficher avec grid (ezCLI) """
    
    gameArray = [["" for j in range(6)] for i in range(6)]
    
    for key in self.cars:
      car = self.cars[key]
      if car.vertical == True:
        for i in range (car.y, car.y + car.height):
          gameArray[i][car.x] = car.name
      else:
        for i in range (car.x, car.x + car.width):
          gameArray[car.y][i] = car.name
          
    return gameArray


  def move(self, car, direction):
    """ Vérifie si le mouvement entré par l'utilisateur peut se faire"""
    assert isinstance(direction, (str)), "<direction> must be an str"
    
    if car == None :
      return "nocar"  #car = None si l'utilisateur a rentré le nom d'une voiture n'existant pas sur la grille
    assert type(car) is type(car), "<car> must be of type car"
    
    if car.canMove(direction) == False:
      return "wrongdir"
    car.movement(direction)  #effectue le déplacement de la voiture
    if self.win():
      return "win"
    elif self.carIsOutOfGrid(car):
      car.movement(direction, True) #effectue le déplacement inverse de la voiture pour la remettre à sa place puisque déplacement impossible
      return "outofstreet"
    elif self.isRoadFree(car) == False:
      car.movement(direction, True)
      return "occupied"
    else:
      return "ok"
    
    

  def carIsOutOfGrid(self, car):
    """ Vérifie si le mouvement fait sortir la voiture de la grille"""
    assert isinstance(car, type(car)), "<car> must be of type car"
    
    if car.x < 0 or car.x + car.width > 6 or car.y < 0 or car.y + car.height > 6:
      return True  #retourne vrai si la voiture est en dehors de la grille
    else:
      return False


  def isRoadFree(self, car):
    """Vérifie s'il y a déjà une autre voiture"""
    assert isinstance(car, type(car)), "<car> must be of type car"
    
    for key in self.cars:
      if key == car.name:
        continue
      if car.crashes(self.cars[key]):
        return False       #retourne faux si on a une collision, donc route pas libre
    return True
  

  def win(self):
    """Vérifie si la voiture Z sort du tableau et don si l'utilisateur a gagné"""
    
    car = self.cars["Z"]
    if car.x + car.width == 7:
      return True
    else :
      return False


  def hasCar(self,carName):
    """ Vérifie si la voiture de nom carName existe sur la grille"""
    assert isinstance(carName, (str)), "<carName> must be of an str"
    
    car = self.cars[carName.upper()] #prend le nom de la voiture en majuscule
    if car == None:
      return False
    return True
    
  
# ==============================================================================
