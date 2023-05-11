import pygame
from Chess_logic import logic

"""Test function before chess logic is done"""

promotion_map = {(0, 0): "r", (0, 1): "n", (1, 0): "b", (1, 1): "q"}


class ChessGUI(object):
    pygame.init()
    pygame.mixer.init()
    _WIDTH = 480
    _HEIGHT = 480
    _NUM_PIECES = 12
    _RECT_SIZE = 60
    _PIECE_IMG_SIZE = 45

    _LIGHT_CHESS_COLOR = "#eeeed2"
    _DARK_CHESS_COLOR = "#769656"
    _BG_COLOR = "#636e72"

    _VIABLE_MOVE_COLOR = (116, 125, 140, 75)
    _VIABLE_MOVE_SURF = pygame.Surface([_RECT_SIZE, _RECT_SIZE], pygame.SRCALPHA)
    pygame.draw.circle(_VIABLE_MOVE_SURF, _VIABLE_MOVE_COLOR, [_RECT_SIZE * 0.5, _RECT_SIZE * 0.5], _RECT_SIZE * 0.20)

    _BOARD_IMG_OFFSET = [0, 0]

    _SELECTED_RECT_COLOR = (186, 202, 68)

    _HOVER_COLOR = (241, 242, 246, 200)
    _HOVER_SURF = pygame.Surface([_RECT_SIZE, _RECT_SIZE], pygame.SRCALPHA)
    pygame.draw.rect(_HOVER_SURF, _HOVER_COLOR, [0, 0, _RECT_SIZE, _RECT_SIZE], 5)

    """---AUDIO STUFF---"""
    _NORMAL_MOVE_SOUND = pygame.mixer.Sound("GUI/src/normal_move.mp3")
    _CAPTURE_MOVE_SOUND = pygame.mixer.Sound("GUI/src/capture.mp3")

    promotion_x, promotion_y = _WIDTH / 2 - _PIECE_IMG_SIZE * 1.5, _HEIGHT / 2 - _PIECE_IMG_SIZE * 1.5

    def __init__(self):
        self._PROMOTION_POPUP_WHITE = pygame.Surface([3 * self._PIECE_IMG_SIZE, 3 * self._PIECE_IMG_SIZE])
        self._PROMOTION_POPUP_BLACK = pygame.Surface([3 * self._PIECE_IMG_SIZE, 3 * self._PIECE_IMG_SIZE])
        self.piece_imgs = self.__load_images()
        self.chess_board = pygame.Surface([8 * self._RECT_SIZE, 8 * self._RECT_SIZE])
        self._mouse_down = False
        self._clicked_pos = None
        self._hover_pos = None
        self.__logic = logic.ChessBoard()
        self.valid_moves = []
        self._choosing_promotion = False
        self._choosing_promotion_color = None
        self._promotion_move = None

    def __load_images(self):
        """
        Loads images from "/src" directory
        :return: dictionary of white and black images
        """
        images = {'b': dict(), 'w': dict()}
        for i in range(1, self._NUM_PIECES + 1):
            if i <= 6:
                img = pygame.image.load("GUI/src/w" + str(i) + ".svg")
                images["w"][i] = img
            else:
                img = pygame.image.load("GUI/src/b" + str(i - 6) + ".svg")
                images["b"][i - 6] = img

        self._PROMOTION_POPUP_WHITE.fill((45, 52, 54))
        self._PROMOTION_POPUP_BLACK.fill((241, 242, 246))
        self._PROMOTION_POPUP_WHITE.blit(images["w"][2], (0.5 * self._PIECE_IMG_SIZE, 0.5 * self._PIECE_IMG_SIZE))
        self._PROMOTION_POPUP_WHITE.blit(images["w"][3], (1.5 * self._PIECE_IMG_SIZE, 0.5 * self._PIECE_IMG_SIZE))
        self._PROMOTION_POPUP_WHITE.blit(images["w"][4], (0.5 * self._PIECE_IMG_SIZE, 1.5 * self._PIECE_IMG_SIZE))
        self._PROMOTION_POPUP_WHITE.blit(images["w"][5], (1.5 * self._PIECE_IMG_SIZE, 1.5 * self._PIECE_IMG_SIZE))

        self._PROMOTION_POPUP_BLACK.blit(images["b"][2], (0.5 * self._PIECE_IMG_SIZE, 0.5 * self._PIECE_IMG_SIZE))
        self._PROMOTION_POPUP_BLACK.blit(images["b"][3], (1.5 * self._PIECE_IMG_SIZE, 0.5 * self._PIECE_IMG_SIZE))
        self._PROMOTION_POPUP_BLACK.blit(images["b"][4], (0.5 * self._PIECE_IMG_SIZE, 1.5 * self._PIECE_IMG_SIZE))
        self._PROMOTION_POPUP_BLACK.blit(images["b"][5], (1.5 * self._PIECE_IMG_SIZE, 1.5 * self._PIECE_IMG_SIZE))
        return images

    @staticmethod
    def __get_piece_color(chess_piece):
        piece_color = None
        if chess_piece != 0:
            piece_color = "b"
            if chess_piece < 0:
                piece_color = "w"
        return piece_color

    def __draw_chess_board(self, surf: pygame.Surface):
        """
        Draws chess board with pieces
        :param surf: pygame.Surface where the board will be drawn
        :return:
        """
        for row in range(8):
            for col in range(8):
                square_col = self._DARK_CHESS_COLOR
                if (row + col) % 2 == 0:
                    square_col = self._LIGHT_CHESS_COLOR
                if [row, col] == self._clicked_pos:
                    square_col = self._SELECTED_RECT_COLOR
                pygame.draw.rect(surf, square_col,
                                 [col * self._RECT_SIZE, row * self._RECT_SIZE, self._RECT_SIZE, self._RECT_SIZE])
                chess_piece = self.__logic.get_piece(row, col)
                piece_color = self.__get_piece_color(chess_piece)
                if piece_color:
                    x = col * self._RECT_SIZE + self._RECT_SIZE * 0.5 - self.piece_imgs[piece_color][
                        abs(chess_piece)].get_width() * 0.5
                    y = row * self._RECT_SIZE + self._RECT_SIZE * 0.5 - self.piece_imgs[piece_color][
                        abs(chess_piece)].get_height() * 0.5
                    if [row, col] == self._clicked_pos and self._mouse_down:
                        pass
                    else:
                        surf.blit(self.piece_imgs[piece_color][abs(chess_piece)], (x, y))
            """--- DRAW IT SEPARATELY ON TOP TO NOT BE OBSTRUCTED ---"""
            if self._mouse_down:
                chess_piece = self.__logic.get_piece(*self._clicked_pos)
                piece_color = self.__get_piece_color(chess_piece)
                row, col = self.__get_row_col(self._hover_pos[0], self._hover_pos[1])
                surf.blit(self._HOVER_SURF, (col * self._RECT_SIZE, row * self._RECT_SIZE))
                if piece_color:
                    surf.blit(self.piece_imgs[piece_color][abs(chess_piece)],
                              [self._hover_pos[0] - self._RECT_SIZE / 2, self._hover_pos[1] - self._RECT_SIZE / 2])
                """--- DRAW ALL VIABLE MOVES ---"""
                for move in self.valid_moves:
                    surf.blit(self._VIABLE_MOVE_SURF, [move[1] * self._RECT_SIZE, move[0] * self._RECT_SIZE])
            if self._choosing_promotion:

                if self._choosing_promotion_color == 1:
                    surf.blit(self._PROMOTION_POPUP_BLACK, (self.promotion_x, self.promotion_y))
                else:
                    surf.blit(self._PROMOTION_POPUP_WHITE, (self.promotion_x, self.promotion_y))

    def __get_row_col(self, x, y):
        return [y // self._RECT_SIZE, x // self._RECT_SIZE]

    def __play_sound(self, new_row, new_col):
        if self.__logic.get_piece(new_row, new_col) != 0:
            pygame.mixer.Sound.play(self._CAPTURE_MOVE_SOUND)
        else:
            pygame.mixer.Sound.play(self._NORMAL_MOVE_SOUND)

    def _determine_move(self):
        new_row, new_col = self.__get_row_col(*self._hover_pos)
        move = [self._clicked_pos, [new_row, new_col]]
        if self.__logic.is_valid_move(move):
            if (self.__logic.get_piece(*self._clicked_pos) == 1 and new_row == 7) or (
                    self.__logic.get_piece(*self._clicked_pos) == -1 and new_row == 0):
                # SHOW POPUP
                self._choosing_promotion = True
                self._choosing_promotion_color = logic.sign(self.__logic.get_piece(*self._clicked_pos))
                self._mouse_down = False
                self._promotion_move = move
                return
            # play sound
            self.__play_sound(new_row, new_col)
            # Do the move
            self.__logic.play_move(move)
        self._mouse_down = False
        self._clicked_pos = None

    def draw(self, win):
        win.fill(self._BG_COLOR)
        self.__draw_chess_board(self.chess_board)
        win.blit(self.chess_board, [0, 0])
        pygame.display.flip()

    def main(self):
        """---- SETUP ----"""
        win = pygame.display.set_mode((self._WIDTH, self._HEIGHT))
        pygame.display.set_caption("Speech Chess")
        self.draw(win)
        """---- Main Loop ----"""
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        pos = pygame.mouse.get_pos()
                        if not self._choosing_promotion:
                            self._clicked_pos = self.__get_row_col(pos[0] - self._BOARD_IMG_OFFSET[0],
                                                                   pos[1] - self._BOARD_IMG_OFFSET[1])
                            if self.__logic.get_piece(*self._clicked_pos) != 0:
                                self._mouse_down = True
                                self.valid_moves = self.__logic.get_valid_moves(self._clicked_pos)
                            else:
                                self._clicked_pos = None

                if event.type == pygame.MOUSEBUTTONUP:
                    if not self._choosing_promotion:
                        if event.button == pygame.BUTTON_LEFT and self._mouse_down:
                            self._determine_move()
                    else:
                        if event.button == pygame.BUTTON_LEFT:
                            pos = pygame.mouse.get_pos()
                            x = round((pos[0] - self.promotion_x - self._PIECE_IMG_SIZE / 2 - self._BOARD_IMG_OFFSET[
                                0]) // self._PIECE_IMG_SIZE)
                            y = round((pos[1] - self.promotion_y - self._PIECE_IMG_SIZE / 2 - self._BOARD_IMG_OFFSET[
                                1]) // self._PIECE_IMG_SIZE)
                            if (x in [0, 1]) and (y in [0, 1]):
                                chosen_promotion = promotion_map[(y, x)]
                                if self.__logic.is_valid_move(self._promotion_move, chosen_promotion):
                                    self.__play_sound(*self._promotion_move[1])
                                    self.__logic.play_move(self._promotion_move, chosen_promotion)
                                self._choosing_promotion = False

            if self._mouse_down:
                pos = pygame.mouse.get_pos()
                self._hover_pos = [pos[0] - self._BOARD_IMG_OFFSET[0], pos[1] - self._BOARD_IMG_OFFSET[1]]
            self.draw(win)


if __name__ == "__main__":
    gui = ChessGUI()
    gui.main()
