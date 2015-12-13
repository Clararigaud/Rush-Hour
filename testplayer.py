from players import *
pl= Player()

d = get_players_points(summed=True)
d = sorted(d, key=lambda scores: scores[1],reverse=True)
