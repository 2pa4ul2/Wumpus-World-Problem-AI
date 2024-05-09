# Wumpus World Game AI

## Overview
The Wumpus World Game is a Python implementation of the classic Wumpus World environment, where the agent navigates a grid-based world filled with dangers and treasures.

## Features
- Grid-based environment.
- Random generation of game elements: gold, pits, and Wumpus.
- Character movement with perception of nearby dangers.
- Shooting mechanism to eliminate the Wumpus.
- Scoring system based on collected gold and actions taken.
- Graphical User Interface (GUI) using Pygame library.

## Rules of the Game

1. **Objective**: Collect all the gold and return to the starting position without falling into pits or being eaten by the Wumpus.

2. **Grid Environment**: Explore a grid-based world where each cell may contain gold, pits, walls, or the Wumpus.

3. **Elements**:
   - **Gold**: Collect gold scattered throughout the grid.
   - **Pits**: Beware of hidden pits; falling into one results in game over.
   - **Wumpus**: The menacing creature can be eliminated with arrows; otherwise, moving adjacent to it results in game over.
   - **Arrows**: Limited arrows can be used to shoot and eliminate the Wumpus.

4. **Perceptions**: 
   - Feel a breeze if a pit is adjacent.
   - Detect the stench of the Wumpus if it's nearby.

5. **Scoring**:
   - Earn points for collecting gold.
   - Bonus points for eliminating the Wumpus.
   - Point deductions for falling into pits and movements.

6. **Winning and Losing**:
   - **Win**: Collect all the gold and safely return to the starting position.
   - **Lose**: Fall into a pit, encounter the Wumpus without eliminating it, or run out of arrows.


## Installation and Usage
1. Clone the repository to your local machine:
   
    ``` bash
    https://github.com/2pa4ul2/Wumpus-World-Problem-AI.git
    ```
3. Install the required dependencies:
   
    ``` bash
    pip install pygame
    ```
5. Run the game:
   
    ``` bash
    python main.py
    ```
## Screenshots
### Start Page

![image](https://github.com/2pa4ul2/Wumpus-World-Problem-AI/assets/95076322/c67741ca-6d7d-4e54-950c-35dcf9275e1b)

### Game Page

![image](https://github.com/2pa4ul2/Wumpus-World-Problem-AI/assets/95076322/340b1eaa-122a-40b4-84c7-83e1191fb749)

![image](https://github.com/2pa4ul2/Wumpus-World-Problem-AI/assets/95076322/4dde6cb1-70d0-4050-890e-57b91f2766ef)

