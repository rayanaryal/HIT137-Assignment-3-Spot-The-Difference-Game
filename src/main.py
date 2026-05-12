import tkinter as tk

from .image_manager import ImageManager
from .game_logic import GameLogic
from .gui import SpotTheDifferenceGUI


def main():
    # Create the Tkinter root window
    root = tk.Tk()

    # Backend components
    image_manager = ImageManager()   # GUI will set the image path
    game_logic = GameLogic(image_manager)

    # Launch GUI
    SpotTheDifferenceGUI(root, game_logic)

    # Start Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
