import numpy as np
from Grid import Grid
from ComputerAI import ComputerAI
from Displayer import Displayer
from PlayerAI import PlayerAI
from test_players.EasyAI import EasyAI
from test_players.MediumAI import MediumAI
from test_players.HardAI import HardAI
from Utils import *
import time

PLAYER_TURN, COMPUTER_TURN = 1,2

# Time Limit Before Losing
timeLimit = 5.0
allowance = 1.0

class Game():
    def __init__(self, playerAI = None, computerAI = None, N = 7, displayer = None):
        '''
        Description
        ----------
        Construct new game given two players, board size and displayer.

        Parameters
        ----------
        playerAI   - Human player AI, of type PlayerAI. default = None 

        computerAI - Human or Computer Opponent. default = None
        
        N  - dimension of grid.

        '''
        self.grid       = Grid(N)
        self.playerAI   = playerAI or ComputerAI() 
        self.computerAI = computerAI or ComputerAI() 
        self.dim        = N
        self.over       = False
        self.displayer = displayer

    def initialize_game(self):

        p1_index, p2_index = (0, self.dim // 2), (self.dim - 1, self.dim // 2)
        
        self.grid.setCellValue(p1_index, 1)
        self.playerAI.setPosition(p1_index)
        self.playerAI.setPlayerNum(1)

        self.grid.setCellValue(p2_index, 2)
        self.computerAI.setPosition(p2_index)
        self.computerAI.setPlayerNum(2)
        

    def is_over(self, turn):
        # whomever's turn it is:
        other_player = self.grid.find(3 - turn)

        # other player has no available moves
        if len(self.grid.get_neighbors(other_player, only_available=True)) == 0:
            return turn

        else:
            return False

    def is_valid_move(self, grid : Grid, player, move : tuple):
        '''Validate move - cell has to be available and immediate neighbor'''
        
        if grid.getCellValue(move) == 0 and move in grid.get_neighbors(player.getPosition()):
            return True
        
        return False

    def is_valid_trap(self, grid : Grid, trap : tuple):
        '''Validate trap - cell can't be a player'''

        if grid.getCellValue(trap) > 0:
            return False

        return True

    def throw(self, player, grid : Grid, intended_position : tuple) -> tuple:
        '''
        Description
        ----------
        Function returns the coordinates in which the trap lands, given an intended location.

        Parameters
        ----------

        player : the player throwing the trap

        grid : current game Grid

        intended position : the (x,y) coordinates to which the player intends to throw the trap to.

        Returns
        -------
        Position (x_0,y_0) in which the trap landed : tuple

        '''
 
        # find neighboring cells
        neighbors = grid.get_neighbors(intended_position)

        neighbors = [neighbor for neighbor in neighbors if grid.getCellValue(neighbor) <= 0]
        n = len(neighbors)
        
        probs = np.ones(1 + n)
        
        # compute probability of success, p
        p = 1 - 0.05*(manhattan_distance(player.getPosition(), intended_position) - 1)

        probs[0] = p

        probs[1:] = np.ones(len(neighbors)) * ((1-p)/n)

        # add desired coordinates to neighbors
        neighbors.insert(0, intended_position)
        
        # return 
        result = np.random.choice(np.arange(n + 1), p = probs)
        
        return neighbors[result]

    def updateAlarm(self, currTime):
        if currTime - self.prevTime > timeLimit + allowance:
            self.over = True
            print("Went over time. Doll Shot!")
        else:
            # while time.process_time() - self.prevTime < timeLimit + allowance:
            #    pass

            self.prevTime = time.process_time()

    def play(self):
        """ DO NOT MODIFY """

        self.initialize_game()

        self.displayer.display(self.grid)

        turn = PLAYER_TURN
        
        while not self.over:
            self.prevTime = time.process_time()
            grid_copy = self.grid.clone()

            move = None
            
            if turn == 1:

                print("Player 1's Turn: ")

                # find best move; should return two coordinates - new position and bombed tile.
                move = self.playerAI.getMove(grid_copy)

                # if move is valid, perform it
                if self.is_valid_move(self.grid, self.playerAI, move):
                    self.grid.move(move, turn)
                    self.playerAI.setPosition(move)
                    print(f"Moving to {move}")
                    won = self.is_over(turn)
                    if won:
                        self.is_over = True
                        self.displayer.display(self.grid)
                        return won
                else:
                    self.over = True
                    print(f"Tried to move to : {move}")
                    print("invalid Player 1 Move!")
                    
                intended_trap = self.playerAI.getTrap(self.grid.clone())

                if self.is_valid_trap(self.grid, intended_trap):
                    trap = self.throw(self.playerAI, self.grid, intended_trap)
                    self.grid.trap(trap)
                    print(f"Throwing a trap to: {intended_trap}. Trap landed in {trap}")
                    won = self.is_over(turn)
                    if won:
                        self.displayer.display(self.grid)
                        return won

                else: 
                    self.over = True
                    print(f"Tried to put trap in {intended_trap}")
                    print("Invalid trap!")

            else:

                print("Player 2's Turn : ")
                
                # make move
                move = self.computerAI.getMove(grid_copy)

                # check if move is valid; perform if it is.
                if self.is_valid_move(self.grid, self.computerAI, move):
                    self.grid.move(move, turn)
                    self.computerAI.setPosition(move)
                    print(f"Moving to {move}")
                    won = self.is_over(turn)
                    if won:
                        self.is_over = True
                        self.displayer.display(self.grid)
                        return won

                else:
                    self.over = True
                    print("invalid Player 2 Move")
                    print(move)
                    return 3 - turn

                intended_trap = self.computerAI.getTrap(self.grid.clone())

                if self.is_valid_trap(self.grid, intended_trap):
                    trap = self.throw(self.computerAI, self.grid, intended_trap)
                    self.grid.trap(trap)
                    print(f"Throwing a trap to: {intended_trap}. Trap landed in {trap}")
                    won = self.is_over(turn)
                    if won:
                        self.is_over = True
                        self.displayer.display(self.grid)
                        return won
                else: 
                    self.over = True
                    print(f"Tried to put trap in {intended_trap}")
                    print("Invalid trap!")

            endtime = time.process_time()
            turn = 3 - turn
            self.displayer.display(self.grid)
            self.updateAlarm(endtime)

def main():

    playerAI = HardAI() # change this to PlayerAI() to test your player!
    computerAI = EasyAI() # change this to a more sophisticated player you've codeds
    displayer = Displayer()
    game = Game(playerAI = playerAI, computerAI = computerAI, N = 7, displayer=displayer)
    
    result = game.play()
    if result == 1: 
        print("Player 1 wins!")
    elif result == 2:
        print("Player 2 wins!")

if __name__ == "__main__":
    main()
