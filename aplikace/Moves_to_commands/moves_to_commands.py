import numpy as np
import matplotlib.pyplot as plt


class Cords:
  def __init__(self, x, y):
   self.x = x
   self.y = y

class MoveToCmds:
  def __init__(self):
    self.start_cords = Cords(0, 0)
    self.final_cords = Cords(0, 0) 
    self.chess_status = dict()
    self.shiftL = 0.5
  
  def update_cords(self, cords):
    self.start_cords = Cords(cords[0][0], cords[0][1])
    self.final_cords = Cords(cords[1][0], cords[1][1])
  
  def fill_board_status(self):
    for i in np.arange(0,7.5,self.shiftL):
     for j in np.arange(0,7.5,self.shiftL):
        self.chess_status[(i,j)] = 0
    return self.chess_status

  def update_board(self, board):
    self.fill_board_status()
    for i,j in board:
      self.chess_status[(i,j)] = 1
    return self.chess_status

  def make_path_lines(self, path, crds):
    xs, ys = crds
    xf, yf = self.final_cords.x, self.final_cords.y
    sign = ''
    '''
    Rozhodne jakým směrem půjde na základě vzdálenosti 
    finálních souřadnic a startovních souřadnic
    '''
    if xs >= xf:
      if xs - self.shiftL >= 0:
        xs -= self.shiftL
        if ys + self.shiftL <= 7:
          ys += self.shiftL
          sign = '+'
        elif ys - self.shiftL >= 0:
          ys -= self.shiftL
          sign = '-'
    elif xs <= xf:
      if xs + self.shiftL <= 7:
        xs += self.shiftL
        if ys + self.shiftL <= 7:
          ys += self.shiftL
          sign = '+'
        elif ys - self.shiftL >= 0:
          ys -= self.shiftL
          sign = '-'
    path.append((xs,ys))
    '''
    Pohyb po svislých krajích šachovnice
    '''
    while ys != yf - self.shiftL and ys != yf + self.shiftL:
      if ys < yf:
        ys += self.shiftL
      else:
        ys -= self.shiftL
      path.append((xs,ys))
    '''
    Pohyb po horizontálních krajích
    '''
    while xs != xf:
      if xs < xf:
        xs += self.shiftL
      else:
        xs -= self.shiftL
      path.append((xs,ys))
    '''
    Na základně předchozího znaménka rozhodne zda je cíl nahoře nebo dole
    '''
    if sign == '+':
      path.append((xs,ys+self.shiftL))
    else:
      path.append((xs,ys-self.shiftL))
    return True, path

  def make_path_squares(self):
    xs, ys = self.start_cords.x, self.start_cords.y
    xf, yf = self.final_cords.x, self.final_cords.y
    xbf = 0
    ybf = 0
    path = []
    path.append((xs,ys))
    '''
    Pohyb po čtverečkách pokud nemá nic ve svém řádku/sloupci
    '''
    while xs != xf or ys != yf:
      xbf = xs
      if xs < xf and xs + self.shiftL <= 7:
        xs += self.shiftL
      elif xs > xf and xs - self.shiftL >= 0:
        xs -= self.shiftL
      ybf = ys
      if ys < yf and ys + self.shiftL <= 7:
        ys += self.shiftL
      elif ys > yf and ys - self.shiftL >= 0:
        ys -= self.shiftL
      if self.chess_status[(xs,ys)] == 0:
        path.append((xs,ys))
      elif xs == xf and ys == yf:
        path.append((xs,ys))
      else:
        return False, path, (xbf,ybf)
    return True, path, (xs,ys)

  def decide(self):
    valid, path, crds = self.make_path_squares()
    if valid:
      print(path)
      return path
    else:
      valid, path,  = self.make_path_lines(path, crds)
      if valid:
        print(path)
        return path
      else:
        print("ERROR creating path")
        exit()

  def move(self, board, cords):
    self.update_cords(cords)
    self.update_board(board)
    return self.decide()

  def print_board(self, path):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_axes([0.05, 0.05, 1, 1])
    ax.set_xlim(-1, 8)
    ax.set_ylim(-1, 8)
    for j in np.arange(0,7.5,0.5):
      for i in np.arange(0,7.5,0.5):
        if (i,j) in path:
          c = 'blue'
          s = 100
        elif i%1 == 0 and j%1 == 0 and self.chess_status[(i,j)] != 0:
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


if __name__ == "__main__":
  move = MoveToCmds()
  i = 0
  while i < 1:
    if i == 0:
      board = [(1,1),(2,2),(6,5)]
      cords = [(6,0),(3.5,3.5)]
    move.print_board(move.move(board,cords))
    i += 1
  
