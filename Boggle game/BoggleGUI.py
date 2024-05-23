import tkinter as tk
from Board import BoardObject
from typing import Callable
from threading import Timer
import datetime
from PIL import ImageTk, Image
import pygame


#######################################################################################################################
# Setting constant values #
#######################################################################################################################

# Constants for color values
COLOR_HOVER_COLOR = "#DB7093"
REGULAR_COLOR = "black"
TEXT_OVER_COLOR = "white"
TEXT_COLOR = "white"
PRESSED_BUTTON = "#4C4E52"

# Constants for layout measurements
UPPER_LABELS_HEIGHT = 4
DISPLAY_CUR_WORD_WIDTH = 26
SUBMIT_WIDTH = 11
TIMER_WIDTH = 11


#######################################################################################################################
# This class creates the GUI #
#######################################################################################################################

class BoggleGUI:

    def __init__(self, board):
        # Create the main window.
        root = tk.Tk()
        root.title("Boggle Game")
        root.resizable(False, False)
        root.geometry("650x500")
        self._main_window = root

        # Create the word display area, submit button, and timer.
        self._create_word_display(0, 0, 4)
        self._create_submit_button(0, 4, 4)
        self.submit_button_clicked = False
        self._create_timer(0, 8, 4)

        # Store the Boggle board and initialize path and buttons.
        self.board = board
        self.path = []
        self.buttons = dict()

        # Create the letter buttons in the lower frame
        self._create_buttons_in_lower_frame()

        # Set the initial score and create the score label.
        self.set_score()
        self._create_score_label(1, 4, 8)

        # Create the label for found words
        self._create_found_words(2, 4, 8, 4)

    def _create_found_words(self, row, col, colspan, rowspan):
        # Creates the label for displaying found words.
        height = 10
        self.found_words_label = tk.Label(self._main_window, font=("Century Gothic", 15), bg=REGULAR_COLOR,
                                          relief="ridge", anchor="n", height=height, text="Found words:", fg=TEXT_COLOR)
        self.found_words_label.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, sticky=tk.NSEW)

    def _create_score_label(self, row, col, colspan):
        # Creates the label for displaying the score.
        height = 3
        self.score_label = tk.Label(self._main_window, font=("Century Gothic", 15), bg= REGULAR_COLOR, fg= TEXT_COLOR,
                                    relief="ridge", text="Score: " + str(self.score), anchor="center", height=height)
        self.score_label.grid(row=row, column=col, columnspan=colspan, sticky=tk.NSEW)

    def _create_buttons_in_lower_frame(self):
        # Creates the letter buttons in the lower frame.
        length = self.board.get_length()
        width = self.board.get_width()
        board_list = self.board.get_board()

        button_width = 10
        button_height = 5

        for i in range(0, length):
            for j in range(width):
                button = tk.Button(self._main_window,
                                   width=button_width,
                                   text=board_list[i][j],
                                   height=button_height,
                                   font= ("Century Gothic", 10),
                                   bg = REGULAR_COLOR,
                                   fg = TEXT_COLOR,
                                   compound="center")
                button.grid(row=i + 1, column=j, padx=1, pady=1)

                self.buttons[button] = ((i, j), board_list[i][j])
                button.configure(command=lambda btn=button: self._on_enter(btn))

    def _on_enter(self, button):
        # Keep the data of the button for later submission and change the color of the button.
        coord, letter = self.buttons[button]
        self.set_display(letter)
        self.set_path(coord)
        button.configure(bg= PRESSED_BUTTON)

    def _create_word_display(self, row, col, columnspan):
        # Creates the label for displaying the current word.
        self._display_cur_word = tk.Label(self._main_window, font=("Century Gothic", 15), bg=REGULAR_COLOR, fg=TEXT_COLOR,
                                          relief="ridge", text="", anchor="w", width=DISPLAY_CUR_WORD_WIDTH,
                                          height=UPPER_LABELS_HEIGHT)
        self._display_cur_word.grid(row=row, column=col, columnspan=columnspan, sticky="NSEW")

    def _create_submit_button(self, row, col, columnspan):
        # Creates the submit button.
        self.submit_btn = tk.Button(self._main_window,
                                    font=("Century Gothic", 15),
                                    bg=REGULAR_COLOR,
                                    fg=TEXT_COLOR,
                                    text="Submit",
                                    height=UPPER_LABELS_HEIGHT,
                                    width=SUBMIT_WIDTH)
        self.submit_btn.grid(row=row,
                             column=col,
                             columnspan=columnspan,
                             sticky="NSEW")

    def _create_timer(self, row, col, columnspan):
        # Creates the timer label.
        self.time_left = "03:00"
        self.timer = tk.Label(self._main_window,
                              text=f"{self.time_left}",
                              font=("Century Gothic", 15),
                              bg=REGULAR_COLOR,
                              fg=TEXT_COLOR,
                              width=TIMER_WIDTH,
                              height=UPPER_LABELS_HEIGHT)
        self.timer.grid(row=row, column=col, columnspan=columnspan, sticky="NSEW")

    def set_display(self, letter):
        # Sets the text for the current word display.
        self._display_cur_word["text"] += letter

    def clear_display(self):
        # Clears the text in the current word display.
        self._display_cur_word["text"] = ""

    def change_btn_color_back(self):
        # Changes the background color of buttons back to the regular color.
        for button in self.buttons.keys():
            button.configure(bg=REGULAR_COLOR)

    def set_path(self, coord):
        # Appends the coordinate to the path.
        self.path.append(coord)

    def clear_path(self):
        # Clears the path.
        self.path = []

    def set_score(self, score=0):
        # Sets the score.
        self.score = score

    def run(self):
        # Runs the GUI main loop.
       self._main_window.mainloop()
