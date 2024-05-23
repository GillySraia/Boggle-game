from typing import List, Tuple, Iterable, Optional
import boggle_board_randomizer
from boggle_board_randomizer import *
import math
from copy import deepcopy






Path = List[Tuple[int, int]]
Board = List[List[str]]
# print(BOARD)


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """
    Checks if a given path on a board is valid and matches any word in the provided word list.

    Args:
        board (Board): A two-dimensional list representing the board.
        path (Path): A list of coordinate tuples representing the path on the board.
        words (Iterable[str]): An iterable of words to check against the path.

    Returns:
        Optional[str]: If the path is valid and matches a word, returns the matched word.
                       Otherwise, returns None.

    """
    # Check if all coordinates in the path are within the boundaries of the board
    if not is_coord_in_board(path, board):
        return None


    # Check if the path contains any duplicate coordinates
    if not are_duplicates_in_path(path):
        return None

    # Check if the path moves only to adjacent cells
    if not is_path_connected(path):
        return None

    # Construct a string representation of the path on the board
    word = word_from_path(path, board)


    # Check if the constructed path string matches any word in the provided word list
    if not is_word_in_words(word, words):
        return None

    return word


def is_coord_in_board(path, board):
    for coord in path:
        y, x = coord
        if 0 <= y < len(board) and 0 <= x < len(board[0]):
            continue
        else:
            return False
    return True


def is_path_connected(path):
    for i in range(len(path)-1):
        y, x = path[i]
        next_y, next_x = path[i+1]
        if abs(x - next_x) > 1 or abs(y - next_y) > 1:
            return False
    return True


def word_from_path(path, board):
    path_str = ""
    for coord in path:
        y, x = coord
        path_str += board[y][x]
    return path_str


def is_word_in_words(word, words):

    if word in words:
        return True
    else:
        return False


def are_duplicates_in_path(path):
    # Check if the path contains any duplicate coordinates
    copied_path = path[:]
    for coord in path:
        cur = copied_path.pop(0)
        if cur in copied_path:
            return False
        else:
            copied_path.append(cur)
    return True

board = [['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['I', 'G', 'K', 'L'], ['M', 'N', 'O', 'P']]
path = [(0, 0), (0, 1), (0, 2)]
words = ('ABC', 'CDE', 'ABCD')



def find_adjacent_cells(coord: tuple[int, int], board: Board):
    """
       Find the adjacent cells to a given coordinate on the board.

       Args:
           coord: The coordinate (y, x) for which to find adjacent cells.
           board: The game board.

       Returns:
           A list of adjacent cell coordinates.
       """
    y, x = coord
    # Generate all potential neighboring coordinates
    potential_neighbors = [(row, col) for row in range(y-1, y+2) for col in range(x-1, x+2)]
    potential_neighbors.remove((y, x))
    # Remove potential neighbors that fall outside the board's boundaries
    back_up = deepcopy(potential_neighbors)
    for cell in back_up:
        row, col = cell
        if (row < 0 or row >= len(board)) or (col < 0 or col >= len(board[0])):
            potential_neighbors.remove(cell)


    return potential_neighbors



def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
        Find paths of length n on the board that satisfy certain conditions.

        Args:
            n: The length of the paths to find.
            board: The game board.
            words: A collection of words.

        Returns:
            A list of paths of length n.
        """
    sub_words = create_subwords_set(words)
    paths = []
    # Iterate over all cells on the board
    for i in range(len(board)):
        for j in range(len(board[0])):
            cur_path = [(i, j)]  # Initialize current path with the current cell
            _find_paths_helper(n, board, words, cur_path, paths, i, j, sub_words)
    return paths


def _find_paths_helper(n, board, words, cur_path, paths, row, col, sub_words):
    word = word_from_path(cur_path, board)
    if word not in sub_words:
        return None

    if len(cur_path) == n:
        # Check if the current path is valid
        if is_valid_path(board, cur_path, words):
            copied_path = deepcopy(cur_path)
            paths.append(copied_path)   # Add a copy of the current path to the list of paths
        return None
    else:
        # Find adjacent cells and recursively explore each cell
        adjacent_cells = find_adjacent_cells((row, col), board)
        for cell in adjacent_cells:
            new_row, new_col = cell
            cur_path.append((new_row, new_col))   # Add the new cell to the current path
            _find_paths_helper(n, board, words, cur_path, paths, new_row, new_col, sub_words)
            cur_path.pop()  # Remove the last cell to backtrack and explore other adjacent cells




def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    sub_words = create_subwords_set(words)
    paths = []
    # Iterate over all cells on the board
    for i in range(len(board)):
        for j in range(len(board[0])):
            cur_path = [(i, j)]  # Initialize current path with the current cell
            word = word_from_path(cur_path, board)
            _find_length_n_words_helper(n, board, words, cur_path, word, paths, i, j, sub_words)
    return paths


def _find_length_n_words_helper(n, board, words, cur_path, word, paths, row, col, sub_words):

    if len(word) > n:
        return None

    if word not in sub_words:
        return None

    if len(word) == n:
        # Check if the current path is valid
        if is_valid_path(board, cur_path, words):
            copied_path = deepcopy(cur_path)
            if copied_path not in paths:
                paths.append(copied_path)   # Add a copy of the current path to the list of paths
        return None
    else:
        # Find adjacent cells and recursively explore each cell
        adjacent_cells = find_adjacent_cells((row, col), board)
        for cell in adjacent_cells:
            new_row, new_col = cell
            cur_path.append((new_row, new_col))   # Add the new cell to the current path
            word = word_from_path(cur_path, board)    # Evaluate word from cur_path
            _find_length_n_words_helper(n, board, words, cur_path, word, paths, new_row, new_col, sub_words)
            cur_path.pop() # Remove the last cell to backtrack and explore other adjacent cells



def create_subwords_set(words: set[str]):
    """ set of word permutations for earlier stop of recursion branch"""
    res_set = set()
    for word in words:
        permutations = set(map(lambda i: word[:i + 1], range(len(word))))
        res_set.update(permutations)
    return res_set


def create_words_set(file_path):
    with open(file_path, "r") as file:
        # Perform operations on the opened file
        lines = file.readlines()
        words_set = set()
        for line in lines:
            clean_line = line.rstrip('\n')
            words_set.add(clean_line)
        return words_set


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    res_dict = dict()
    side = len(board)
    max_len = max(set(len(word) for word in words))
    for n in range(1, max_len + 1):
        paths = find_length_n_paths(n, board, words)
        for path in paths:
            word = word_from_path(path, board)
            res_dict[word] = path
    return list(res_dict.values())





if __name__ == "__main__":

    file_name = "boggle_dict.txt"
    board = randomize_board()
    words = create_words_set(file_name)
    # paths = find_length_n_words(3, board, words)

    paths = max_score_paths(board, words)
    for path in paths:
        word = word_from_path(path, board)
        print(word, path)



#
# words = create_words_set("C:/Users/97254/dev/intro_to_cs/excercises/ex11/boggle_dict.txt")
# print(find_length_n_paths(3,[['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['I', 'G', 'K', 'L'], ['M', 'N', 'O', 'P']], ('ABC', 'CDE', 'ABCD')))
# print(max_score_paths([['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['I', 'G', 'K', 'L'], ['M', 'N', 'O', 'P']],('ABC', 'CDE', 'ABCD') ))
