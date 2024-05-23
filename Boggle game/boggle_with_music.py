import tkinter as tk
import Board
import boggle_board_randomizer
from Board import BoardObject
import ex11_utils
from PIL import ImageTk, Image
import BoggleModel
import BoggleGUI
import pygame

#######################################################################################################################
# Setting constant values #
#######################################################################################################################

# Constants for color values
COLOR_HOVER_COLOR = "#DB7093"
REGULAR_COLOR = "black"
TEXT_OVER_COLOR = "white"
TEXT_COLOR = "white"

# Constant for the game time in seconds
GAME_TIME = 180

# Constants for layout measurements
UPPER_LABELS_HEIGHT = 4
DISPLAY_CUR_WORD_WIDTH = 26
SUBMIT_WIDTH = 11
TIMER_WIDTH = 11


#######################################################################################################################
# This class, the controller, links the other classes - the model and the GUI #
#######################################################################################################################


class BoggleController:
    def __init__(self):
        # Initialize the opening screen and load the dictionary of words.
        self.create_opening_screen()
        self.words = ex11_utils.create_words_set("boggle_dict.txt")

        # Initialize Pygame mixer for the music in the background.
        pygame.mixer.init()

    def create_opening_screen(self):
        # Create the opening screen with a background image and a start button.
        root = tk.Tk()
        root.title("Boggle Game")
        root.resizable(False, False)
        root.geometry("650x500")
        self.opening_screen = root
        self.timer = GAME_TIME

        # Load and resize the background image.
        image = Image.open("opening_pic.png")
        image = image.resize((650, 500), Image.LANCZOS)  # Adjust the size of the image to fit your window
        background_image = ImageTk.PhotoImage(image)

        # Create a label for the background image.
        background_label = tk.Label(self.opening_screen, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image

        # Create the start button.
        self.create_start_button()
        start_action = self.create_start_action()
        self.start_button.configure(command=start_action)

    def play_background_music(self, file_path):
        # Load the background music file
        pygame.mixer.music.load(file_path)

        # Play the background music in an infinite loop (-1).
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)

    def create_start_button(self):
        # Create the start button for the game screen.
        self.start_button = tk.Button(self.opening_screen,
                                 height=3,
                                 width=15,
                                 font= ("Century Gothic", 15),
                                 text="Press to start",
                                 bg="black",
                                 fg="red",
                                 borderwidth=0,
                                 highlightthickness=1)
        self.start_button.place(x=225, y=350)

    def create_start_action(self):
        # Create the action function for the start button.
        def fun():
            self.opening_screen.destroy()
            self.board = Board.BoardObject()
            self.game = BoggleGUI.BoggleGUI(self.board)
            self.logic = BoggleModel.BoggleModel(self.game.board.get_board(), self.words)
            self.time = GAME_TIME
            submit_action = self.create_submit_action()
            self.game.submit_btn.configure(command=submit_action)
            self.create_clock()
            self.play_background_music("Stranger_Things_Theme_Song.mp3")
        return fun

    def create_submit_action(self):
        # Create the action function for the submit button.
        def fun() -> None:
            path = self.game.path
            self.logic.set_path(path)
            self.game.clear_path()
            self.game.clear_display()
            self.game.change_btn_color_back()
            if self.logic.one_try():
                cur_score = self.logic.get_score()
                self.game.score_label.configure(text = "Score: " + str(cur_score))
                text = "Found Words: \n " + ", ".join(list(self.logic.found_words))
                self.game.found_words_label.configure(text = text, wraplength=200)

                self.logic.clear_path()

        return fun

    def create_clock(self):
        # Update the game clock display every second.
        if self.timer == 0:
            self._end_game()
            self.timer = 0
            return
        min = self.timer // 60
        sec = self.timer % 60
        txt = str(min).zfill(2) + ":" + str(sec).zfill(2)
        self.game.timer.configure(text=txt)
        self.timer -= 1
        self.game._main_window.after(1000, self.create_clock)

    def _end_game(self):
        # End the game by destroying the main window and creating the last screen.
        self.game._main_window.destroy()
        self.stop_music()
        self._create_last_screen()

    def stop_music(self):
        # Stop the background music
        pygame.mixer.music.stop()

    def _create_last_screen(self):
        # Create the last screen and options to play again or quit.
        root = tk.Tk()
        root.title("Boggle Game")
        root.resizable(False, False)
        root.geometry("650x500")
        self._last_screen = root

        # Load and resize the background image.
        image = Image.open("SEE_YOU_IN_THE_UPSIDEDOWN.png")
        image = image.resize((650, 500), Image.LANCZOS)  # Adjust the size of the image to fit your window
        background_image = ImageTk.PhotoImage(image)

        # Create a label for the background image.
        background_label = tk.Label(self._last_screen, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image

        # Create the "Play again" button.
        self.create_play_again_btn()

        # Create the "Quit" button.
        self.create_quit_btn()

        # Play background music and set the volume.
        self.play_background_music("Stranger_Things_Season_4_Soundtrack_Running_Up_That_Hill_Orchestral.mp3")
        pygame.mixer.music.set_volume(0.4)

    def create_play_again_btn(self):
        # Create the "Play again" button for the last screen.
        self.play_again_btn = tk.Button(self._last_screen,
                                    font=("Century Gothic", 15),
                                    bg=REGULAR_COLOR,
                                    fg=TEXT_COLOR,
                                    text="Play again!",
                                    height=UPPER_LABELS_HEIGHT,
                                    width=SUBMIT_WIDTH)
        self.play_again_btn.place(x=360, y=330)
        action = self.create_resume_action()
        self.play_again_btn.configure(command=action)

    def create_quit_btn(self):
        # Create the "Quit" button for the last screen
        self.quit_btn = tk.Button(self._last_screen,
                                        font=("Century Gothic", 15),
                                        bg=REGULAR_COLOR,
                                        fg=TEXT_COLOR,
                                        text="Quit",
                                        height=UPPER_LABELS_HEIGHT,
                                        width=SUBMIT_WIDTH,
                                        )
        self.quit_btn.configure(command=self._last_screen.destroy)
        self.quit_btn.place(x=180, y=330)

    def create_resume_action(self):
        # Create the action function for the "Play again" button.
        def fun():
            self._last_screen.destroy()
            self.stop_music()
            self.create_start_action()
            main()

        return fun


def main():
    # Create an instance of BoggleController.
    controller = BoggleController()

    # Open the opening screen.
    controller.opening_screen.mainloop()


if __name__ == "__main__":
    main()


