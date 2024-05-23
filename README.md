# Boggle-game

## Description
In this game, the player has 3 minutes to find many words as possible on the board.

## Prerequisites
Python 3.8 or higher

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/GillySraia/Boggle-game.git
    cd Boggle-game
    ```

2. **Set up a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Project

1. **Run the main script**:
    ```bash
    python main.py
    ```

## Dependencies
- Pillow
- pygame

## Files
- `boggle_with_music.py`: The main entry point of the game.
- `Board.py`: Contains the `BoardObject` class.
- `ex11_utils.py`: Utility functions, including `create_words_set`.
- `BoggleModel.py`: The model for the Boggle game logic.
- `BoggleGUI.py`: The graphical user interface for the Boggle game.
- Other necessary files (e.g., images and sound files) should be placed in the appropriate directories.

## Usage
The game starts with an opening screen. Press the "Press to start" button to begin the game. The goal is to find as many words as possible within the given time.
