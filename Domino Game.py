import random
import tkinter as tk
from tkinter import messagebox

# Create the domino set
def create_domino_set():
    return [(i, j) for i in range(7) for j in range(i, 7)]

# Distribute the tiles
def draw_tiles(tiles, num):
    drawn = tiles[:num]
    del tiles[:num]
    return drawn

# Evaluate move (for AI)
def evaluate_move(board, tile, position):
    if not board:
        return True
    if position == "left" and (tile[1] == board[0][0] or tile[0] == board[0][0]):
        return True
    if position == "right" and (tile[0] == board[-1][1] or tile[1] == board[-1][1]):
        return True
    return False

def play_tile(board, tiles, tile, position):
    if position == "left":
        board.insert(0, tile if tile[1] == board[0][0] else tile[::-1])
    else:
        board.append(tile if tile[0] == board[-1][1] else tile[::-1])
    tiles.remove(tile)

# Minimax algorithm
def minimax(board, ai_tiles, player_tiles, stock, depth, is_ai_turn):
    if depth == 0 or not ai_tiles or not player_tiles:
        return evaluate_board_state(board, ai_tiles, player_tiles)

    if is_ai_turn:
        max_eval = float("-inf")
        for tile in ai_tiles:
            for direction in ["left", "right"]:
                if evaluate_move(board, tile, direction):
                    new_board = board[:]
                    new_ai_tiles = ai_tiles[:]
                    play_tile(new_board, new_ai_tiles, tile, direction)
                    eval = minimax(new_board, new_ai_tiles, player_tiles, stock, depth - 1, False)
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for tile in player_tiles:
            for direction in ["left", "right"]:
                if evaluate_move(board, tile, direction):
                    new_board = board[:]
                    new_player_tiles = player_tiles[:]
                    play_tile(new_board, new_player_tiles, tile, direction)
                    eval = minimax(new_board, ai_tiles, new_player_tiles, stock, depth - 1, True)
                    min_eval = min(min_eval, eval)
        return min_eval

def evaluate_board_state(board, ai_tiles, player_tiles):
    return len(player_tiles) - len(ai_tiles)

# AI logic to determine the optimal move
def ai_play(board, ai_tiles, player_tiles, stock, depth=3):
    best_score = float("-inf")
    best_move = None
    for tile in ai_tiles:
        for direction in ["left", "right"]:
            if evaluate_move(board, tile, direction):
                new_board = board[:]
                new_ai_tiles = ai_tiles[:]
                play_tile(new_board, new_ai_tiles, tile, direction)
                score = minimax(new_board, new_ai_tiles, player_tiles, stock, depth - 1, False)
                if score > best_score:
                    best_score = score
                    best_move = (tile, direction)
    return best_move

class DominoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Domino Game")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        # Game setup
        self.domino_set = create_domino_set()
        random.shuffle(self.domino_set)
        self.player_tiles = draw_tiles(self.domino_set, 7)
        self.ai_tiles = draw_tiles(self.domino_set, 7)
        self.stock = self.domino_set
        self.board = []
        self.game_over = False

        # User Interface
        self.setup_ui()

    def setup_ui(self):
        self.opponent_frame = tk.Frame(self.root, bg="#ffcccb", height=100, relief=tk.SUNKEN, bd=2)
        self.opponent_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.board_frame = tk.Frame(self.main_frame, bg="#d0e6f5", width=1500, height=400, relief=tk.RAISED, bd=2)
        self.board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)
        self.board_frame.pack_propagate(False)

        self.stock_frame = tk.Frame(self.main_frame, bg="#e0e0e0", width=300, relief=tk.RAISED, bd=2)
        self.stock_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.player_frame = tk.Frame(self.root, bg="#fdfd96", height=150, relief=tk.SUNKEN, bd=2)
        self.player_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.controls_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.controls_frame.pack(side=tk.BOTTOM, pady=10)

        self.draw_button = tk.Button(self.controls_frame, text="Draw from Stock", command=self.draw_from_stock,
                                      state=tk.DISABLED, font=("Arial", 14), bg="lightgray", relief=tk.RAISED)
        self.draw_button.pack(side=tk.LEFT, padx=10)

        self.pass_button = tk.Button(self.controls_frame, text="Pass", command=self.pass_turn,
                                      state=tk.DISABLED, font=("Arial", 14), bg="lightgray", relief=tk.RAISED)
        self.pass_button.pack(side=tk.LEFT, padx=10)

        self.update_ui()

    def update_ui(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        tk.Label(self.board_frame, text="Board:", font=("Arial", 16, "bold"), bg="#d0e6f5").pack(anchor="nw", padx=10)
        if self.board:
            for idx, tile in enumerate(self.board):
                tile_label = tk.Label(self.board_frame, text=f"[{tile[0]}|{tile[1]}]", font=("Arial", 16), bg="#d0e6f5", relief=tk.SOLID, bd=1)
                tile_label.place(x=50 + idx * 60, y=150, anchor="center")
        else:
            tk.Label(self.board_frame, text="Empty", font=("Arial", 16), bg="#d0e6f5").pack(anchor="nw", padx=10)

        for widget in self.opponent_frame.winfo_children():
            widget.destroy()
        tk.Label(self.opponent_frame, text="Opponent's Tiles:", font=("Arial", 16, "bold"), bg="#ffcccb").pack(side=tk.LEFT)
        for _ in self.ai_tiles:
            btn = tk.Button(self.opponent_frame, text="", font=("Arial", 14), bg="#ff9999", relief=tk.RAISED, width=3, height=1)
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        for widget in self.player_frame.winfo_children():
            widget.destroy()
        tk.Label(self.player_frame, text="Your Tiles:", font=("Arial", 16, "bold"), bg="#fdfd96").pack(side=tk.LEFT)
        for idx, tile in enumerate(self.player_tiles):
            btn = tk.Button(self.player_frame, text=f"[{tile[0]}|{tile[1]}]", font=("Arial", 14),
                            command=lambda i=idx: self.play_tile(i), bg="#d1e7dd", relief=tk.RAISED)
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        for widget in self.stock_frame.winfo_children():
            widget.destroy()
        tk.Label(self.stock_frame, text="Stock:", font=("Arial", 16, "bold"), bg="#e0e0e0").pack()
        for _ in self.stock:
            btn = tk.Button(self.stock_frame, text=" ", font=("Arial", 14), bg="#c0c0c0", relief=tk.RAISED)
            btn.pack(pady=2)

        self.draw_button["state"] = tk.NORMAL if not self.has_valid_move(self.player_tiles) and self.stock else tk.DISABLED
        self.pass_button["state"] = tk.NORMAL if not self.has_valid_move(self.player_tiles) and not self.stock else tk.DISABLED

    def play_tile(self, idx):
        tile = self.player_tiles[idx]
        if self.board:
            if evaluate_move(self.board, tile, "left") and evaluate_move(self.board, tile, "right"):
                direction = self.ask_direction(tile)
            elif evaluate_move(self.board, tile, "left"):
                direction = "left"
            elif evaluate_move(self.board, tile, "right"):
                direction = "right"
            else:
                messagebox.showinfo("Invalid Move", "You cannot play this tile.")
                return

            if direction == "left":
                self.board.insert(0, tile if tile[1] == self.board[0][0] else tile[::-1])
            else:
                self.board.append(tile if tile[0] == self.board[-1][1] else tile[::-1])

            self.player_tiles.pop(idx)
            self.update_ui()
            self.check_winner()
            self.ai_turn()
        else:
            self.board.append(tile)
            self.player_tiles.pop(idx)
            self.update_ui()
            self.check_winner()
            self.ai_turn()

    def ask_direction(self, tile):
        direction = tk.StringVar()
        direction.set("left")
        popup = tk.Toplevel(self.root)
        popup.title("Choose Direction")
        tk.Label(popup, text=f"Where to play [{tile[0]}|{tile[1]}]?").pack(pady=10)
        tk.Button(popup, text="Left", command=lambda: [direction.set("left"), popup.destroy()]).pack(side=tk.LEFT, padx=20)
        tk.Button(popup, text="Right", command=lambda: [direction.set("right"), popup.destroy()]).pack(side=tk.RIGHT, padx=20)
        popup.grab_set()
        self.root.wait_window(popup)
        return direction.get()

    def ai_turn(self):
        if self.has_valid_move(self.ai_tiles):
            move = ai_play(self.board, self.ai_tiles, self.player_tiles, self.stock)
            if move:
                tile, direction = move
                play_tile(self.board, self.ai_tiles, tile, direction)
                self.update_ui()
                self.check_winner()
        elif self.stock:
            self.ai_tiles.append(self.stock.pop(0))
            self.ai_turn()
        elif not self.has_valid_move(self.player_tiles):
            self.end_game("No moves left for either player. Game ends in a draw!")

    def draw_from_stock(self):
        if self.stock:
            self.player_tiles.append(self.stock.pop(0))
            self.update_ui()

    def pass_turn(self):
        if not self.has_valid_move(self.player_tiles) and not self.stock:
            self.end_game("No moves left for either player. Game ends in a draw!")
        else:
            messagebox.showinfo("Pass", "You passed your turn.")
            self.ai_turn()

    def has_valid_move(self, tiles):
        for tile in tiles:
            if evaluate_move(self.board, tile, "left") or evaluate_move(self.board, tile, "right"):
                return True
        return False

    def check_winner(self):
        if not self.game_over:
            if not self.player_tiles:
                self.game_over = True
                self.end_game("You Win!")
            elif not self.ai_tiles:
                self.game_over = True
                self.end_game("AI Wins!")

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = DominoGame(root)
    root.mainloop()
