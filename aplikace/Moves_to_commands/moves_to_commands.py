import numpy as np

class Cords:
  def __init__(self, x, y):
   self.x = x
   self.y = y

class MoveToCmds:
  def __init__(self, chess_status, cords):
    self.start_cords = Cords(cords[0][0], cords[0][1])
    self.final_cords = Cords(cords[1][0], cords[1][1]) 
    self.chess_status = chess_status
  
  def fill_board_status(self):
    for i in np.arange(0,7.5,0.5):
     for j in np.arange(0,7.5,0.5):
        self.chess_status[(i,j)] = 0
    return self.chess_status

  def make_path_lines(self):
    xs, ys = self.start_cords.x, self.start_cords.y
    xf, yf = self.final_cords.x, self.final_cords.y
    path = []
    sign = ''
    path.append((xs,ys))
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
      path.append((xs,ys))
    '''
    Pohyb po horizontálních krajích
    '''
    while xs != xf:
      if xs < xf:
        xs += 0.5
      else:
        xs -= 0.5
      path.append((xs,ys))
    '''
    Na základně předchozího znaménka rozhodne zda je cíl nahoře nebo dole
    '''
    if sign == '+':
      path.append((xs,ys+0.5))
    else:
      path.append((xs,ys-0.5))
    return True, path

  def make_path_squares(self):
    xs, ys = self.start_cords.x, self.start_cords.y
    xf, yf = self.final_cords.x, self.final_cords.y
    path = []
    path.append((xs,ys))
    '''
    Pohyb po čtverečkách pokud nemá nic ve svém řádku/sloupci
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
      if self.chess_status[(xs,ys)] == 0:
        path.append((xs,ys))
      else:
        return False, None
    return True, path

  def decide(self):
    valid, path = self.make_path_squares()
    if valid:
      return path
    else:
      valid, path = self.make_path_lines()
      if valid:
        return path
      else:
        print("ERROR creating path")
        exit()

  def move(self):
    return self.decide()


if __name__ == "__main__":
  chess_status = dict()
  cords = [(0,1),(4,4)]
  move = MoveToCmds(chess_status, cords)
  move.fill_board_status()
  print(move.move())
