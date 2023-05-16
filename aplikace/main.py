import pygame
from Chess_logic import logic
from GUI import menu
from Speech_to_moves import VoiceControl
from Chess_AI import ChessAI

"""Test function before chess logic is done"""

promotion_map = {(0, 0): "r", (0, 1): "n", (1, 0): "b", (1, 1): "q"}
_STOCKFISH_ENGINE_PATH = "/opt/homebrew/bin/stockfish"


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
    _CHECK_MOVE_SOUND = pygame.mixer.Sound("GUI/src/move-check.mp3")
    _PROMOTION_MOVE_SOUND = pygame.mixer.Sound("GUI/src/promote.mp3")
    _CASTLE_MOVE_SOUND = pygame.mixer.Sound("GUI/src/castle.mp3")
    """--- GAME MODES ---"""
    _PVP = 1
    _PVAI = 2

    promotion_x, promotion_y = _WIDTH / 2 - _PIECE_IMG_SIZE * 1.5, _HEIGHT / 2 - _PIECE_IMG_SIZE * 1.5

    def __init__(self):
        """---------- VISUAL STUFF --------"""
        self._PROMOTION_POPUP_WHITE = pygame.Surface([3 * self._PIECE_IMG_SIZE, 3 * self._PIECE_IMG_SIZE])
        self._PROMOTION_POPUP_BLACK = pygame.Surface([3 * self._PIECE_IMG_SIZE, 3 * self._PIECE_IMG_SIZE])
        self.piece_imgs = self.__load_images()
        self.chess_board = pygame.Surface([8 * self._RECT_SIZE, 8 * self._RECT_SIZE])
        self._mouse_down = False
        self._clicked_pos = None
        self._hover_pos = None
        self._choosing_promotion = False
        self._choosing_promotion_color = None
        self._promotion_move = None
        """----------- FUNCTIONAL STUFF -----------"""
        self.__logic = logic.ChessBoard()
        self.valid_moves = []
        self._speech_recog = None
        self._stockfish = None
        self.my_color = -1
        self._recently_played_move = ""
        self._recent_promotion = ""
        self._was_castle = False
        self._mode = self._PVP

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

    def __play_sound(self, move, promotion):
        self._was_castle = False
        if abs(self.__logic.get_piece(*move[0])) == 6 and abs(self.__logic.get_piece(*move[1])) == 2:
            pygame.mixer.Sound.play(self._CASTLE_MOVE_SOUND)
            self._was_castle = True
            print("castle")
        elif promotion != "":
            print("promotion")
            pygame.mixer.Sound.play(self._PROMOTION_MOVE_SOUND)
        else:
            if self.__logic.get_piece(*move[1]) != 0:
                print("capture")
                pygame.mixer.Sound.play(self._CAPTURE_MOVE_SOUND)
            else:
                print("normal")
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
            self.play_move(move)
        self._mouse_down = False
        self._clicked_pos = None

    def __init_speech(self) -> None:
        """
        Initializes speech recognition module and starts new thread
        :return: None
        """
        self._speech_recog = VoiceControl.VoiceControl(debug=True, info=True, recordTime=4, lan="en-US")
        self._speech_recog.start()

    def __init_stockfish(self) -> None:
        """
        Initializes stockfish engine and sets parameters
        :return: None
        """
        self._stockfish = ChessAI.ChessAI(_STOCKFISH_ENGINE_PATH)
        self._stockfish.set_parameters(skill_level=0)

    def _eval_player_move(self, event):
        """
        Evaluates what move is being played based on users input
        :param event: pygame.event
        :return:
        """
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
                        self.play_move(self._promotion_move, chosen_promotion)
                        self._choosing_promotion = False

    def _play_stockfish_move(self, move, promotion=""):
        if self._was_castle:
            # castle
            if move[1][1] == 7:
                move[1][1] = 6
            elif move[1][1] == 0:
                move[1][1] = 2
        if move:
            move = self._stockfish.get_move(logic.row_col_to_cmd(*move[0]) + logic.row_col_to_cmd(*move[1]) + promotion)
            print(move)
        else:
            move = self._stockfish.get_move("")
        move = [logic.cmd_to_row_col(move[0:2]), logic.cmd_to_row_col(move[2:4])]

        if len(move) == 5:
            promotion = move[4]
        self.play_move(move, promotion)

    def __reset_board(self) -> None:
        print("PLAYER: ", self.__logic.get_player_playing() * -1, " WON")
        self.__logic.reset_board()
        self._recently_played_move = ""
        self._recent_promotion = ""
        if self._mode == self._PVAI:
            self.__init_stockfish()

    def play_move(self, move, promotion="") -> None:
        """
        Plays move and handles all of the logic (sending to Arduino, updating board etc...)
        :param: move = [[start row, start col], [end row, end col]]
        :return: None
        """
        if self.__logic.is_valid_move(move, promotion=promotion):
            # play sound
            print(move)
            self.__play_sound(move, promotion)
            # Do the move
            self.__logic.play_move(move, promotion)
            self._recently_played_move = move
            self._recent_promotion = promotion
            if self.__logic.is_checkmate():
                self.__reset_board()
            ## TODO: move to commands
            ## TODO: send to serial

    def draw(self, win: pygame.Surface) -> None:
        """
        Draws chess board to win
        :param win: pygame.Surface
        :return: None
        """
        win.fill(self._BG_COLOR)
        self.__draw_chess_board(self.chess_board)
        win.blit(self.chess_board, [0, 0])
        pygame.display.flip()

    def main(self) -> None:
        """---- SETUP ----"""
        win = pygame.display.set_mode((self._WIDTH, self._HEIGHT))
        pygame.display.set_caption("Speech Chess")
        """ --- SETTINGS SCREEN ---"""
        run = True
        q = False
        _menu = menu.Menu([self._WIDTH, self._HEIGHT])
        _speech_commands = False
        mode = self._PVP
        clock = pygame.time.Clock()
        while run:
            clock.tick(30)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    q = True
            if _menu.update(events):
                settings = _menu.get_settings()
                # [1v1, 1vAI, speech_commands]
                mode = None
                if settings[0]:
                    mode = self._PVP
                elif settings[1]:
                    mode = self._PVAI
                _speech_commands = settings[2]
                if mode:
                    run = False

            win.blit(_menu.screen, [0, 0])
            pygame.display.flip()

        """---- Start speech recog thread"""
        self._mode = mode
        if _speech_commands:
            self.__init_speech()
        if mode == self._PVAI:
            self.__init_stockfish()
        """---- Main Loop ----"""
        self.draw(win)
        run = not q
        while run:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    if _speech_commands:
                        self._speech_recog.runControl = False
                        self._speech_recog.join(1)

                if mode == self._PVAI and self.__logic.get_player_playing() != self.my_color:
                    pass
                else:
                    self._eval_player_move(event)

            if mode == self._PVAI and self.__logic.get_player_playing() != self.my_color:
                self._play_stockfish_move(self._recently_played_move, self._recent_promotion)

            if _speech_commands:
                if self._speech_recog.dataReady:
                    move = self._speech_recog.read_data()
                    if mode == self._PVAI and self.__logic.get_player_playing() != self.my_color:
                        pass
                    elif mode == self._PVAI and self.__logic.get_player_playing() == self.my_color:
                        if self.__logic.is_valid_move(move):
                            print("Voice command valid- playing move: ", move)
                            self.play_move(move)
                        else:
                            print("voice command not valid!")

                    elif mode == self._PVP:
                        if self.__logic.is_valid_move(move):
                            print("Voice command valid- playing move: ", move)
                            self.play_move(move)
                        else:
                            print("voice command not valid!")

            if self._mouse_down:
                pos = pygame.mouse.get_pos()
                self._hover_pos = [pos[0] - self._BOARD_IMG_OFFSET[0], pos[1] - self._BOARD_IMG_OFFSET[1]]
            self.draw(win)


if __name__ == "__main__":
    gui = ChessGUI()
    gui.main()
