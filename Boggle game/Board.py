import boggle_board_randomizer
from boggle_board_randomizer import *
from typing import List, Tuple, Iterable, Optional

class BoardObject:

    def __init__(self):
        self.__board = boggle_board_randomizer.randomize_board()
        self.__size = boggle_board_randomizer.BOARD_SIZE

    def get_width(self):
        #num of columns
        return len(self.__board[0])

    def get_length(self):
        #num of rows
        return len(self.__board)

    def get_str(self, path: List[Tuple[int, int]]):
        """ returns a str of given path"""
        # Construct a string representation of the path on the board
        path_str = ""
        for coord in path:
            y, x = coord
            path_str += self.__board[y][x]
        return path_str

    def get_board(self):
        return self.__board


