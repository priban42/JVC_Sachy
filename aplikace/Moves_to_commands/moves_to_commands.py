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
    self.shiftS = 1
  
  def update_cords(self, cords):
    '''
    cords - array of two cords [(xs,ys),(xf,yf)]
    Function updates start and final cords if it's called.
    '''
    self.start_cords = Cords(cords[0][0], cords[0][1])
    self.final_cords = Cords(cords[1][0], cords[1][1])
  
  def fill_board_status(self):
    '''
    Function fill chess status with cords as a key and assigns it state - 0 - there is nothing on this position.
    It returns dictionary with cords as a key and value 0.
                                                                      
    '''
    for i in np.arange(0,7.5,self.shiftL):
     for j in np.arange(0,7.5,self.shiftL):
        self.chess_status[(i,j)] = 0
    return self.chess_status

  def update_board(self, board):
    '''
    board - array of cords [(x,y),(x,y),...]
    Function clears board status and adds 1 on positions, where figures are, by given array of positions (board) of figures.
    It returns dictionary with cords as a key and values 0 or 1.
    '''
    self.fill_board_status()
    for i,j in board:
      self.chess_status[(i,j)] = 1
    return self.chess_status

  def make_path_lines(self, path, crds):
    '''
    path - array of cords [(x,y),(x,y),...]
    crds - cords (x,y)
    At the start its decide, wich line is closer to final position, than the sign is set.
    Function goes by lines on board till it reaches same row, where final postion is.
    Then it goes in columns until it reaches same column. In the end it goes up or down
    base on decision, that was made at the beginning.
    It returns array of cords (x,y).
    '''
    print("DOING LINES",crds) 
    xs, ys = crds
    xf, yf = self.final_cords.x, self.final_cords.y
    sign = ''
    if xs % 1 == 0 and ys % 1 == 0:
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
   
    while ys != yf - self.shiftL and ys != yf + self.shiftL:
      if ys < yf:
        ys += self.shiftL
      else:
        ys -= self.shiftL
      path.append((xs,ys))
   
    while xs != xf:
      if xs < xf:
        xs += self.shiftL
      else:
        xs -= self.shiftL
      path.append((xs,ys))
  
    if sign == '+':
      path.append((xs,ys+self.shiftL))
    else:
      path.append((xs,ys-self.shiftL))
    return True, path

  def make_path_squares(self):
    '''
    Function goes by squares until it reaches final cords or the square on cords (xs,ys) is occupied.
    If it's occupied then it switches to another function that goes by lines.
    It returns validity of path, array of cords (x,y) and last cords.
    '''
    xs, ys = self.start_cords.x, self.start_cords.y
    xf, yf = self.final_cords.x, self.final_cords.y
    xbf = 0
    ybf = 0
    path = []
    path.append((xs,ys))
    if xf % 1 == 0 and yf % 1 == 0:
      shift = self.shiftS
    else:
      shift = self.shiftL
    print("DOING SQUARES","shift is",shift)
    while xs != xf or ys != yf:
      xbf = xs
      if xs < xf and xs + shift <= 7:
        xs += shift
      elif xs > xf and xs - shift >= 0:
        xs -= shift
      ybf = ys
      if ys < yf and ys + shift <= 7:
        ys += shift
      elif ys > yf and ys - shift >= 0:
        ys -= shift
      if self.chess_status[(xs,ys)] == 0:
        path.append((xs,ys))
      elif xs == xf and ys == yf:
        path.append((xs,ys))
      else:
        return False, path, (xbf,ybf)
    return True, path, (xs,ys)

  def decide(self):
    '''
    This function decide, what function does make the path.
    It returns array of cords (x,y).
    '''
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
    '''
    cords - array of two cords [(xs,ys),(xf,yf)]
    board - array of cords [(x,y),(x,y),...]s
    Main function, calls other functions.
    Returns array of cords (x,y).
    '''
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
      board = [(1,1),(5,6),(6,6),(7,6)]
      cords = [(6,7),(3.5,2)]
    move.print_board(move.move(board,cords))
    i += 1
