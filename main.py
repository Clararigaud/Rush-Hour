# ==============================================================================
"""RUSH HOUR : get your car out of this mess !"""
# ==============================================================================
__author__  = "Gwladys Léré, Clara Rigaud"
__version__ = "2.0"
__date__    = "2015-1-26"
__usage__   = """"""
# ==============================================================================
from ezCLI import *
from grid import *
import json
# ------------------------------------------------------------------------------
def error_msg(code):
#methode d'affichage des messages d'erreur
  if code == "outofstreet":
    print("Il faut rester sur la route !")
  elif code == "occupied":
    print("Deja une voiture ici !")
  elif code == "wrongdir":
    print("Cette voiture ne peut pas rouler lateralement")

def parser(grid):
  command = input("Enter move : ")
  carName = command[0]
  direc = command[1]
  car = grid.cars[carName]
  result = grid.move(car, direc)
  error_msg(result)
  
  return result == "win"
  #retourne vrai si result vaut "win"


def main():
  
  gdicts = json.load(open('grilles.json'))

  #demander quelle grille à l'utilisateur
  
  gdict = gdicts["1"]
  gameGrid = Grid(gdict)
  
  trials = 0              #trials iterator
  while(True):
    print(grid(gameGrid.toArray(), size=3))
    if parser(gameGrid):  #parser renvoie faux tant que la voiture Z n'es pas sortie
      break               #du coup si il renvoie vrai, c'est qu'on a gagné, donc on sort de la boucle
    trials +=1            #à chaque tour de boucle, un essai supplémentaire
        
  print("WINNER !! \nNombre de coups :", trials) 
# ==============================================================================
if __name__ == '__main__':
  main()
# ==============================================================================
