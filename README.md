# Connect 4 PyGame with Minimax AI
This application serves as a simple implementation of the minimax algorithm with alpha-beta pruning in a connect 4 style game. 
https://en.wikipedia.org/wiki/Minimax
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

Hand calculation example of minimax with alpha-beta pruning:
https://www.youtube.com/watch?v=zp3VMe0Jpf8

# Instructions
The game can be run through the connect4.py script file or the connect4.exe. 
2-player mode will create a mode where you can alternate turns between two users.
1-player mode will prompt you to select a difficulty level for facing the minimax AI. 

# Parameters
Experiment with different parameters to adjust the difficulty and behavior of the AI.

## Depth 
In 1-player mode, your opponent will be player 2, whose moves are determined by an AI using the minimax algorithm. The difficulty level is determined by setting the depth of the minimax AI with a random factor included for playability. The depth can be a random choice from the corresponding arrays:
|Difficulty| Depth array |
|--|--|
|Easy| [1, 1, 1, 2] |
|Medium| [1, 2, 2, 3, 3]|
|Hard| [5, 6]|

## Heuristic evaluation function
The decison_score and space_score  function serves as the scoring scheme to score each game state with the minimax game tree. The function adds a max score of 1000 for a winning condition. Each open sequence of 3 pieces adds 5 points and  sequences of 2 are worth 2 points. For each of the opponents open sequences of the 3 pieces, 4 points are subtracted to incentive the AI to block your sequences of 3 pieces. Finally, pieces placed in the center column add 2 points to the score as center pieces create more opportunities for sequences. This causes the AI to favor placing pieces in the center column, especially in the opening of the game.
