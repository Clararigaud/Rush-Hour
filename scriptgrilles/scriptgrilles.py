import json
import urllib.request
import io

def getgrille(f):
  carletters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q"]
  i= 0
  grille = {}
  for line in f:
    
    if(line[0:8] == "vehicle["):
      y= line[line.find("fTop+")+5]
      x= line[line.find("fLeft+")+6]
      if (line[line.find(".gif")-2]=='E'):
        direction = "h"
      elif(line[line.find(".gif")-2]=='N'):
        direction = "v"
      else :
        print("erreur direction")
      if (line[line.find("car(\"")+6]=='e'):
        size = 2
        name = "Z"
      elif (line[line.find("car(\"")+6]=='c'):
        size = 2
        name = carletters[i]
        i = i+1
      elif (line[line.find("car(\"")+6]=='l'):
        size = 3
        name = carletters[i]
        i=i+1
      else:
        print("erreur size / name ")
      voiture = dict([(name, dict([('size', size), ('x', int(x)), ('y', int(y)), ('direction',direction)]))])
      grille.update(voiture)
  return grille

def dl(url):
  f= urllib.request.urlopen(url)
  return io.TextIOWrapper(f, encoding='utf-8')

grilles = {}
for i in range (1,41):
  url = "http://www.puzzles.com/products/RushHour/RHfromMarkRiedel/jam%s.js" %(i) 
  f = dl(url)
  grilles.update({str(i):getgrille(f)})

with open("tgri.json", "w") as outfile:
    json.dump(grilles, outfile, indent=4, sort_keys=True)

print("Done ma capt'n")


