import pygame

class Button():
    '''
    Button
    
    A button that the user can click.
    The buttons will allow the user to navagate the menus
    
    FUNCTIONS
        __init__(self, nextGameStateIn, buttonRectangeIn, buttonColorIn, textIn, textColorIn, fontIn)
            Creates the button object with initial values.
        
        draw(self, surfaceIn)
            Draws the button as a rounded rectangle with text.
            
        isClicked(self, mousePosition)
            Returns true if the mouse is on the button
        
    '''    
    def __init__(self, nextGameStateIn, buttonRectangeIn, buttonColorIn, textIn, textColorIn, fontIn):
        '''
        Initializes a Button Object

        Object contains all the values needed to make a button with text

        Parameters
        ----------
        nextGameStateIn: str
            The next game state that will run when this button is clicked

        buttonRectangeIn: pygame.Rect() or [left, top, width, height] 
            The rectangle object that represents the top-left position of the
            Button and its dimensions.

        buttonColorIn: pygame.Color() or (r, g, b)  
            The color of the button
            
        textIn: str 
            The text that will appear on the button
            
        textColorIn: pygame.Color() or (r, g, b) 
            The color of the text on the button
            
        fontIn: pygame.Font() 
            The font used to render the text

        Returns
        -------
        None
        '''
        self.buttonRectangle = buttonRectangeIn
        self.buttonColor = buttonColorIn
        self.text = textIn
        self.textColor = textColorIn
        self.nextGameState = nextGameStateIn
        self.font = fontIn
        
    def draw(self, surfaceIn):
        '''
        Draws the Button Object

        Draws the Button as a rounded rectangle with text onto the given surface.

        Parameters
        ----------
        surfaceIn: pygame.Surface()
            The surface that the button will be drawn onto
            
        Returns
        -------
        None
        '''
        # draw a rounded rectangle for the button
        pygame.draw.rect(surfaceIn, self.buttonColor, self.buttonRectangle, border_radius = 2)
        
        # render the text of the button
        buttonText = self.font.render(self.text, 1, self.textColor)
        
        # blit the text onto surfacein. make it centered on the button rectangle. 
        surfaceIn.blit(buttonText, (self.buttonRectangle[0] + self.buttonRectangle[2]/2 - buttonText.get_width()/2,
                                    self.buttonRectangle[1] + self.buttonRectangle[3]/2 - buttonText.get_height()/2))
        
    def isClicked(self, mousePosition):
        '''
        Determine if the player's mouse is clicking on the button

        Using the position of the mouse and button determine if
        the mouse is on the button. Call this function on a
        mouse-down event to know if the button has been pressed.

        Parameters
        ----------
        mousePosition: List<int>
            The position of the player's mouse on the surface
            
        Returns
        -------
        bool
            True if the player is clicking on the button
        '''
        # return true if the position of the mouse is inside the button rectangle 
        return(mousePosition[0] > self.buttonRectangle[0] and
               mousePosition[0] < self.buttonRectangle[0] + self.buttonRectangle[2] and
               mousePosition[1] > self.buttonRectangle[1] and
               mousePosition[1] < self.buttonRectangle[1] + self.buttonRectangle[3])