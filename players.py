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
    assert isinstance(ngrid, (int)), "<ngrid> must be an int"
    return (self.scores[ngrid-1]!=None)


  def islogged(self):
    """retourne vrai ou faux selon si le joueur est enregistré ou non"""
    return self.name!=None
  

  def saveinfile(self):
    """ enregistre le joueur et ses nouveaux scores dans le fichier"""
    filecontent = json.load(open('players.json'))
    if self.name in filecontent.keys():
      filecontent[self.name] = self.scores
    else:
      filecontent.update({self.name:self.scores})
    with open("players.json", "w") as outfile:
      json.dump(filecontent, outfile, indent=4, sort_keys=True)

      
  def setname(self, name):
    """ change le nom du joueur"""
    assert isinstance(name, (str)), "<name> must be an str"
    self.name = name
    
    
  def set_player_grid_score(self,ngrid, score):
    """ modifie le score du joueur sur le numero de grille donné s'il est meilleur que celui déjà présent""" 
    assert isinstance(ngrid, (int)), "<ngrid> must be an int"
    assert isinstance(score, (int)), "<score> must be an int"
    oldscore = self.get_player_grid_score(ngrid)
    if oldscore:
      if oldscore>score:
        self.scores[ngrid-1]=score
    else:
      self.scores[ngrid-1]=score

                                                       
  def get_player_grid_score(self, ngrid):
    """ renvoie le score du joueur pour une grille donnée"""
    assert isinstance(ngrid, (int)), "<ngrid> must be an int"
    return self.scores[ngrid-1]


  def get_player_points(self):
    """renvoie une liste des points du joueur pour chaque grille (meilleur score sur la grille divisé par son score *100 pour donner de l'importance)"""
    points =[]
    for i in range(1,41):
      bestscore = get_grid_best_score(i)
      playerscore = self.get_player_grid_score(i)
      if bestscore:
        if playerscore:
          points.append(int((bestscore/playerscore)*25))
        else:
          points.append(0)
      else:
        points.append(0)
    return (points,sum(points))

        
  def sync(self, player2):
    """Syncronise les scores de deux joueurs"""
    self.name = player2.name
    for i in range (40):
      if player2.scores[i]:
        self.set_player_grid_score(i+1, player2.scores[i])


def playernames():
  """Récupère les noms des joueurs contenus dans le fichier json"""
  return json.load(open('players.json')).keys()

  
def get_players_points(summed=True):
  """Récupère les points des joueurs"""
  assert isinstance(summed, (bool)), "<summed> must be a bool"
  players = json.load(open('players.json'))
  names = list(players.keys())
  points = []
  for name in names:
    player = Player(name)
    points.append((name,player.get_player_points()[int(summed)]))
  return points


def get_grid_best_score(ngrid):
  """retourne une liste contenant le meilleur score sur un grille"""
  assert isinstance(ngrid, (int)), "<ngrid> must be an int"
  players = json.load(open('players.json'))
  n=None
  name = ""
  for player in players.values():
        if player[ngrid-1] and (not(n) or n>player[ngrid-1]):
          n=player[ngrid-1] 
  return n
