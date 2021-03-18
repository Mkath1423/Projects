import pygame

class Flag():
    '''
    Flag
    
    The end goal of the player
    
    FUNCTIONS
        __init__(self, posIn, sizeIn, colorIn)
            Creates the flag object with position, size, and color values.
        
        draw(self, surfaceIn)
            Draws the flag as a circle on a surface
            
        isColliding(self, playerPos, playerSize)
            Returns true if the player is colliding with the flag
        
    '''
    
    def __init__(self, posIn, sizeIn, colorIn):
        '''
        Initializes a Flag Object

        Object contains a value for the position, the size, and the color of the flag

        Parameters
        ----------
        posIn: list<float>
            The x-y position of the flag on the mainSurface

        sizeIn: int
            The size of the circle that represents the flag

        colorIn: pygame.Color() or (r, b, g)
            The color of the circle that represents the flag

        Returns
        -------
        None
        '''
        self.pos = posIn
        self.size = sizeIn
        self.color = colorIn
        
    def draw(self, surfaceIn):
        '''
        Draws the flag Object

        Draws the flag as a circle with the specified color, size, and position on a given surface.

        Parameters
        ----------
        surfaceIn: pygame.Surface()
            The surface that the flag will be drawn onto
            
        Returns
        -------
        None
        '''
        pygame.draw.circle(surfaceIn, self.color, self.pos, self.size)

    def isColliding(self, playerPos, playerSize):
        '''
        Determine if the player is colliding with the flag

        Using Pythagoras's theorem and the radii of the flag and the player
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
            True if the player is colliding with the flag otherwise False
        '''
        # The circles is colliding if the distance between their centers is smaller than the sum of their radii
        return(((self.pos[0] - playerPos[0])**2 + (self.pos[1] - playerPos[1])**2)**0.5 < self.size + playerSize)