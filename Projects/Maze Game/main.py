#-----------------------------------------------------------------------------
# Name:        Assignment Template (assignment.py)
# Purpose:     A simple maze game with a user controlled player and impassable obsticals.
#                Explore the pygame library and demonstrate planning skills.
#
# Author:      Lex Stapleton
# Created:     03-08-2021
# Updated:     03-14-2021
#-----------------------------------------------------------------------------
# I think this project deserves a level 4+ because I met all the criteria for
# the project and also added new features. My code is also well polished and efficient.
#
# My project includes movement controls to move a ball around the maze and has obstacles
# that the player cannot pass through. There are screens for the start, the end, and for instructions on
# how to play. I've also included extra features like a timer and score system and a maze generating algorithm
# for replayability.
#
# My code is well polished and efficient.
# 
#Features Added:
#   - randomly generated mazes using a recursive backtracking algorithm
#   - Buttons that register clicks and allow the user to navigate the various menu screens
#   - The use of a timer to limit the player's time to solve the maze and a scoring system
#
#   - A ball that can move around and not pass through obstacles
#   - Various screens for the Start Menu, Help Menu, Game Screen, and Game Over Screen
#-----------------------------------------------------------------------------

import pygame
import random
from ball import Ball
from flag import Flag
from wall import Wall
from button import Button
from maze_generator import MazeGenerator

pygame.init()

# Colors
BACKGROUNDCOLOR = (6, 36, 84)
WALLCOLOR = pygame.Color('white')
BUTTONCOLOR = (255, 69, 125)
TEXTCOLOR = (175, 177, 196)

# Fonts
GIANTTEXT = pygame.font.SysFont("Arial", 40)
LARGETEXT = pygame.font.SysFont("Arial", 25)
SMALLTEXT = pygame.font.SysFont("Arial", 20)
TINYTEXT = pygame.font.SysFont("Arial", 15)

surfaceSize = 500

# Maze variables
cellSize = 20
mazeSize = (int(surfaceSize * 0.8 // cellSize), int(surfaceSize * 0.5 // cellSize))
mazeStartPoint = (surfaceSize*0.1, surfaceSize*0.3)
mazeWalls = []
mazeGenerator = MazeGenerator(mazeSize)

# Player variables
ballStartPoint = [mazeStartPoint[0] + cellSize*0.5, mazeStartPoint[1] + cellSize*0.5]
ball = Ball(ballStartPoint, cellSize * 0.25, pygame.Color('red'))

# Flag variables 
flagStartPoint = [random.randint(1, mazeSize[0]) * cellSize + cellSize * 0.5 + mazeStartPoint[0],
                  random.randint(1, mazeSize[1]) * cellSize + cellSize * 0.5 + mazeStartPoint[1]]
flag = Flag(flagStartPoint, 3, pygame.Color('green'))

def writeText(surface, text, textPos, font, textColor):
    '''
    Draws the text on the screen

    Renders and blits text onto a given surface. The parameters control the
    font, color, position, and text displayed.

    Parameters
    ----------
    surface: pygame.Surface()
        The surface that the text will be drawn onto
        
    text: string
        What the text will say
        
    textPos: List<int>
        The top left corner of the text on the surface
        [x, y]
    
    font: pygame.Font()
        The font that will be used to render the text
        
    textColor: pygame.Color() or (r, g, b)
        The color of the text
        
    Returns
    -------
    None
    '''
    # Render the text onto a surface
    textSurface = font.render(text, 1, textColor)
    
    # blit the surface onto surfaceIn at the given position
    surface.blit(textSurface, textPos)
    
def writeTextCentered(surfaceIn, text, textCenter, font, textColor):
    '''
    Draws the text on the screen

    Renders and blits text onto a given surface. The parameters control the
    font, color, position, and text displayed. The text will be centered on
    the given position

    Parameters
    ----------
    surface: pygame.Surface()
        The surface that the text will be drawn onto
        
    text: string
        What the text will say
        
    textCenter: List<int>
        The center of the text on the surface
        [x, y]
    
    font: pygame.Font()
        The font that will be used to render the text
        
    textColor: pygame.Color() or (r, g, b)
        The color of the text
        
    Returns
    -------
    None
    '''
    # Render the text onto a surface
    textSurface = font.render(text, 1, textColor)
    
    # blit the surface onto surfaceIn using
    #  the given position as a center
    surfaceIn.blit(textSurface, (textCenter[0] - textSurface.get_width()/2,
                                 textCenter[1] - textSurface.get_height()/2))

def calculateRandomStartPoint(mazeSize, cellSize, mazeStartPoint):
    '''
    Finds a random position within the maze

    Determines a random position in the maze so that the position in
    pixels will be in the center of a cell in the maze.

    Parameters
    ----------
    mazeSize: List<int>
        The amount of cells in the maze
        [x, y]
        
    cellSize: int
        the pixel size of each cell
        
    mazeStartPoint: List<int>
        The top-left corner of the maze
        [x, y]
        
    Returns
    -------
    List<int>
        A randomly chosen pixel position in the maze
        [x, y]
    '''
    # Return a random 2-d point inside the maze
    #  The point is centered in a randomly chosen cell
    return [random.randint(1, mazeSize[0] - 1) * cellSize + cellSize * 0.5 + mazeStartPoint[0],
            random.randint(1, mazeSize[1] - 1) * cellSize + cellSize * 0.5 + mazeStartPoint[1]]

def initializeNewMaze():
    '''
    Initializes a new maze

    Creates a new randomly generated maze and creates the wall objects that will make up the maze.

    Parameters
    ----------
    None
        
    Returns
    -------
    None
    '''
    global mazeWalls
    # Generate a new maze
    mazeGenerator.generateMaze()
    # Create wall objects
    mazeWalls = makeWalls(mazeStartPoint, mazeGenerator.maze, cellSize, WALLCOLOR)

def restartCurrentMaze():
    '''
    Restarts the maze

    Updates the position of the player and the flag to a new random location in the maze.

    Parameters
    ----------
    None
        
    Returns
    -------
    None
    '''
    # put the player and the flag in a random location in the maze
    ball.pos = calculateRandomStartPoint(mazeSize, cellSize, mazeStartPoint)
    flag.pos = calculateRandomStartPoint(mazeSize, cellSize, mazeStartPoint)

def makeWalls(startingPos, maze, cellSize, wallColor):
    '''
    Creates the walls of the maze

    using cell objects it creates and returns wall objects that will make up the maze.

    Parameters
    ----------
    startingPos: List<int>
        The top left corner of the maze
    
    maze: MazeGenerator()
        A maze object that contains cells objects that will determine the position of the walls
        
    cellSize: int
        the pixel size of a cell
        
    wallColor: pygame.Color() or (r, g, b)
        the color of the walls
        
    Returns
    -------
    List<Wall()>
        The walls that make up the maze
    '''
    
    mazeWalls = []
    # for every cell in the maze
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            # If a wall needs to be added create a new wall and append it to mazeWalls
            # LEFT WALL
            if cell.walls[-2]:
                mazeWalls.append(Wall(pygame.Rect(x * cellSize + startingPos[0], y * cellSize + startingPos[1], cellSize * 0.1, cellSize), wallColor))
            
            # RIGHT WALL    
            if cell.walls[2]:
                mazeWalls.append(Wall(pygame.Rect(x * cellSize + startingPos[0]+(cellSize*0.9), y * cellSize + startingPos[1], cellSize * 0.1, cellSize), wallColor))
            
            # TOP WALL
            if cell.walls[-1]:
                mazeWalls.append(Wall(pygame.Rect(x * cellSize + startingPos[0], y * cellSize + startingPos[1], cellSize, cellSize*0.1), wallColor))
                
            # BOTTOM WALL
            if cell.walls[1]:
                mazeWalls.append(Wall(pygame.Rect(x * cellSize + startingPos[0], y * cellSize + startingPos[1]+(cellSize*0.9), cellSize, cellSize * 0.1), wallColor))
    
    return mazeWalls  

def addButtonColumn(buttonsToAdd, buttonInfo):
    '''
    Creates a column of buttons

    Creates a column of different buttons that all look the same (except for the text).

    Parameters
    ----------
    buttonsToAdd: Dictionary<string, string>
        The text on each button and the gameState that will be activated when the button is pressed
        {nextGameState: text}
    
    buttonInfo: Dictionary<string, dynamic>
        The parameters of each buttons.
        Must include these parameters:
        {'buttonXCenter': int,
        'buttonYCenter': int,
        'buttonHeight' int,
        'buttonWidth': int,
        'buttonPadding': int,
        'font': font
        }
        
    Returns
    -------
    List<Button()>
        The buttons that have been created
        
    Raises
    -------
    KeyError
        If one of the specified keys in the buttonInfo is not added this will be raised
    '''
    buttons = []
    # For every button that needs to be added
    for i, button in enumerate(list(buttonsToAdd.items())):
        # Calculate the top-left position of the first button
        buttonX = buttonInfo['buttonXCenter'] - buttonInfo['buttonWidth'] * 0.5
        buttonY = buttonInfo['buttonYCenter'] + (buttonInfo['buttonHeight'] + buttonInfo['buttonPadding']) * i
        
        # Create a new button object according to the given specs
        # add the button to buttons
        buttons.append(
            Button(button[0],
                   [buttonX, buttonY, buttonInfo['buttonWidth'],
                   buttonInfo['buttonHeight']],
                   BUTTONCOLOR,
                   button[1],
                   TEXTCOLOR,
                   buttonInfo['font'])
            )
    return buttons

def main():
    '''
    Main loop of the game

    Runs the game. Controls the initialization and display of different screens,
    events, the scoring system, and the timing system.

    Parameters
    ----------
    None
        
    Returns
    -------
    None
    '''
    clock = pygame.time.Clock()
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))
  
    isWPressed, isAPressed, isSPressed, isDPressed = False, False, False, False
    
    gameTimer = 0
    timePerRound = 30
    
    roundNumber = 1
    roundsPerGame = 3
    
    score = 0
    
    buttons = []
    
    gameState = 'initializeStart'
    
    play = True
    while play:
        
        # time between frames in seconds
        deltatime = clock.tick(130)/1000
        
        # all events that are currently triggered
        events = pygame.event.get()
        
        # if the quit event was triggered, exit the game
        for event in events:
            if event.type == pygame.QUIT:
                play = False
                
        if(gameState == 'initializeStart'):
            
            # Create a column of buttons for the start screen
            # Start, Help, Quit
            buttonPositionInfo = {
                'buttonWidth':100,
                'buttonHeight':50, 
                'buttonXCenter':surfaceSize * 0.5,
                'buttonYCenter':surfaceSize * 0.5,
                'buttonPadding':10,
                'font':SMALLTEXT
                }
            
            buttonsToAdd = {
                'initializeGame':'Start',
                'initializeHelp':'Help',
                'quit':'Quit'
                }
            
            buttons.clear()
            buttons = addButtonColumn(buttonsToAdd, buttonPositionInfo)
            
            # switch to the start screen
            gameState = 'start'
            
        if(gameState == 'start'):
            # if the mouse button is clicked
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    
                    # Check if any of the buttons were clicked
                    for button in buttons:
                        # if they were clicked switch to their associated game state
                        if(button.isClicked(pygame.mouse.get_pos())): gameState = button.nextGameState
            
            mainSurface.fill(BACKGROUNDCOLOR)
            
            # Draw a title and the buttons
            writeText(mainSurface, "THE MOST A-MAZE-ING GAME EVER", (30, 100), LARGETEXT, TEXTCOLOR)
            
            for button in buttons:
                button.draw(mainSurface)

        elif(gameState == 'initializeHelp'):
            # Create a column of buttons for the start screen
            # Start Menu, Quit 
            buttonInfo = {
                'buttonWidth':80,
                'buttonHeight':30, 
                'buttonXCenter':surfaceSize * 0.85,
                'buttonYCenter':surfaceSize * 0.8,
                'buttonPadding':10,
                'font':TINYTEXT
                }
            
            buttonsToAdd = {
                'initializeStart':'Start Menu',
                'quit':'Quit'
                }
            
            buttons.clear()
            buttons = addButtonColumn(buttonsToAdd, buttonInfo)
            
            # switch to the help screen
            gameState = 'help'
            
        elif(gameState == 'help'):
            # if the mouse button is clicked
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    
                    # Check if any of the buttons were clicked
                    for button in buttons:
                        # if they were clicked switch to their associated game state
                        if(button.isClicked(pygame.mouse.get_pos())): gameState = button.nextGameState
            
            mainSurface.fill(BACKGROUNDCOLOR)
            
            # Draw instuctions for the player 
            writeText(mainSurface, "Use WASD to navigate the maze", (30, 50), LARGETEXT, TEXTCOLOR)
            writeText(mainSurface, "Collect the Green Circle to gain points", (30, 80), LARGETEXT, TEXTCOLOR)
            writeText(mainSurface, "When time runs out you will be ", (30, 110), LARGETEXT, TEXTCOLOR)
            writeText(mainSurface, "given a new maze", (40, 140), LARGETEXT, TEXTCOLOR)
            writeText(mainSurface, f"After {roundsPerGame} rounds are over the game ends", (30, 170), LARGETEXT, TEXTCOLOR)
            
            # Draw the buttons
            for button in buttons:
                button.draw(mainSurface)
            
        elif(gameState == 'initializeGame'):
            
            # Create a column of buttons for the game screen
            # Exit Game, Quit 
            buttonInfo = {
                'buttonWidth':80,
                'buttonHeight':30, 
                'buttonXCenter':surfaceSize * 0.85,
                'buttonYCenter':surfaceSize * 0.8,
                'buttonPadding':10,
                'font':TINYTEXT
                }
            
            buttonsToAdd = {
                'initializeStart':'Exit Game',
                'quit':'Quit'
                }
            
            buttons.clear()
            buttons = addButtonColumn(buttonsToAdd, buttonInfo)
            
            # Create a new maze
            # place the player and flag in the maze
            initializeNewMaze()
            restartCurrentMaze()
            
            # Initalize the timer, the round number, and the score
            gameTimer = timePerRound
            roundNumber = 1
            score = 0
            
            # switch to the game screen
            gameState = 'game'
            
        elif(gameState == 'game'):
            # Remove the elapsed time from the timer
            gameTimer -= deltatime
            
            
            for event in events:
                # if a key is pressed
                if event.type == pygame.KEYDOWN:
                    # record which is pressed down and record the other keys as unpressed
                    if(event.key == 119): isWPressed, isAPressed, isSPressed, isDPressed = True, False, False, False
                    elif(event.key == 97): isWPressed, isAPressed, isSPressed, isDPressed = False, True, False, False   
                    elif(event.key == 115): isWPressed, isAPressed, isSPressed, isDPressed = False, False, True, False                         
                    elif(event.key == 100): isWPressed, isAPressed, isSPressed, isDPressed = False, False, False, True 
            
                # if a key is unpressed
                elif event.type == pygame.KEYUP:
                    # record which key is unpressed
                    if(event.key == 119): isWPressed = False     
                    elif(event.key == 97): isAPressed = False           
                    elif(event.key == 115): isSPressed = False
                    elif(event.key == 100): isDPressed = False
                        
                # if the mouse button is clicked          
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Check if any of the buttons were clicked
                    for button in buttons:
                        # if they were clicked, switch to their associated game state
                        if(button.isClicked(pygame.mouse.get_pos())): gameState = button.nextGameState

            # tell the ball object what direction it should move
            if(isWPressed): ball.setMove(True, 'up')
            elif(isAPressed): ball.setMove(True, 'left')
            elif(isSPressed): ball.setMove(True, 'down')
            elif(isDPressed): ball.setMove(True, 'right')
            else: ball.setMove(False, '')
                
            mainSurface.fill(BACKGROUNDCOLOR)
        
            # draw the walls 
            for wall in mazeWalls:
                wall.draw(mainSurface)
            
            # draw the player and the flag
            flag.draw(mainSurface)
            ball.update(mainSurface, mazeWalls, deltatime)
            
            # draw the buttons
            for button in buttons:
                button.draw(mainSurface)
            
            # write text for the Time Left, the Rounds, and the Score
            writeText(mainSurface, f'Time Left: {str(round(gameTimer, 2))}', (10, 10), SMALLTEXT, TEXTCOLOR)
            writeText(mainSurface, f'Rounds: {roundNumber}', (10, 40), SMALLTEXT, TEXTCOLOR)
            writeText(mainSurface, f'Score: {score}', (10, 70), SMALLTEXT, TEXTCOLOR)
            
            # If the player has reached the flag
            if(flag.isColliding(ball.pos, ball.size)):
                # randomly place the player, and flag in the maze
                restartCurrentMaze()
                # increase the score
                score += int(gameTimer * 10)
            
            # if time runs out
            if(gameTimer < 0):
                # if there are no more rounds left, end the game
                if(roundNumber == roundsPerGame): gameState = 'initializeGameOver'
                # otherwise increment the roundNumber
                roundNumber += 1
                # Start a new round with a new maze
                gameTimer = timePerRound
                initializeNewMaze()
                restartCurrentMaze()
        
        elif(gameState == 'initializeGameOver'):
            # Create a column of buttons for the game over screen
            # Start Menu, New Game, Quit 
            buttonInfo = {
                'buttonWidth':80,
                'buttonHeight':30, 
                'buttonXCenter':surfaceSize * 0.85,
                'buttonYCenter':surfaceSize * 0.75,
                'buttonPadding':10,
                'font':TINYTEXT
                }
            
            buttonsToAdd = {
                'initializeStart':'Start Menu',
                'initializeGame':'New Game',
                'quit':'Quit'
                }
            
            buttons.clear()
            buttons = addButtonColumn(buttonsToAdd, buttonInfo)
            
            # switch to the game over screen
            gameState = 'gameOver'
        
        elif(gameState == 'gameOver'):
            # if the mouse button is clicked
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    # Check if any of the buttons were clicked
                    for button in buttons:
                        # if they were clicked, switch to their associated game state
                        if(button.isClicked(pygame.mouse.get_pos())): gameState = button.nextGameState
            
            mainSurface.fill(BACKGROUNDCOLOR)
            # write a game over message and the final score
            writeTextCentered(mainSurface, "GAME OVER", (surfaceSize/2, 100), GIANTTEXT, TEXTCOLOR)
            writeTextCentered(mainSurface, f"Score: {score}", (surfaceSize/2, 140), LARGETEXT, TEXTCOLOR)
            
            # draw the buttons
            for button in buttons:
                button.draw(mainSurface)
        
        elif(gameState == 'quit'):
            play = False
            
        else:
            raise ValueError(f'{gameState} is not a valid Game State')

        pygame.display.flip()
        
    pygame.quit()
        
main()