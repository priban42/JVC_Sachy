import chess

_piece_map = {"p": 1, "r": 2, "n": 3, "b": 4, "q": 5, "k": 6,
              "P": -1, "R": -2, "N": -3, "B": -4, "Q": -5, "K": -6}


def cmd_to_row_col(cmd: str):
    """
    :param cmd: eg: "a1" or "h8" ...
    :return: [row, col] in board
    """
    return [8 - int(cmd[1]), ord(cmd[0]) - 97]


def row_col_to_cmd(row, col):
    """
    :param row: of piece
    :param col: of piece
    :return: cmd as "a1" ...
    """
    return chr(col + 97) + str(8 - row)


def sign(num):
    if num == 0:
        return 1
    return num / abs(num)


class ChessPiece(object):
    def __init__(self, color):
        self.num = 0
        self._valid_move_squares = []
        ## black = 1, white = -1
        self.color = color

    @staticmethod
    def _in_range(pos):
        if (0 <= pos[0] < 8) and (0 <= pos[1] < 8):
            return True
        return False

    def get_num(self):
        return self.num * self.color

    def get_all_moves(self, pos):
        return []


class Pawn(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.num = 1

        """ all move patterns in +row, +col from passed row, col"""
        self._valid_move_squares = [(1, 0), (2, 0), (1, 1), (1, -1)]

    def get_all_moves(self, pos):
        moves = []
        for move in self._valid_move_squares:
            row, col = round(pos[0] + move[0] * self.color), pos[1] + move[1]

            if self._in_range([row, col]):
                moves.append([row, col])
        return moves


class Rook(ChessPiece):
    def __init__(self, color):
        super().__init__(color)
        self.num = 2

        """ Valid moves but in direction"""
        self._valid_move_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def get_all_moves(self, pos):
        moves = []
        for dir in self._valid_move_dirs:
            row, col = pos[0] + dir[0], pos[1] + dir[1]
            while self._in_range([row, col]):
                moves.append([row, col])
                row += dir[0]
                col += dir[1]
        return moves


class Horse(Pawn):
    def __init__(self, color):
        super().__init__(color)
        self.num = 3

        """ Valid moves in patterns"""
        self._valid_move_squares = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]


class Bishop(Rook):
    def __init__(self, color):
        super().__init__(color)
        self.num = 4

        """ Valid moves but in direction"""
        self._valid_move_dirs = [(1, 1), (-1, -1), (1, -1), (-1, 1)]


class Queen(Rook):
    def __init__(self, color):
        super().__init__(color)
        self.num = 5

        """ Valid moves but in direction"""
        self._valid_move_dirs = [(1, 1), (-1, -1), (1, -1), (-1, 1), (1, 0), (-1, 0), (0, 1), (0, -1)]


class King(Pawn):
    def __init__(self, color):
        super().__init__(color)
        self.num = 6

        """ Valid moves in patterns"""
        self._valid_move_squares = [(1, 0), (1, -1), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]


pieces = [ChessPiece, Pawn, Rook, Horse, Bishop, Queen, King]


class ChessBoard(object):
    def __init__(self):
        self.__logic = chess.Board()
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self._update_board()
        self.player_playing = -1

    def _update_board(self):
        """--- Loads current state of board from self.__logic and converts it ---"""
        str_board = self.__logic.fen()
        rows = str_board.split(" ")[0].split("/")
        for r, row in enumerate(rows):
            c = 0
            col_index = 0
            while c < 8:
                if rows[r][col_index].isnumeric():
                    num = int(rows[r][col_index])
                    for i in range(num):
                        self.board[r][c + i] = ChessPiece(1)
                    c += num
                else:
                    self.board[r][c] = pieces[abs(_piece_map[rows[r][col_index]])](sign(_piece_map[rows[r][col_index]]))
                    c += 1
                col_index += 1
        #self.__print_board()

    def get_piece(self, row, col):
        """
        :param row, col: row, col in board
        :return: piece number
        """
        return self.board[row][col].get_num()

    def __print_board(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                print(self.board[row][col].get_num(), end=" ")
            print()

    def get_valid_moves(self, pos):
        """
        :param pos: row, col of the piece
        :return: all moves that can be done with the piece
        """
        valid_moves = []
        all_moves = self.board[pos[0]][pos[1]].get_all_moves(pos)
        init_move = row_col_to_cmd(pos[0], pos[1])
        for move in all_moves:
            """ convert to 'a2a3' - notation"""
            if chess.Move.from_uci(init_move + row_col_to_cmd(*move)) in self.__logic.legal_moves:
                valid_moves.append(move)
            if abs(self.board[pos[0]][pos[1]].get_num()) == 1:
                if chess.Move.from_uci(init_move + row_col_to_cmd(*move) + "q") in self.__logic.legal_moves:
                    valid_moves.append(move)
        return valid_moves

    def get_player_playing(self):
        """ -1 if white, 1 if black"""
        return self.player_playing

    def __move_to_str(self, move):
        return row_col_to_cmd(*move[0]) + row_col_to_cmd(*move[1])

    def is_valid_move(self, move, promotion=""):
        """
        :param promotion: if pawn promotion -- promotion = "q/k/r/b" else empty string
        :param move: ((start_row, start_col), (end_row, end_col))
        :return: True/False
        """
        if move[0] == move[1]:
            return False
        move_str = self.__move_to_str(move) + promotion
        if not promotion:
            return (chess.Move.from_uci(move_str) in self.__logic.legal_moves) or (chess.Move.from_uci(move_str + "q") in self.__logic.legal_moves)
        else:
            return chess.Move.from_uci(move_str) in self.__logic.legal_moves

    def play_move(self, move, promotion=""):
        """
        :param promotion: if pawn promotion -- promotion = "q/k/r/b" else empty string
        :param move: ((start_row, start_col), (end_row, end_col))
        :return: True/False - if move was executed or not
        """
        if self.is_valid_move(move, promotion):
            self.__logic.push_san(self.__move_to_str(move) + promotion)
            self.player_playing *= -1
            self._update_board()
            return True
        return False


if __name__ == "__main__":
    board = ChessBoard()
    print(board.is_valid_move([[6, 2], [6, 2]]))
