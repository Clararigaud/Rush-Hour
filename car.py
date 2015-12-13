# ==============================================================================
"""RUSH HOUR : get your car out of this mess !"""
# ==============================================================================
__author__  = "Gwladys Léré, Clara Rigaud"
__version__ = "3.0"
__date__    = "2015-12-13"
__usage__   = """"""
# ==============================================================================
from ezCLI import *
# ------------------------------------------------------------------------------
class Car:
  
  def __init__(self, dic, name):
    self.name = name
    self.x = dic["x"]
    self.y = dic["y"]
    
    if dic["direction"] == "v" :
      self.vertical = True
      self.height = int(dic["size"])
      self.width = 1
    else:
      self.vertical = False
      self.width = int(dic["size"])
      self.height = 1

  def canMove(self, direction):
    """ Vérifie si la direction entrée par l'utilisateur correspond au sens de déplacement de la voiture"""
    assert isinstance(direction, (str)), "<direction> must be an str"
    
    if direction not in ["U","D","L","R"]:
      return False
    if self.vertical:
      return (direction == "U" or direction == "D")
    else :
      return (direction == "L" or direction == "R")

  def crashes(self, car):
    """Vérifie si deux voitures se touchent"""
    assert isinstance(car, type(car)), "<car> must be of type car"
    
    #compare les différents cas où on est sûr que les voitures ne se toucheront pas
    if car.x + car.width <= self.x or \
       car.x >= self.x + self.width or \
       car.y + car.height <= self.y or \
       car.y >= self.y + self.height :
         return False    # retourne faux s'il n'y a pas de crash donc si les voitures ne se touchent pas
    else:
      return True #retourne vrai s'il y a un crash

  def movement(self, direction, back = False):  #back à une valeur par défaut de false, si on le passe pas en param ce sera false
    """effectue le mouvement de la voiture ou inverse le mouvement si back = true, pour rétablir la grille si le mouvement demandé est impossible """
    assert isinstance(direction, (str)), "<direction> must be an str"
    assert isinstance(back, (bool)), "<back> must be a bool"
    
    movement = {"U" : [0,-1],
                "D" : [0, 1],
                "L" : [-1,0],
                "R" : [1,0] }
    if back: #si on précise que back vaut true, on inverse le mouvement
      self.x -= movement[direction][0]
      self.y -= movement[direction][1]
    else:
      self.x += movement[direction][0]
      self.y += movement[direction][1]

# ------------------------------------------------------------------------------

# ==============================================================================

# ==============================================================================
