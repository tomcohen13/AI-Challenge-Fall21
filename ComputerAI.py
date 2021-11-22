import random
from BaseAI import BaseAI
import numpy as np
from Grid import Grid

class ComputerAI(BaseAI):

    def __init__(self, initial_position = None) -> None:
        super().__init__()
        self.pos = initial_position

    def setPosition(self, new_pos: tuple):
        self.pos = new_pos
    
    def getPosition(self):
        return self.pos 

    def getMove(self, grid):
        """ Returns a random, valid move """
        
        # find all available moves 
        available_moves = grid.get_neighbors(self.pos, only_available = True)

        # make random move
        new_pos = random.choice(available_moves) if available_moves else None
        
        self.setPosition(new_pos)

        return new_pos

    def getTrap(self, grid : Grid):
        
        # find all available cells in the grid
        available_cells = grid.getAvailableCells()

        # find all available cells
        trap = random.choice(available_cells) if available_cells else None

        return self.throw(grid, trap)

    def throw(self, grid : Grid, intended_position : tuple) :
        '''
        Description
        ----------
        Function returns the coordinates in which the trap lands, given an intended location.

        Parameters
        ----------

        grid : current game Grid

        intended position : the (x,y) coordinates to which the player intends to throw the trap to.
        '''
        # find neighboring cells
        neighbors = grid.get_neighbors(intended_position)

        n = len(neighbors)
        
        probs = np.ones(1 + n)
        
        # compute probability of success, p
        p = 1 - 0.05*(manhattan_distance(self.pos, intended_position) - 1)

        probs[0] = p

        probs[1:] = np.ones(len(neighbors)) * ((1-p)/n)

        return np.random.choice(np.concatenate(([intended_position], neighbors)), p = probs)


def manhattan_distance(position, target):
    return np.abs(target[0] - position[0]) + np.abs(target[1] - position[1])


