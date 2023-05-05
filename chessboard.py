
class my_chessboard:
    #white + ;black -
    #empty 0;
    #pawn 1;
    #rook 2;
    #knight 3;
    #bishop 4;
    #queen 5;
    #king 6;
    board = []
    def __init__(self):
        import pygame
        self.board=[[ 2, 3, 4, 5, 6, 4, 3, 2],
                    [ 1, 1, 1, 1, 1, 1, 1, 1],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [ 0, 0, 0, 0, 0, 0, 0, 0],
                    [-1,-1,-1,-1,-1,-1,-1,-1],
                    [-2,-3,-4,-5,-6,-4,-3,-2]]
    
    def my_print(self):
        for i in range(0,len(self.board)):
            print(self.board[i])

    def chess_coord_to_row_col(self,s):
        row = int(s[1])-1
        col = ord(chr(s[0].upper()))-ord('A')
        return row,col

    def return_piece_on_position(self,pos:str):
        row,col=self.chess_coord_to_row_col(pos)
        return self.board[row][col]

    def is_neutral_by_row(self,row:int,col:int):
        if(self.board[row][col]):
            return True
        return False

    def is_in_bounds(self,pos:str):
        row,col=self.chess_coord_to_row_col(pos)
        if(row<0)or(col<0)or(row>7)or(col>7):
            return False
        return True
    
    def is_enemy(self,pos,piece):
        if not(self.is_in_bounds(pos)):
            if(self.return_piece_on_position(pos)*piece<0):
                return True
            else:
                return False

    def is_neutral(self,pos):
        if not(self.is_in_bounds(pos)):
            if(self.return_piece_on_position(pos)==0):
                return True
            else:
                return False

    def check_knight_movement(self,start:str,fin:str):
        if(self.is_in_bounds(fin)):
            start_row,start_col=self.chess_coord_to_row_col(start)
            fin_row,fin_col=self.chess_coord_to_row_col(fin)

            if(self.is_enemy(fin,self.return_piece_on_position(start))or 
               self.is_neutral(fin,self.return_piece_on_position(start))):
                
                if((abs(start_row-fin_row)==2)and(abs(start_col-fin_col==1))or
                   (abs(start_row-fin_row)==1)and(abs(start_col-fin_col==2))):
                    return True
        return False

    def check_bishop_movement(self,start:str,fin:str):
        if(self.is_in_bounds(fin)):
            start_row,start_col=self.chess_coord_to_row_col(start)
            fin_row,fin_col=self.chess_coord_to_row_col(fin)
            
            if(abs(start_row-fin_row)==abs(start_col-fin_col)):
                dir=[-1*(start_row-fin_row)/abs(start_row-fin_row),-1*(start_col-fin_col)/abs(start_col-fin_col)]
                dist=abs(start_row-fin_row)
                for i in range(0,dist-1):
                    if(not(self.is_neutral_by_row(start_row+dir[0]*i,start_col+dir[1]*i))):
                        return False
                if(self.is_neutral(fin) or self.is_enemy(fin)):
                    return True
                
        return False