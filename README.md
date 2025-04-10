🁢 Domino Game – Python + Tkinter 🎮🧠

A classic Domino game built with Python and a simple GUI using Tkinter. Play against a smart AI opponent powered by the Minimax algorithm, which evaluates the best strategic moves to win the game!
✅ Features

    🧩 Automatically generates a full domino set (from [0|0] to [6|6]).

    👤 Single-player mode against AI.

    🧠 AI uses Minimax with a search depth of 3 to make smart decisions.

    🎨 Clean and user-friendly Tkinter interface.

    🕹️ Interactive gameplay: click to play, choose direction, draw from stock, or pass.

    🏁 Automatically detects win or draw conditions.

📁 Code Structure

    create_domino_set(): Initializes all valid domino tiles.

    evaluate_move() & play_tile(): Validates and plays moves.

    minimax(): Core AI logic.

    DominoGame class: Handles GUI and game flow.

🛠️ Requirements

    Python 3.x

    Tkinter (usually bundled with Python)

To run the game:

python gmax.py

🚀 Possible Improvements

    Add two-player (PvP) mode.

    Improve AI with Alpha-Beta Pruning for faster decision-making.

    Track and display player scores based on remaining tile values.

    Use tile images for a more polished look.

    Add alternative rule modes (e.g., Double-9 dominoes).


If you like the project, give it a ⭐ on GitHub!
Feel free to fork it and contribute new features. Happy coding! 🧠🎲
