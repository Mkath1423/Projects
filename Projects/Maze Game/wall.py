import pygame

class Wall():
    '''
    Wall
    
    A wall object that acts as an impassible barrier for the player
    
    FUNCTIONS
        __init__(self, rectangleIn, colorIn)
            Creates the wall object with initial values for its position, size, and color
            
        draw(self, surfaceIn)
            Draws the wall as a rectangle on a surface
        
        isColliding(self, playerPos, playerSize)
            Returns true if the player is colliding with the wall
        
    '''
    def __init__(self, rectangleIn, colorIn):
        '''
        Initializes a Wall Object

        Object contains values for the position, the size, and the color of the wall

        Parameters
        ----------
        rectangleIn: pygame.Rect() or [left, top, width, height]
            The rectangle object that represents the top-left position of the
            wall and its dimenstions. 

        colorIn: pygame.Color() or (r, g, b)
            The color of the rectangle that represents the wall

        Returns
        -------
        None
        '''
        self.rectangle = rectangleIn
        self.color = colorIn
        
    def draw(self, surfaceIn):
        '''
        Draws the Wall Object

        Draws the Wall as a rectangle with the specified color, size, and position on a given surface.

        Parameters
        ----------
        surfaceIn: pygame.Surface()
            The surface that the wall will be drawn onto
            
        Returns
        -------
        None
        '''
        pygame.draw.rect(surfaceIn, self.color, self.rectangle)
        
    def isColliding(self, playerPos, playerSize):
        '''
        Determine if the player is colliding with the wall

        Using the position and dimenstions of the wall and player
        determine if they are colliding.

        Parameters
        ----------
        playerPos: List<int>
            The position of the player on the surface
            
        playerSize: int
            The radius of the circle that represents the player
            
        Returns
        -------
        bool
            True if the player is colliding with the wall otherwise False
            
        List<int>
            The new position of the player.
            If the player is colliding with a wall, the position will be adjusted
                otherwise it will remain the same.
        '''
        snappedPlayerPos = playerPos.copy()
        # The highest and lowest y values of the player's circle
        playerTop    = playerPos[1] - playerSize
        playerBottom = playerPos[1] + playerSize
        
        # The highest and lowest y values of the wall's rectangle
        wallTop = self.rectangle[1]
        wallBottom = self.rectangle[1] + self.rectangle[3]
        
        # The highest and lowest x values of the player's circle
        playerLeft   = playerPos[0] - playerSize
        playerRight  = playerPos[0] + playerSize
        
        # The highest and lowest x values of the wall's rectangle
        wallLeft = self.rectangle[0]
        wallRight = self.rectangle[0] + self.rectangle[2]
        
        conditionsMet = 0
        # if the player is to the left of the left side of the wall
        if(playerPos[0] < wallLeft):
            # if the player's right side is colliding with the wall
            if playerRight > wallLeft:
                conditionsMet += 1
                # snap the player to the left edge of the wall
                snappedPlayerPos[0] = wallLeft - playerSize - 1
        
        # if the player is to the right of the right side of the wall
        elif(playerPos[0] > wallRight):
            # if the player's left side is colliding with the wall
            if playerLeft < wallRight:
                conditionsMet += 1
                # snap the player to the right edge of the wall
                snappedPlayerPos[0] = wallRight + playerSize + 1
                
        # if the player is between the left and right edges
        else:
            conditionsMet += 1
        
        # if the player is above the top side of the wall
        if(playerPos[1] < wallTop):
            # if the player's bottom side is colliding with the wall
            if playerBottom > wallTop:
                conditionsMet += 1
                # snap the player to the top edge of the wall
                snappedPlayerPos[1] = wallTop - playerSize - 1
    
        # if the player is below the bottom side of the wall
        elif(playerPos[1] > wallBottom):
            # if the player's top side is colliding with the wall
            if playerTop < wallBottom:
                conditionsMet += 1
                # snap the player to the bottom edge of the wall
                snappedPlayerPos[1] = wallBottom + playerSize + 1
                
        # if the player is between the top and bottom edges     
        else:
            conditionsMet += 1
        
        # if the player is colliding with the wall
        if(conditionsMet == 2): 
            return (True, snappedPlayerPos)
        else:
            return (False, playerPos)