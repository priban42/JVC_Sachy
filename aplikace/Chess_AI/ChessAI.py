"""
Implementation of AI player class for our voice controlled chess project using Stockfish engine

It requires you to have the Stockfish engine executable file and 'stockfish' python lib installed 
"""

from stockfish import Stockfish

_HASH_SIZE_DEFAULT = 512
_ELO_DEFAULT = 800
_THREADS_DEFAULT = 1
_DEPTH_DEFAULT = 18
_MOVE_TIME_DEFAULT = 3000

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
        self.engine = Stockfish(path, depth, {"UCI_Elo": _ELO_DEFAULT, "Threads": _THREADS_DEFAULT, "Hash": _HASH_SIZE_DEFAULT})

    def get_move(self, players_move: str) -> str:
        """
        Method that takes in player's move and returns the best move AI opponent can make as string in algebraic notaion

        Parameters
        ----------
        players_move : str
            Move that a real player executed, if you send empty string "" with the first move of the game
            the engine will start game as white, otherwise it will react to your first move as black

        Returns
        -------
        str
            String representing move made by AI opponent
        """

        self.engine.make_moves_from_current_position([players_move])
        
        return self.engine.get_best_move(self.move_time, self.move_time)
    
    def set_parameters(self, elo: int = _ELO_DEFAULT, threads: int = _THREADS_DEFAULT, hash_size: int = _HASH_SIZE_DEFAULT) -> None:
        """
        Sets parameters of Stockfish engine

        Parameters
        ----------
        elo : int
            Desired elo rating of AI opponent (default is 800)
        threads : int
            Number of threads Stockfish engine will be allowed to use (default is 1)
        hash_size : int 
            Size of RAM (in MB) that Stockfish will be allowed to use, use powers of 2 (default is 512)

        Returns
        -------
        None
        """

        self.engine.update_engine_parameters({"UCI_Elo": elo, "Threads": threads, "Hash": hash_size})


if __name__ == "__main__":
    player_move = str(input("Enter first chess move (for example e2e4): "))
    opponent = ChessAI(".\stockfish_15.1_win_x64_avx2\stockfish-windows-2022-x86-64-avx2.exe")
    print(player_move)
    opponent.set_parameters(1400, 1, 512)
    print(opponent.get_move(player_move))