import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import random
#arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

'''
chess board
      a        b       c       d       e       f       g       h

8 || (7,0) (7,0.5) (7,1) (7,1.5) (7,2) (7,2.5) (7,3) (7,3.5) (7,4) (7,4.5) (7,5) (7,5.5) (7,6) (7,6.5) (7,7) || 8

7 || (6,0) (6,0.5) (6,1) (6,1.5) (6,2) | (6,3) | (6,4) | (6,5) | (6,6) | (6,7) || 7

6 || (5,0) (5,0.5) (5,1) (5,1.5) (5,2) | (5,3) | (5,4) | (5,5) | (5,6) | (5,7) || 6

5 || (4,0) (4,0.5) (4,1) (4,1.5) (4,2) | (4,3) | (4,4) | (4,5) | (4,6) | (4,7) || 5

4 || (3,0) (3,0.5) (3,1) (3,1.5) (3,2) | (3,3) | (3,4) | (3,5) | (3,6) | (3,7) || 4

3 || (2,0) (2,0.5) (2,1) (2,1.5) (2,2) | (2,3) | (2,4) | (2,5) | (2,6) | (2,7) || 3

2 || (1,0) (1,0.5) (1,1) (1,1.5) (1,2) | (1,3) | (1,4) | (1,5) | (1,6) | (1,7) || 2

1 || (0,0) (0,0.5) (0,1) (0,1.5) (0,2) | (0,3) | (0,4) | (0,5) | (0,6) | (0,7) || 1

      a        b       c       d       e       f       g       h
'''

class Cords:
  def __init__(self, x, y):
    self.x = x
    self.y = y
      
def print_board(chess_status, path):
  fig = plt.figure(figsize=(8, 8))
  ax = fig.add_axes([0.05, 0.05, 1, 1])
  ax.set_xlim(-1, 8)
  ax.set_ylim(-1, 8)
  for j in np.arange(0,7.5,0.5):
    for i in np.arange(0,7.5,0.5):
      if (i,j) in path:
        c = 'blue'
        s = 100
      elif i%1 == 0 and j%1 == 0 and chess_status[(i,j)] != 0:
        c = 'red'
        s = 100
      elif  i%1 == 0 and j%1 == 0:
        c = 'green'
        s = 100
      else:
        c = 'black'
        s = 10
      ax.scatter(i,j, s=s, c=c, marker='o')
  plt.show()

def fill_board_status(chess_status, cords):
  for i in np.arange(0,7.5,0.5):
     for j in np.arange(0,7.5,0.5):
      if i%1 != 0 or j%1 != 0 or (i,j) == cords[0] or (i,j) == cords[1]:
        chess_status[(i,j)] = 0
      else:
        chess_status[(i,j)] = random.randint(0, 0)
  return chess_status

#---------------------------Funkce pod čarou jsou potřeba------------------------------------------------
def make_path_squares(chess_status, start_cords, final_cords):
  '''
  VSTUPY - (chess_status) obsazenost políček - dict((x,y) = status př. chess_status[(1,2)] = 0 ==> na souřadnicích (1,2) nic není
         - (start_cords) počáteční souřadnice
         - (final_cords) finální souřadnice
  
  VÝSTUP - (valid, path) platnost provedení a cesta s posloupností souřadnic od staru do finishe
  
  Funkce vrací pole souřadnic, od startovních po finální, pokud je možné
  aby se figurka mohla pohybovat celou dobu po čtverečkách, v opačném případě
  varcí False, None a provede se funkce druhá make_path_lines
  '''
  xs, ys = start_cords.x, start_cords.y
  xf, yf = final_cords.x, final_cords.y
  path = []
  path.append((xs,ys))
  '''
  Pohyb po čtverečkách pokud nemá nic ve svém řádku/sloupci/diagonále
  '''
  while xs != xf or ys != yf:
    if xs < xf and xs + 1 <= 7:
      xs += 1
    elif xs > xf and xs - 1 >= 0:
      xs -= 1
    if ys < yf and ys + 1 <= 7:
      ys += 1
    elif ys > yf and ys - 1 >= 0:
      ys -= 1
    if chess_status[(xs,ys)] == 0:
      path.append((xs,ys))
      print("CORDS:", xs, ys)
    else:
      return False, None
  return True, path

def make_path_lines(chess_status, start_cords, final_cords):
  '''
  VSTUPY - (chess_status) obsazenost políček
         - (start_cords) počáteční souřadnice
         - (final_cords) finální souřadnice
  
  VÝSTUP - (valid, path) platnost provedení a cesta s posloupností souřadnic od staru do finishe
  
  Funkce vrací pole souřadnic, od startovních po finální, pokud je možné
  aby se figurka mohla pohybovat celou dobu po čtverečkách, v opačném případě
  varcí False, None a provede se funkce druhá make_path_lines
  '''
  xs, ys = start_cords.x, start_cords.y
  xf, yf = final_cords.x, final_cords.y
  path = []
  sign = ''
  path.append((xs,ys))
  print("CORDS:", xs, ys)
  '''
  Rozhodne jakým směrem půjde na základě vzdálenosti 
  finálních souřadnic a startovních souřadnic
  '''
  if xs >= xf:
    if xs - 0.5 >= 0:
      xs -= 0.5
      if ys + 0.5 <= 7:
        ys += 0.5
        sign = '+'
      elif ys - 0.5 >= 0:
        ys -= 0.5
        sign = '-'
  elif xs <= xf:
    if xs + 0.5 <= 7:
      xs += 0.5
      if ys + 0.5 <= 7:
        ys += 0.5
        sign = '+'
      elif ys - 0.5 >= 0:
        ys -= 0.5
        sign = '-'
  path.append((xs,ys))
  '''
  Pohyb po svislých krajích šachovnice
  '''
  while ys != yf - 0.5 and ys != yf + 0.5:
    if ys < yf:
      ys += 0.5
    else:
      ys -= 0.5
    print("CORDS:", xs, ys)
    path.append((xs,ys))
  '''
  Pohyb po horizontálních krajích
  '''
  while xs != xf:
    if xs < xf:
      xs += 0.5
    else:
      xs -= 0.5
    print("CORDS:", xs, ys)
    path.append((xs,ys))
  '''
  Na základně předchozího znaménka rozhodne zda je cíl nahoře nebo dole
  '''
  if sign == '+':
    path.append((xs,ys+0.5))
  else:
    path.append((xs,ys-0.5))
  return True, path

def decide(chess_status, start_cords, final_cords):
  '''
  VÝSTUP - (valid, path) platnost provedení a cesta s posloupností souřadnic od staru do finishe
  
  Rozhodne jakým způsobem stroj hrací plochu projde. Pokud nebudou v cestě žádné figurky
  půjde klasiky po čtverečkách. Pokud bude něco v cestě půjde po krajích čtverečků
  '''
  valid, path = make_path_squares(chess_status, start_cords, final_cords)
  if valid:
    print(path)
    return path
  else:
    valid, path = make_path_lines(chess_status, start_cords, final_cords)
    if valid:
      print(path)
      return path
    else:
      print("ERROR creating path")
      exit()
  
def move(chess_status, cords):
  start_cords = Cords(cords[0][0], cords[0][1])
  final_cords = Cords(cords[1][0], cords[1][1])  
  path = decide(chess_status, start_cords, final_cords)
  return path

#-------------------------------FUNKCE NAD JSOU POTŘEBA-------------------------------------


chess_status = dict()
#------------VSTUP-------------
cords = [(7,7),(0,0)]
#------------------------------
fill_board_status(chess_status, cords)

#------------VÝSTUP-----------
path = move(chess_status, cords)
#-----------------------------

print_board(chess_status, path)
