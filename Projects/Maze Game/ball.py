import pygame

class Ball():
    '''
    Ball
    
    The player's 'character'. It can move around the screen and interact with other objects.
    
    FUNCTIONS
        __init__(self, nextGameStateIn, buttonRectangeIn, buttonColorIn, textIn, textColorIn, fontIn)
            Creates the button object with initial values.
        
        update(self, surfaceIn, walls, deltatime)
            Updates the position of the ball and calls the draw function
            
        draw(self, surfaceIn)
            Draws the ball as a circle on a surface
        
        move(self, walls, deltatime)
            Updates the position of the ball.
            Uses user input to determine the new position
        
        setMove(self, isMovingIn, directionIn)
            Changes the isMoving and the direction variables
        
        validateMove(self, walls)
            Assures the ball cannot pass through walls
        
        '''    
    def __init__(self, posIn, sizeIn, colorIn):
        '''
        Initializes a Ball Object

        Object contains values for the position, size, and color of the ball
        as well as information about its movement.

        Parameters
        ----------
        posIn: List<int>
            The x-y position of the flag on the mainSurface

        sizeIn: int 
            The size of the circle that represents the ball.

        colorIn: pygame.Color() or (r, g, b)  
            The color of the ball

        Returns
        -------
        None
        '''
        self.pos = posIn
        self.color = colorIn
        self.size = sizeIn
        
        self.isMoving = False
        self.direction = [0, 0]
        self.speed = 100
         
    def update(self, surfaceIn, walls, deltatime):
        '''
        Updates the ball's position and draws it.

        The ball's position is updated based on its movement and its collision.
        The ball is then drawn.

        Parameters
        ----------
        surfaceIn: pygame.Surface()
            The surface the ball will be drawn on.

        walls: List<Wall()> 
            The list of wall the ball can collide with.

        deltatime: float  
            The time that has elapsed between frames.

        Returns
        -------
        None
        '''
        # update the ball's position
        self.move(walls, deltatime)
        
        # draw the ball
        self.draw(surfaceIn)
    
    def draw(self, surfaceIn):
        '''
        Draws the Ball Object

        Draws the Ball as a circle with the specified color, size, and position on a given surface.

        Parameters
        ----------
        surfaceIn: pygame.Surface()
            The surface that the ball will be drawn onto
            
        Returns
        -------
        None
        '''
        # draw a circle on the surface
        pygame.draw.circle(surfaceIn, self.color, self.pos, self.size)
    
    def move(self, walls, deltatime):
        '''
        Update the ball's position

        Change the ball's position based on its movement.
        Validate the new position of the ball and if it is colliding with
        a wall, change its position to the adjusted position.

        Parameters
        ----------
        walls: List<Wall()> 
            The list of walls the ball can collide with.

        deltatime: float  
            The time that has elapsed between frames.

        Returns
        -------
        None
        '''
        # update the ball's position using its move direction, its speed, and the elapsed time
        tempPos = self.pos.copy()
        if(self.isMoving):
            tempPos[0] += self.direction[0] * self.speed * deltatime
            tempPos[1] += self.direction[1] * self.speed * deltatime
        
        # check if the ball's new position is colliding with any walls
        isColliding = self.validateMove(walls)
        
        # if the ball is colliding with something
        # set its position to the adjusted position
        if(isColliding[0]): self.pos = isColliding[1]
        
        # otherwise set its position to the previously found position
        else: self.pos = tempPos.copy()
    
    def setMove(self, isMovingIn, directionIn):
        '''
        Changes movement values of the ball.

        Changes the isMoving variable and the direction variable.

        Parameters
        ----------
        isMovingIn : bool
            Whether or not the ball should be moving
          
        directionIn : string
            The direction the ball should travel in
            'left', 'right', 'up' or 'down'

        Returns
        -------
        None

        Raises
        -------
        ValueError
            If the directionIn is not 'left', 'right', 'up', 'down' or ''
        '''
        # Update the isMoving variable
        self.isMoving = isMovingIn
        
        # Convert the direction string to a vector
        # Update the direction value with the new vector
        if(directionIn == ''):
            return
        elif(directionIn == 'left'):
            self.direction = [-1, 0]
            
        elif(directionIn == 'right'):
            self.direction = [1, 0]
            
        elif(directionIn == 'up'):
            self.direction = [0, -1]
            
        elif(directionIn == 'down'):
            self.direction = [0, 1]
            
        else:
            raise ValueError("directionIn must be ['left', 'right', 'down', 'up']")
        
    def validateMove(self, walls):
        '''
        Determine if the ball is colliding with any walls.

        Use the walls collision method to determine if the player is
        colliding with any walls. If the player is colliding with a wall
        return True and the adjusted position of the player

        Parameters
        ----------
        walls: List<Wall()> 
            The list of walls the ball can collide with.

        Returns
        -------
        bool
            True if the player is colliding with the wall otherwise False
        
        List<int>
            The new position of the player.
            If the player is colliding with a wall, the position will be adjusted
            otherwise it will remain the same.

        Raises
        -------
        ValueError
            If no walls are in the walls list
        '''
        result = []
        # raise an error if there are no walls to collide with
        if(len(walls) == 0): raise ValueError('No walls are initialized')
        
        # for every wall
        for wall in walls:
            # check if it is colliding with the player
            #  store the result
            result = wall.isColliding(self.pos, self.size)
            
            # if the player is colliding with the wall
            # break and return the result of this check
            if(result[0]):
                break
            
        # return the last result calculated
        return result