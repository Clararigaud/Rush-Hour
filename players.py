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
      self.scores = [None for i in range (40)]

  def hasplayed(self, ngrid):
    """retourne vrai ou faux selon si le jouer à un score associé au numéro de grille"""
    return (self.scores[ngrid-1]!=None)

  def islogged(self):
    return self.name!=None
  
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
    
  def set_player_grid_score(self,ngrid, score):
    """ enregistre le score du joueur sur le numero de grille donné s'il est meilleur que celui déjà présent""" 
    oldscore = self.get_player_grid_score(ngrid)
    if oldscore:
      if oldscore>score:
        self.scores[ngrid-1]=score
    else:
      self.scores[ngrid-1]=score
                                                       
  def get_player_grid_score(self, ngrid):
    """ renvoie le score du joueur pour une grille donnée"""
    return self.scores[ngrid-1]

  def get_players_points(self):
    players = json.load(open('players.json'))
    n=[999 for i in range (40)]
    for player in players.values():
        for i in range(40):
          if player[i] and n[i]>player[i]:
            n[i]=player[i]
            print("n =" + n)


            n=[999 for i in range (40)]
    for i in range (40):
      for player in players:
        
          n[i] = [min(player[i]) for player in players]

##    names = list(players.keys())
##    values = list(players.values())
##
##    
##
##    
##    playedscores = [sum(list(filter(lambda x:x !=-1, values[i]))) for i in range (len(values))]
##    return dict(zip(names,playedscores))
##
      return n

  def get_grid_best_score(self,ngrid):
    """retourne une liste contenant le meilleur score sur un grille avec ou sans le nom du joueur selon name"""
    players = json.load(open('players.json'))
    n=None
    name = ""
    for player in players.values():
          if player[ngrid-1] and (not(n) or n>player[ngrid-1]):
            n=player[ngrid-1] 
    return n

  def sync(self, player2):
    self.name = player2.name
    for i in range (40):
      if player2.scores[i]:
        self.set_player_grid_score(i+1, player2.scores[i])

  def playernames(self):
    return json.load(open('players.json')).keys()
  

  
