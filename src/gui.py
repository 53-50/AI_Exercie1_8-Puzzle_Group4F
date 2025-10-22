import tkinter as tk
from tkinter import messagebox
import random
import time


class SlidePuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title(" Slide Puzzle")

        self.size = 3
        self.tiles = list(range(1, self.size * self.size)) + [0]
        self.moves = 0
        self.start_time = None

        self.buttons = []
        self.create_widgets()
        self.shuffle_tiles()

    def create_widgets(self):
            frame = tk.Frame(self.root)
            frame.grid(row=0, column=0, padx=10, pady=10)

            for i in range(self.size):
                row = []
                for j in range(self.size):
                    button = tk.Button(frame, width=4, height=2, font=("Arial", 18),
                                       command=lambda i=i, j=j: self.move_tile(i, j))
                    button.grid(row=i, column=j)
                    row.append(button)
                self.buttons.append(row)

            self.moves_label = tk.Label(self.root, text="Moves: 0", font=("Arial", 14))
            self.moves_label.grid(row=1, column=0, pady=5)

            self.timer_label = tk.Label(self.root, text="Time: 0s", font=("Arial", 14))
            self.timer_label.grid(row=2, column=0, pady=5)

            manhattan_button = tk.Button(self.root, text="Manhattan", command=self.manhattan, font=("Arial", 14))
            manhattan_button.grid(row=3, column=0, pady=5)

            hamming_button = tk.Button(self.root, text="Hamming", command=self.hamming, font=("Arial", 14))
            hamming_button.grid(row=4, column=0, pady=5)


            reset_button = tk.Button(self.root, text="Reset", command=self.reset_game, font=("Arial", 14))
            reset_button.grid(row=5, column=0, pady=5)

            quit_button = tk.Button(self.root, text="Quit", command=self.root.quit, font=("Arial", 14))
            quit_button.grid(row=6, column=0, pady=5)

    def shuffle_tiles(self):
        random.shuffle(self.tiles)
        self.update_buttons()
        self.start_time = time.time()
        self.update_timer()

    def update_buttons(self):
        for i in range(self.size):
            for j in range(self.size):
                tile = self.tiles[i * self.size + j]
                text = str(tile) if tile != 0 else ""
                self.buttons[i][j].config(text=text)

    def move_tile(self, i, j):
        empty_index = self.tiles.index(0)
        empty_row, empty_col = divmod(empty_index, self.size)

        if abs(empty_row - i) + abs(empty_col - j) == 1:
            self.tiles[empty_row * self.size + empty_col], self.tiles[i * self.size + j] = self.tiles[
                i * self.size + j], self.tiles[empty_row * self.size + empty_col]
            self.moves += 1
            self.update_buttons()
            self.moves_label.config(text=f"Moves: {self.moves}")
            self.check_win()

    def update_timer(self):
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            self.root.after(1000, self.update_timer)

    def check_win(self):
        if self.tiles == list(range(self.size * self.size)):
            end_time = time.time()
            duration = int(end_time - self.start_time)
            messagebox.showinfo(f"You solved the puzzle in {self.moves} moves and {duration} seconds!")
            self.reset_game()

    def reset_game(self):
        self.moves = 0
        self.moves_label.config(text="Moves: 0")
        self.timer_label.config(text="Time: 0s")
        self.shuffle_tiles()
    def hamming(self):
        self.calculatehamming

    def manhattan(self):
        self.calculatemanhattan


if __name__ == "__main__":
   root = tk.Tk()
   game = SlidePuzzle(root)
   root.mainloop()