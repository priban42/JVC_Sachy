"""
Implementation of AI player class for our voice controlled chess project using Stockfish engine version 15.1 
(download available at https://stockfishchess.org)

It requires you to have the Stockfish engine executable file and 'stockfish' python lib installed 
"""

from stockfish import Stockfish

_HASH_SIZE_DEFAULT = 256
_THREADS_DEFAULT = 1
_DEPTH_DEFAULT = 15
_MOVE_TIME_DEFAULT = 3000
_SKILL_LEVEL_DEFAULT = 1

class ChessAI(object):
    """
    The ChessAI object contains information about current state of the board in 'engine' attribute and 
    its methods are able to find the best move for AI player and set parameters of Stockfish engine.
    I recommend you call

    Parameters
    ----------
    path : str
        Path to Stockfish executable file
    depth : int
        Depth is how many moves the Stockfish engine looks ahead, the greater the number the 'smarter' the engine is (default is 18)
    move_time_ms : int
        The time in miliseconds in which Stockfish engine has to return the best move it found (defaault is 3000)
    
    Attributes
    -------
    move_time : int
        This is where you store move_time_ms
    engine : class
        This is where the Stockfish engine class is stored for our purposes
    """

    def __init__(self, path: str, depth: int = _DEPTH_DEFAULT,  move_time_ms: int = _MOVE_TIME_DEFAULT):
        self.move_time = move_time_ms
        self.engine = Stockfish(path, depth, {"Skill Level": _SKILL_LEVEL_DEFAULT, "Threads": _THREADS_DEFAULT, "Hash": _HASH_SIZE_DEFAULT})

    def get_move(self, players_move: str) -> str:
        """
        Method that takes in player's move in algebraic notation (e.g. "e2e4") and returns the best move AI opponent can make as 
        string in algebraic notaion

        Parameters
        ----------
        players_move : str
            Move that a real player executed, if you send empty string "" with the first move of the game
            the engine will start game as white, otherwise it will react to your first move as black

            Example: "e2e4"

        Returns
        -------
        str
            String representing move made by AI opponent
        """

        self.engine.make_moves_from_current_position([players_move])
        ret = self.engine.get_best_move(self.move_time, self.move_time)
        self.engine.make_moves_from_current_position([ret])

        return ret
    
    def set_parameters(self, skill_level: int = _SKILL_LEVEL_DEFAULT, threads: int = _THREADS_DEFAULT, hash_size: int = _HASH_SIZE_DEFAULT) -> None:
        """
        Sets parameters of Stockfish engine

        Parameters
        ----------
        skill_level : int
            Desired skill level of Stockfish engine (default is 1 and beyond level 7 is pretty much unbeatable, min 0 max 20)
        threads : int
            Number of threads Stockfish engine will be allowed to use (default is 1)
        hash_size : int 
            Size of RAM (in MB) that Stockfish will be allowed to use, use powers of 2 (default is 256)

        Returns
        -------
        None
        """

        self.engine.update_engine_parameters({"Skill Level": skill_level, "Threads": threads, "Hash": hash_size})


if __name__ == "__main__":
    """ player_move = str(input("Enter first chess move (for example e2e4): "))
    opponent = ChessAI(".\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")
    print(player_move)
    opponent.set_parameters(1400, 1, 512)
    print(opponent.get_move(player_move)) """
    opponent = ChessAI(".\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")
    opponent.set_parameters(900, 1, 1024)
    print(opponent.engine.get_parameters())
    opponent.engine.make_moves_from_current_position(["e2e4", "f7f6", "e4e5", "e7e6", "e5f6", "e6e5", "f6g7"])
    print(opponent.get_move("e5e4"))
    print(opponent.engine.get_evaluation())
    print(opponent.engine.get_wdl_stats())
