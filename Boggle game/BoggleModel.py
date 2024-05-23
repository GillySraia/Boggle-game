from ex11_utils import *
from Board import BoardObject


#######################################################################################################################
# This class creates the model - the logic of the game #
#######################################################################################################################


class BoggleModel:

    board: list[list[int]]
    words: set[str]
    score: int
    words_on_board:  set[str]
    found_words: set[str]
    path: list[tuple[int, int]]

    def __init__(self, board, words):
        # Initializes the BoggleModel object.
        self.board = board
        self.words = words
        self.score = 0
        self.found_words = set()
        self.path = []

    def get_score(self):
        # Returns the current score.
        return self.score

    def set_score(self):
        # Sets the score based on the current path.
        self.score += (len(self.path) ** 2)

    def one_try(self):
        """Attempts to find a word in the current path."""

        # Check if the path contains any duplicate coordinates
        if not are_duplicates_in_path(self.path):
            return False

        # Check if the path moves only to adjacent cells
        if not is_path_connected(self.path):
            return False

        # Construct a string representation of the path on the board.
        word = word_from_path(self.path, self.board)

        # Check if the constructed path string matches any word in the provided word list
        if not is_word_in_words(word, self.words):
            return False

        if word in self.found_words:
            return False

        self.found_words.add(word)
        self.set_score()
        return True

    def clear_path(self):
        # Clears the current path.
        self.cur_path = []

    def set_path(self, path):
        # Sets the current path.
        self.path = path
