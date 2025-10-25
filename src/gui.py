import tkinter as tk
from tkinter import messagebox
import random
import time
from datetime import datetime
from solver import Solver, flatten
from heuristics import Heuristics


class SlidePuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Heuristic Solve")

        self.size = 3
        self.initial_tiles = list(range(1, self.size * self.size)) + [0]
        self.tiles = list(self.initial_tiles)
        self.goalState = ((0, 1, 2), (3, 4, 5), (6, 7, 8))

        self.solver = Solver()
        self.heuristics_calc = Heuristics(self.goalState)

        self.moves = 0
        self.start_time = None
        self.is_solving = False
        self.current_heuristic = "None"

        self.solution_path = []
        self.current_step = 0
        self.animation_speed_ms = 300

        self.buttons = []
        self.create_widgets()
        self.shuffle_tiles()


    def create_widgets(self):

        grid_frame = tk.Frame(self.root, padx=10, pady=10)
        grid_frame.grid(row=0, column=0, rowspan=2, sticky='n')

        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.grid(row=2, column=0, sticky='ew')

        log_frame = tk.Frame(self.root, padx=10, pady=10)
        log_frame.grid(row=0, column=1, rowspan=3, sticky='nsew')

        # --- Puzzle Buttons ---
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = tk.Button(grid_frame, width=4, height=2, font=("Arial", 18, "bold"),
                                   command=lambda i=i, j=j: self.move_tile(i, j))
                button.grid(row=i, column=j, padx=2, pady=2)
                row.append(button)
            self.buttons.append(row)

        # --- Info Labels (placed below grid in the control_frame) ---

        # Row 0: Moves and Time
        self.moves_label = tk.Label(control_frame, text="Moves: 0", font=("Arial", 14))
        self.moves_label.grid(row=0, column=0, sticky='w', padx=5, pady=2)

        self.timer_label = tk.Label(control_frame, text="Search Time: N/A", font=("Arial", 14))
        self.timer_label.grid(row=0, column=1, sticky='e', padx=5, pady=2)

        # Row 1: Heuristics Display
        self.h_manhattan_label = tk.Label(control_frame, text="Manhattan H: 0", font=("Arial", 12))
        self.h_manhattan_label.grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.h_hamming_label = tk.Label(control_frame, text="Hamming H: 0", font=("Arial", 12))
        self.h_hamming_label.grid(row=1, column=1, sticky='e', padx=5, pady=2)

        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_columnconfigure(1, weight=1)

        # --- Benchmark Buttons ---
        tk.Label(control_frame, text="Run 100-Board Benchmark:", font=("Arial", 14)).grid(row=2, column=0, columnspan=2,
                                                                                          pady=(10, 5))

        bench_manhattan_button = tk.Button(control_frame, text="Benchmark All (Manhattan)",
                                           command=lambda: self.run_single_benchmark("manhattan"), font=("Arial", 12),
                                           bg='yellow')
        bench_manhattan_button.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        bench_hamming_button = tk.Button(control_frame, text="Benchmark All (Hamming)",
                                         command=lambda: self.run_single_benchmark("hamming"), font=("Arial", 12),
                                         bg='yellow')
        bench_hamming_button.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        # --- Solver Buttons ---
        tk.Label(control_frame, text="Solve Current Board:", font=("Arial", 14)).grid(row=4, column=0, columnspan=2,
                                                                                      pady=(10, 5))

        manhattan_button = tk.Button(control_frame, text="Manhattan",
                                     command=lambda: self.find_and_show_solution("manhattan"), font=("Arial", 12))
        manhattan_button.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

        hamming_button = tk.Button(control_frame, text="Hamming",
                                   command=lambda: self.find_and_show_solution("hamming"), font=("Arial", 12))
        hamming_button.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

        # --- Control Buttons ---
        reset_button = tk.Button(control_frame, text="New Game", command=self.reset_game, font=("Arial", 12))
        reset_button.grid(row=6, column=0, padx=5, pady=5, sticky='ew')

        quit_button = tk.Button(control_frame, text="Quit", command=self.root.quit, font=("Arial", 12), fg="red")
        quit_button.grid(row=6, column=1, padx=5, pady=5, sticky='ew')

        # --- Log Textbox ---
        log_label = tk.Label(log_frame, text="Activity Log", font=("Arial", 14, "bold"))
        log_label.pack(side=tk.TOP, pady=(0, 5))
        self.log_text = tk.Text(log_frame, height=20, width=80, state=tk.DISABLED, wrap=tk.WORD, font=("Consolas", 10))
        self.log_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.log_message("GUI initialized.")
        self.log_message(f"Goal State: {self.goalState}")

    def log_message(self, message, color="black"):
        timestamp = datetime.now().strftime("[%H:%M:%S]")

        self.log_text.config(state=tk.NORMAL)

        full_message = f"{timestamp} {message}\n"
        self.log_text.insert(tk.END, full_message)

        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    ## Game Logic
    # --------------------------------------------------------------------------------

    def shuffle_tiles(self):
        state_2d = self.solver.generateRandomSolvableBoard()
        self.tiles = flatten(state_2d)

        self.update_buttons()
        self.moves = 0
        self.moves_label.config(text="Moves: 0")

        self.start_time = None
        self.timer_label.config(text="Search Time: N/A")

        self.calculate_heuristics()
        self.log_message("New solvable board generated.")

    def move_tile(self, i, j):
        """
        Handles user clicks on a tile to move it into the blank space.
        """
        if self.is_solving:
            return

        current_index = i * self.size + j

        empty_index = self.tiles.index(0)
        empty_row, empty_col = divmod(empty_index, self.size)

        if abs(empty_row - i) + abs(empty_col - j) == 1:
            self.tiles[empty_index], self.tiles[current_index] = self.tiles[current_index], self.tiles[empty_index]
            self.moves += 1
            self.update_buttons()
            self.moves_label.config(text=f"Moves: {self.moves}")
            self.calculate_heuristics()
            self.check_win()

    def check_win(self):
        """Checks if the current state is the goal state."""
        goal_1d = flatten(self.goalState)
        if self.tiles == goal_1d:


            self.moves = 0
            self.moves_label.config(text="Moves: 0")

    def reset_game(self):
        """Resets the game state and shuffles a new board."""
        self.moves = 0
        self.moves_label.config(text="Moves: 0")

        self.start_time = None
        self.timer_label.config(text="Search Time: N/A")

        self.is_solving = False
        self.current_heuristic = "None"
        self.solution_path = []
        self.current_step = 0
        self.log_message("Game reset.")
        self.shuffle_tiles()

    ## Utility Functions
    # --------------------------------------------------------------------------------

    def update_buttons(self):
        """Updates the text and color of all buttons based on the current self.tiles state."""
        for i in range(self.size):
            for j in range(self.size):
                tile = self.tiles[i * self.size + j]
                text = str(tile) if tile != 0 else ""

                button = self.buttons[i][j]
                button.config(text=text, state=tk.NORMAL if not self.is_solving else tk.DISABLED)

                if tile == 0:
                    button.config(bg="lightgray", activebackground="lightgray")
                else:
                    button.config(bg="white", activebackground="lightblue")

    def calculate_heuristics(self):
        """Calculates and updates the displayed Manhattan and Hamming distances."""
        current_state_2d = self.get_current_state_2d()

        h_manhattan = self.heuristics_calc.manhattan(current_state_2d)
        h_hamming = self.heuristics_calc.hamming(current_state_2d)

        self.h_manhattan_label.config(text=f"Manhattan H: {h_manhattan}")
        self.h_hamming_label.config(text=f"Hamming H: {h_hamming}")

    def update_timer(self):
        """Updates the elapsed time display during the search."""
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"Search Time: {elapsed_time:.2f}s")

            if self.is_solving:
                self.root.after(100, self.update_timer)

    ## Solver Integration
    # --------------------------------------------------------------------------------

    def get_current_state_2d(self):
        """Converts the GUI's 1D list state to the 2D tuple-of-tuples format for the Solver."""
        state_2d = []
        for i in range(0, self.size * self.size, self.size):
            state_2d.append(tuple(self.tiles[i: i + self.size]))
        return tuple(state_2d)

    def set_current_state_from_2d(self, state_2d):
        """Converts a 2D tuple-of-tuples state to the GUI's 1D list state."""
        self.tiles = flatten(state_2d)

    def run_single_benchmark(self, heuristic):
        """
        Runs the full 100-board benchmark using the Solver and logs the results.
        """
        if self.is_solving:
            self.log_message("Benchmark is already running. Please wait.")
            return

        self.is_solving = True
        self.log_message(f"--- Starting 100-Board Benchmark for {heuristic.capitalize()} ---")
        self.update_buttons()  # Disable buttons

        self.is_solving = False

        try:
            results = self.solver.runBenchmark()

            if heuristic in results:
                res = results[heuristic]
                self.log_message(f"Benchmark finished successfully for {heuristic.capitalize()}.")
                self.log_message(f"Results for {heuristic.capitalize()} (100 boards):")
                self.log_message(f"  Avg Runtime: {res['mean_runtime']:.4f} s (Stdev: {res['standard_runtime']:.4f})")
                self.log_message(f"  Avg Nodes: {res['mean_nodes']:.2f} (Stdev: {res['standard_nodes']:.2f})")
            else:
                self.log_message(f"Benchmark failed to find results for {heuristic.capitalize()}.")

        except Exception as e:
            self.log_message(f"Benchmark failed: {e}")
            messagebox.showerror("Benchmark Error", f"Benchmark execution failed: {e}")

        self.is_solving = False
        self.update_buttons()
        self.log_message("--- Benchmark Complete ---")

    def find_and_show_solution(self, heuristic):
        """
        Calculates the solution path using the specified heuristic and starts the animation.
        """
        if self.is_solving:
            self.log_message("Solver is already running. Please wait or reset.")
            return

        self.is_solving = True
        self.log_message(f"Starting A* search with {heuristic.capitalize()} heuristic...")
        self.update_buttons()  # Disable buttons

        start_state = self.get_current_state_2d()

        if start_state == self.goalState:
            self.log_message("Board is already solved. Aborting search.")
            self.is_solving = False
            self.update_buttons()
            return

        # Start the Search Timer
        self.start_time = time.time()
        self.update_timer()

        self.current_heuristic = heuristic

        # Run the A* search
        try:
            path, nodes_expanded = self.solver.solve(start_state, self.goalState, heuristic)
        except Exception as e:
            self.log_message(f"Solver FAILED: {e}")
            messagebox.showerror("Fatal Error", f"Solver failed: {e}")
            path = None

        solve_time = time.time() - self.start_time

        # Stop the Search Timer
        self.start_time = None
        self.timer_label.config(text=f"Search Time: {solve_time:.4f}s")

        self.is_solving = False

        if path is not None:
            self.solution_path = path
            self.current_step = 0

            moves = len(path) - 1

            self.log_message(f"Search FINISHED in {solve_time:.4f}s.")
            self.log_message(f"Path Length: {moves} moves. Nodes Expanded: {nodes_expanded}.")
            self.log_message(f"Starting solution animation in {self.animation_speed_ms}ms steps.")

            # Start the animation
            self.is_solving = True
            self.animate_solution()
        else:
            self.log_message("Could not find a solution (Unsolvable board? Should not happen with current logic).")
            self.is_solving = False
            self.update_buttons()

    def animate_solution(self):
        """
        Displays the solution path on the board one step at a time.
        """
        if not self.solution_path:
            self.log_message("Animation stopped (no path).")
            self.is_solving = False
            self.update_buttons()
            return

        if self.current_step < len(self.solution_path):
            state_2d = self.solution_path[self.current_step]
            self.set_current_state_from_2d(state_2d)
            self.update_buttons()

            # Update the move count for the animation
            self.moves_label.config(text=f"Moves: {self.current_step}")
            self.calculate_heuristics()

            self.log_text.config(state=tk.NORMAL)
            # Find and delete the last animation step log line, if it exists
            if self.log_text.tag_ranges("temp_animation_step"):
                self.log_text.delete("temp_animation_step.first", "temp_animation_step.last")

            # Insert the new step and tag it for future deletion
            full_message = f"Animating step {self.current_step}/{len(self.solution_path) - 1}"
            self.log_message(full_message)

            # Apply a temporary tag to the last inserted line to allow quick deletion in the next step
            start_index = f"{self.log_text.index(tk.END)}-2l"
            end_index = f"{self.log_text.index(tk.END)}-1c"
            self.log_text.tag_add("temp_animation_step", start_index, end_index)
            self.log_text.config(state=tk.DISABLED)

            self.current_step += 1
            # Schedule the next step
            self.root.after(self.animation_speed_ms, self.animate_solution)
        else:
            # Animation finished

            algo_name = self.current_heuristic.capitalize()
            self.log_message(f"*** Puzzle SOLVED by {algo_name}! ***")

            self.is_solving = False
            self.update_buttons()
            self.check_win()


if __name__ == "__main__":
    root = tk.Tk()
    game = SlidePuzzleGUI(root)
    root.mainloop()