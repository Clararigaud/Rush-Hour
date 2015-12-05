# ==============================================================================
"""RUSH HOUR : get your car out of this mess !"""
# ==============================================================================
__author__  = "Gwladys Léré, Clara Rigaud"
__version__ = "3.0"
__date__    = "2015-12-13"
__usage__   = """"""
# ==============================================================================
import json
# ------------------------------------------------------------------------------
class Player:
  def __init__(self, name=None):  #init pour nouveau joueur
    self.name = name
    if self.name:
      scores = json.load(open('players.json'))
      self.scores = scores[name]
    else :
      self.scores = [-1 for i in range (40)]

  def hasplayed(self, ngrid):
    """retourne vrai ou faux selon si le jouer à un score associé au numéro de grille"""
    return (self.scores[ngrid-1]!=-1)
  
  def saveinfile(self):
    """ sauvegarde la partie"""
    filecontent = json.load(open('players.json'))
    if self.name in filecontent.keys():
      filecontent[self.name] = self.scores
    else:
      filecontent.update({self.name:self.scores})
    with open("players.json", "w") as outfile:
      json.dump(filecontent, outfile, indent=4, sort_keys=True)
      
  def setname(self, name):
    """ change le nom du joueur"""
    self.name = name
    
  def setgridscore(self,ngrid, score):
    """ enregistre le score du joueur sur le numero de grille donné s'il est meilleur que celui déjà présent""" 
    if not(self.hasplayed(ngrid))^(self.getgridscore(ngrid)>score):
      self.scores[ngrid-1]=score
      print("score updated")

  def getgridscore(self, ngrid):
    """ renvoie le score du joueur pour une grille donnée"""
    return self.scores[ngrid-1]

  def playernames(self):
    return json.load(open('players.json')).keys()
  

  
