from states.wumpus import WumpusGame, StartGame

if __name__ == "__main__":

    start_game = StartGame()
    if start_game.run():
        game = WumpusGame()
        game.main_loop()
