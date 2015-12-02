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
import json
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
    print("Il n'y a pas de voiture à ce nom")


def parser(grid):
  """ gère les fonctions appelées pour le déplacement d'une voiture"""
  assert isinstance(grid, type(grid)), "<grid> must be of type grid"

  command = ""
  while len(command) != 2: #redemande tant que l'utilisateur ne rentre pas 2 lettres
    command = input("Entrez le mouvement (nom de la voiture et nom de la direction en anglais (ex: ZU, ZD, ZL, ZR)) : ")

  carName = command[0].upper()
  direc = command[1].upper()
  if carName in grid.cars:
    car = grid.cars[carName]  #Vérifie si le nom entré par l'utilisateur correspond bien à une voiture
  else:
    car = None #si l'utilisateur n'a pas écrit le nom d'une voiture sur la grille, vaut None
  result = grid.move(car, direc) #renvoie une str avec le nom de l'erreur s'il y en a
  error_msg(result)
  
  return result == "win"
  #retourne vrai si result vaut "win"

def gridChoice(choice,num,mapNum):
  """ renvoie le numérode la grille à jouer selon si l'utilisateur joue dans l'ordre ou non"""
  assert isinstance(choice, (str)), "<choice> must be an str "
  assert isinstance(num, (int)), "<num> must ba an int "
  assert isinstance(mapNum, (list)), "<mapNum> must be a list"
  
  if choice == "ordre":
    num2 = mapNum[num] #l'indice num du tableau mapNum correspond à la valeur de la grille à jouer
    print("Vous jouez sur la grille %s" % num2)
  else:
    num2 = int(input("Quelle grille souhaitez-vous utiliser? (de 1 à 40) :"))
    while str(num2) not in mapNum:
      print("Il y a 40 grilles donc rentrez un numéro compris entre 1 et 40")
      num2 = int(input("Quelle grille souhaitez-vous utiliser? (de 1 à 40) :"))
  return num2

def main():
  
  gdicts = json.load(open('grilles.json'))

  mapNum = ["%s" %i for i in range(1,41)]

  choice = input("voulez-vous faire les niveaux dans l'ordre ou choisir le niveau? (ordre/choix) :")
  while choice not in ["ordre","choix"]:
    choice = input("Je n'ai pas compris. Vous devez rentrer 'ordre' (dans l'ordre) ou 'choix' :")
  num = 0
  
  
  toContinue = "oui"
  
  while toContinue == "oui":

    num = gridChoice(choice, num, mapNum)
    
    gdict = gdicts[str(num)]
    gameGrid = Grid(gdict)

    trials = 0              #trials iterator
    while(True):
      print(grid(gameGrid.toArray(), size=3))

      #a = input("Passer la grille? (o)")     #pour tester sans avoir à jouer la grille
      #if a == "o":
      
      if parser(gameGrid):      #parser renvoie faux tant que la voiture Z n'es pas sortie
        break               #du coup si il renvoie vrai, c'est qu'on a gagné, donc on sort de la boucle
      trials +=1            #à chaque tour de boucle, un essai supplémentaire
          
    print("WINNER !! \nNombre de coups :", trials)
    toContinue = input("Voulez-vous passer à la grille suivante? (oui/non) :")
    while toContinue not in ["oui","non"]:
      toContinue = input("Je n'ai pas compris. Vous devez rentrer 'oui' ou 'non'. Voulez-vous jouer encore une fois? :")
      
  print("Au revoir!!")
    
#ToDo :
   
    # faire l'enregistrement de la partie en cours et du coup le chargement d'une partie antérieure

# ==============================================================================
if __name__ == '__main__':
  main()
# ==============================================================================
