import random

class Cell():
    '''
    Cell
    
    Information storage for the walls of each cell in the maze.
    
    FUNCTIONS
        __init__(self)
            Creates a new cell object with default values for each of the four possible walls
    '''
    def __init__(self):
        '''
        Initializes a cell Object

        Object contains a boolean for each wall to determine if the wall should be drawn
        and it contains a boolean for whether or not it has been checked by the algorithm

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.walls = {
            
            -1:True,# Top
           
            1:True, # Bottom
            
            2:True, # Right
            
            -2:True # Left         
            }
        
        
        self.checked = False

class MazeGenerator():
    '''
    MazeGenerator
    
    An object that can store and generate new random mazes
    
    FUNCTIONS
        __init__(self, mazeSizeIn)
            Creates a new MazeGenerator with an initial value
            
        updateCell(self, cellPos, wallsIn, checkedIn)
            Updates the values stored in a cell object
        
        generateMaze(self)
            Generates a new random maze using recursive backtracking
    '''
    def __init__(self, mazeSizeIn):
        '''
        Initializes a MazeGenerator Object

        Object contains an integer list for the size of the maze and
        a 2d array containing the Cell Objects that will make up the maze

        Parameters
        ----------
        mazeSizeIn : List<int>
          A 2 element list for the x and y size of the maze.
          [x, y]

        Returns
        -------
        None
        '''
        
        self.mazeSize = mazeSizeIn
        
        
    def updateCell(self, cellPos, wallsIn, checkedIn):
        '''
        Changes the values of a Cell Object in the maze.

        Gets a Cell Object from the maze array and changes its
        walls values and its checked value.

        Parameters
        ----------
        cellPos : List<int>
          A 2 element list for the x and y position of the Cell in the maze.
          [x, y]

        Returns
        -------
        None

        Raises
        -------
        IndexError
          If the mazeSize has less than 2 elements an Index error will be raised
        '''
        # Update the cell at position [x, y] with the new values
        self.maze[cellPos[0]][cellPos[1]].walls = wallsIn
        self.maze[cellPos[0]][cellPos[1]].checked = checkedIn
    
    def generateMaze(self):
        '''
        Generates a maze using a recursive backtracking algorithm.

        Creates paths to each Cell in the maze using a recursive backtracking algorithm
        and updates the Cells walls values to reflect the paths in the maze.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        # Create a new maze of default cells
        self.maze = [[Cell() for i in range(self.mazeSize[0])] for j in range(self.mazeSize[1])]
        
        # Cells that have been reached by the algorithm and still have unchecked neighbors. 
        cellsStack = []
        
        # Starting square for the algorithm
        cellsStack.append([0, 0])
        
        # While there are still uncheck cells to path to
        while(len(cellsStack) > 0):
            
            # look at the last cell in the stack
            # set its checked value to true
            cellPos = cellsStack[-1]
            self.maze[cellPos[1]][cellPos[0]].checked = True
            
            # FIND NEIGHBOURING CELLS
            # All neighbouring cells that have not been reached
            neighbourCells = {}
            
            # LEFT NEIGHBOUR
            # If there is a left neighbour
            if(cellPos[0] - 1 >= 0):
                # if the left neighbour has not been reached 
                if(self.maze[cellPos[1]][cellPos[0] - 1].checked == False):
                    # Add this neighbour to the neighbourCells dictionary
                    neighbourCells[-2] = [cellPos[0] - 1, cellPos[1]]
                    
            # RIGHT NEIGHBOUR
            # If there is a right neighbour
            if(cellPos[0] + 1 < self.mazeSize[0]):
                # if the right neighbour has not been reached
                if(self.maze[cellPos[1]][cellPos[0] + 1].checked == False):
                    # Add this neighbour to the neighbourCells dictionary
                    neighbourCells[2] = [cellPos[0] + 1, cellPos[1]]
            
            # TOP NEIGHBOUR
            # If there is a top neighbour
            if(cellPos[1] - 1 >= 0): 
                # if the top neighbour has not been reached
                if(self.maze[cellPos[1] - 1][cellPos[0]].checked == False):
                    # Add this neighbour to the neighbourCells dictionary
                    neighbourCells[-1] = [cellPos[0], cellPos[1] - 1]
                    
            # BOTTOM NEIGHBOUR
            # If there is a bottom neighbour
            if(cellPos[1] + 1 < self.mazeSize[1]):
                # if the bottom neighbour has not been reached
                if(self.maze[cellPos[1] + 1][cellPos[0]].checked == False):
                    # Add this neighbour to the neighbourCells dictionary
                    neighbourCells[1] = [cellPos[0], cellPos[1] + 1]
            
            # CONTINUE THE PATH
            # if there are any neighbours
            if(len(neighbourCells) > 0):
                # choose a random neighbour
                # ('direction', Cell position)
                nextCell = random.choice(list(neighbourCells.items()))
                
                # remove the walls of the current cell and the next cell
                #  so that they connect to one another
                self.maze[cellPos[1]][cellPos[0]].walls[nextCell[0]] = False
                self.maze[nextCell[1][1]][nextCell[1][0]].walls[nextCell[0] * -1] = False
                
                # add the next cell to the end of the stack
                cellsStack.append([nextCell[1][0], nextCell[1][1]])
            
            # if there are no neighbours
            else:
                # remove this cell from the stack
                cellsStack.pop()