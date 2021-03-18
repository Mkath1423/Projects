#-----------------------------------------------------------------------------
# Name:        Game manager (gameManager.py)
#              Database Tool (databaseTools.py)
#              Sqlite Manager (squliteManager.py)
#
# Purpose:     Allow users to create a level that they can then navigate 
#
# Author:      Lex Stapleton
# Created:     18-Feb-2021
# Updated:     22-Feb-2021
#-----------------------------------------------------------------------------
#      I think this project deserves a level 4+ because I have met all the assignment 
# requirement and done much more. I have made a simple adventure game that takes in user input,
# allows them to decide where they go in a given level and makes use of the time.sleep() method.
# I do this while making use of for and while loops, boolean operators and many functions.
# The code is also well polished and many extra features are added.
#
#      The main feature I added is the ability to create new save files from within the GUI and a
# way to modify existing save files. This makes use of sqlite databases that get created and modified
# upon the user's request. The squliteManager contains functionality that allows me to connect to databases
# created tables and insert, select and update data. These functions  all generate queries from the parameters.
# This script is not specific to this program and can be used in other applications.
#
#      The databaseTools provides more game-specific functionality like making a new database with the tables and columns
# needed for this game.
#
#Features Added:
#   Users can select save files from the main menu
#   Users can create new save files
#   Users can modify the rooms in an existing save file
#   Users can navigate through a level without end
#-----------------------------------------------------------------------------
import time as time
import sqlite_manager as db
import databaseTools as dbTools
import PySimpleGUI as sg

# define global variables for in game
gameSave = 'Preset' # what gameSave is being used
gameLevelInfo = dbTools.getLevelInfo(gameSave) # information about the gameSave
roomInfo = {} # information about the current room

# define global variables for the editor
editorSave = 'Preset' # what gameSave is being used
editorLevelInfo = dbTools.getLevelInfo(editorSave) # information about the gameSave

currentWindow = 'MainMenu'

def goBackTo(currentWindow):
    '''
  This function tells you what window the back button should take you to based on your currentWindow.
  
  Using a dictionary  lookup the correct window to go back to is returned

  Parameters
  ----------
  current : str
    The window that is currently visible.

  
  Returns
  -------
  str
    The window that the back button should take you to. This window will currently be invisible
    and should be made visible after this function is called. 
'''
    switcher = {
        'GameMenu' : 'MainMenu',
        'EditMenu' : 'MainMenu'
        }
    
    # return the room you should go back to
    return switcher[currentWindow]

def changeWindow(nextWindow):
    '''
  This function changes what window is currently visible.
  
  The window that is currently visible will be made invisible.
  The nextWindow will be made visible.
  The name of the now visible window will be stored globally for later
  referance.

  Parameters
  ----------
  nextWindow : str
    The window that is currently visible.

  
  Returns
  -------
  None
'''
    global currentWindow
    
    # switch what window is currently visible and refresh the screen
    window[currentWindow].update(visible = False)
    window[nextWindow].update(visible = True)
    window.refresh()
    
    # change the currentWindow variable to refelect the change in windows
    currentWindow = nextWindow

def findGamePaths():
    '''
  This function finds the paths of all the gameSaves
  
  This function reads the gameFilePaths.txt file and returns all the gameSaves
  that are stored within it.

  Parameters
  ----------
  None

  
  Returns
  -------
  list<str>
     A list of all the game paths.
     This does not include their directory only the name of the file.
'''
    # read and save the information in gaemFilePaths.txt
    gameFilePaths = open('GameFiles/gameFilePaths.txt', 'r')
    paths = gameFilePaths.read()        
    gameFilePaths.close()

    # split the data into a list of strings
    return paths.split(',')
    
def displayRoom(roomId):
    '''
  This function displays the information for a room when ingame
  
  This function changes the values of the room info text elements as well as the movement buttons.
  There is some delay between the different values changing.
  Only buttons with valid movement options are made visible to the user.
  

  Parameters
  ----------
  roomId
    The id of the room you want to be displayed

  
  Returns
  -------
  None
'''    
    global roomInfo

    # get the data from the room
    data = dbTools.getRoomData(gameSave, roomId)
    roomData = data[0]
    connectionsData = data[1]
    
    # update roomInfo to store the new data
    roomInfo.clear()
    roomInfo['id'] = roomData[0]
    roomInfo['room_name'] = roomData[1]
    roomInfo['room_description'] = roomData[2]
    
    roomInfo['N'] = connectionsData[0]
    roomInfo['E'] = connectionsData[1]
    roomInfo['S'] = connectionsData[2]
    roomInfo['W'] = connectionsData[3]
    
    # Change the in game GUI elements to default to invisible
    window.FindElement('RoomName').update(visible = False)
    window.FindElement('RoomDescription').update(visible = False)

    window.FindElement('NorthButton').update(visible = False)
    window.FindElement('SouthButton').update(visible = False)
    window.FindElement('EastButton').update(visible = False)
    window.FindElement('WestButton').update(visible = False)
    window.refresh()
    
    # Update the room name element to display the name of the room
    # delay for 1 second
    window.FindElement('RoomName').update(value = f'You are in {roomData[1]}', visible = True)
    window.refresh()
    time.sleep(1)
    
    # Update the room description element to display the description of the room
    # delay for 3 seconds
    window.FindElement('RoomDescription').update(value = roomData[2], visible = True)
    window.refresh()
    time.sleep(3)
    
    # For each of the directional input buttons
    i = 0
    for direction in ['North', 'East', 'South', 'West']:
        # if the value of the direction is not 0 (0 is treated as no connection)
        if(not connectionsData[i] == 0):
            # update their value to show where the button takes you
            window.FindElement(f'{direction}Button').update(text = f'Go {direction} to {gameLevelInfo[connectionsData[i]]}', visible = True)
            window.refresh()
            # delay slightly in-between buttons
            time.sleep(0.5)
        i += 1
        
# IN-GAME #
# the menu that will be displayed in-game
GameMenu = [[sg.Column([
            [sg.Text('roomName', size = (20, 1), key = 'RoomName', visible = False)],
            [sg.Text('roomDescription', size = (20, 5), key = 'RoomDescription', visible = False)],
            [sg.Button('North', key = 'NorthButton', visible = False)],
            [sg.Button('East', key = 'EastButton', visible = False)],
            [sg.Button('South', key = 'SouthButton', visible = False)],
            [sg.Button('West', key = 'WestButton', visible = False)],
            [sg.Button('Back to MainMenu', key = 'Back', visible = True)],
            ])]]

# MAIN MENU #
# the layout box that lets you select what gameSave you want to play in 
GameSaveSelector = [[sg.Listbox(findGamePaths(), select_mode = 'LISTBOX_SELECT_MODE_SINGLE', size = (10, 10),  key = 'GameSavesListBox')],
                      [sg.Button('Ok', key = 'GameSaveSelectButton')],
                      [sg.Text(findGamePaths()[0], size = (20, 1),key = 'SelectedGameSave')],
                      [sg.Sizer(250, 100)]]

# the buttons that take you to the edit menu or start the game
MainMenuOptions = [[sg.Text('WELCOME TO CHOOSE YOUR OWN ADVENTURE')],
                   [sg.Button('Start Game', key = 'StartGame')],
                   [sg.Button('Edit Saves', key = 'EditSaves')],
                   [sg.Sizer(750, 400)]]

# the layout that will be displayed in the main menu
MainMenu = [[sg.Frame('Choose Save File:', GameSaveSelector, vertical_alignment = 't'),
             sg.Column(MainMenuOptions, element_justification = 'center', vertical_alignment = 'c')],
            [sg.Column([[sg.Button('Exit')]], size = (1000, 100), element_justification = 'right')]]

# EDIT MENU #
# the listbox that lets you select what database you want to edit
# also lets you create new databases
DatabaseSelector = [[sg.Listbox(findGamePaths(), select_mode = 'LISTBOX_SELECT_MODE_SINGLE', size = (10, 10),  key = 'DataBaseListBox')],
                   [sg.Button('Ok', key = 'SelectDatabase')],
                   [sg.Input(size = (16, 1), key = 'NewDatabaseName'),sg.Button('New', key = 'CreateNewDatabase')]]

# the listbox that lets you select what room you want to edit
RoomSelector = [[sg.Listbox(list(editorLevelInfo.keys())[:-1], select_mode = 'LISTBOX_SELECT_MODE_SINGLE', size = (10, 10),  key = 'RoomSelectorListBox')],
                      [sg.Button('Ok', key = 'SelectRoom')],
                      [sg.Button('New Room', key = 'CreateNewRoom')]]

# the input field to set the new room values
# the button to save the values
RoomEditor = [[sg.Text(editorSave, key = 'SaveName', size = (20, 1))],
              
                   [sg.Column([
                       [sg.Text('Room Id:', size = (16, 1)), sg.Text('id', key = 'RoomIdText', size = (16, 1))],
                       [sg.Text('Room Name', size = (16, 1)), sg.Input(size = (16, 1), key = 'RoomNameInput')],
                       [sg.Text('Room Description', size = (16, 1)), sg.Input(size = (16, 1), key = 'RoomDescriptionInput')]],
                   element_justification = 'right')],
                   
                   [sg.Column([
                        [sg.Text('Connections (input a room id)')],
                        [sg.Text('North', size = (16, 1)), sg.Input(size = (16, 1), key = 'NorthConnectionInput')],
                        [sg.Text('East', size = (16, 1)), sg.Input(size = (16, 1), key = 'EastConnectionInput')],
                        [sg.Text('South', size = (16, 1)), sg.Input(size = (16, 1), key = 'SouthConnectionInput')],
                        [sg.Text('West', size = (16, 1)), sg.Input(size = (16, 1), key = 'WestConnectionInput')]],
                   element_justification = 'center')],

                   [sg.Button('Submit Changes', key = 'SubmitChanges')],
                   [sg.Button('Back to Main Menu', key = 'Back')]]

# the layout that will be displayed in the edit menu
EditMenu = [[sg.Column(DatabaseSelector, size = (200, 500)),
             sg.Column(RoomEditor, size = (600, 500), element_justification = 'center'),
             sg.Column(RoomSelector, size = (200, 500))]]

# all the layouts that will be used in the game
layout = [[sg.Column(MainMenu, size = (1000, 500), key = 'MainMenu', visible = True),
           sg.Column(EditMenu, size = (1000, 500), key = 'EditMenu', visible = False),
           sg.Column(GameMenu, size = (1000, 500), key = 'GameMenu', visible = False)]]

window = sg.Window('Choose Your Own Adventure', layout, size = (1000, 500))

# game loop
while True:
    event, values = window.read()
    
    # Changes what gameSave will be used during the game
    if(event == 'GameSaveSelectButton'):
        # update the text element to tell you what game will be used
        window.FindElement('SelectedGameSave').Update(value = values['GameSavesListBox'][0])
        
        # store the gameSave and its info
        gameSave = values["GameSavesListBox"][0]
        gameLevelInfo = dbTools.getLevelInfo(gameSave)
        
    #Start the game
    elif(event == 'StartGame'):
        # change to the GameMenu and display the first room
        gameLevelInfo = dbTools.getLevelInfo(gameSave)
        changeWindow('GameMenu')
        displayRoom(1)
    
    # display the room the north button goes to
    elif(event == 'NorthButton'):
        displayRoom(roomInfo['N'])
        
    # display the room the east button goes to
    elif(event == 'EastButton'):
        displayRoom(roomInfo['E'])
        
    # display the room the south button goes to
    elif(event == 'SouthButton'):
        displayRoom(roomInfo['S'])
        
    # display the room the west button goes to
    elif(event == 'WestButton'):
        displayRoom(roomInfo['W'])
    
    
    #Go to the Edit Menu
    elif(event == 'EditSaves'):
        changeWindow('EditMenu')
    
    # Changes what database is being edited
    elif(event == 'SelectDatabase'):
        if(values['DataBaseListBox']):
            # store what database is being edited and its info
            editorSave = values["DataBaseListBox"][0]
            editorLevelInfo = dbTools.getLevelInfo(editorSave)

            # update the rooms listbox and the SaveName text element 
            window.FindElement('RoomSelectorListBox').Update(list(editorLevelInfo.keys())[:-1])    
            window.FindElement('SaveName').Update(value = editorSave)
            
            # clear the room input fields
            window.FindElement('RoomIdText').Update(value = 'id')
            window.FindElement('RoomNameInput').Update(value = '')
            window.FindElement('RoomDescriptionInput').Update(value = '')
            
            window.FindElement('NorthConnectionInput').Update(value = '')
            window.FindElement('EastConnectionInput').Update(value = '')
            window.FindElement('SouthConnectionInput').Update(value = '')
            window.FindElement('WestConnectionInput').Update(value = '')
            
    # creates a new database
    elif(event == 'CreateNewDatabase'):
        if(not values['NewDatabaseName'] == ''):
            # creat the new database with the user-inputed name
            dbTools.createNewDB(values["NewDatabaseName"], 1)
           
            # update the game saves listbox in the MainMenu
            window.FindElement('GameSavesListBox').Update(values = findGamePaths())
            
            # update the database listbox in the EditMenu
            window.FindElement('DataBaseListBox').Update(values = findGamePaths())
    
    # selects the room that will be edited
    elif(event == 'SelectRoom'):
        if(values['RoomSelectorListBox']):            
            # get the information for the selected room
            data = dbTools.getRoomData(editorSave, values["RoomSelectorListBox"][0])
            roomData = data[0]
            connectionsData = data[1]
            
            # display the data of the selected room
            window.FindElement('RoomIdText').Update(value = roomData[0])
            window.FindElement('RoomNameInput').Update(value = roomData[1])
            window.FindElement('RoomDescriptionInput').Update(value = roomData[2])
            
            window.FindElement('NorthConnectionInput').Update(value = connectionsData[0])
            window.FindElement('EastConnectionInput').Update(value = connectionsData[1])
            window.FindElement('SouthConnectionInput').Update(value = connectionsData[2])
            window.FindElement('WestConnectionInput').Update(value = connectionsData[3])
    
    # creates a new room
    elif(event == 'CreateNewRoom'):
        # create the new room in the current database
        dbTools.createNewRoom(editorSave)
        
        # update the level info room selector listbox
        editorLevelInfo = dbTools.getLevelInfo(editorSave)
        window.FindElement('RoomSelectorListBox').Update(values = list(editorLevelInfo.keys())[:-1])
    
    # saves the any changes to the  selected room to the database 
    elif(event == 'SubmitChanges'):
        
        # find the id of the edited room
        roomId = window.FindElement('RoomIdText').get()
        if(not roomId == 'id'):
            # store the edited room name and description
            roomData = {
                'room_name' : values['RoomNameInput'],
                'room_description' : values['RoomDescriptionInput']
                         }
            # store the values in the rooms table
            db.update(f'GameFiles/{editorSave}', 'rooms', roomData, ('id', roomId))
            
            # set the connections data values to default to 0
            connecitonsData = {
                'N':0,
                'E':0,
                'S':0,
                'W':0
                }
            # for each of the directions
            for direction in ['North', 'East', 'South', 'West']:
                # if the value for a given direction is an integer and not larger than the amount of rooms or negative
                # save it to connectionsData
                try:
                    connecitonsData[direction[0]] = int(values[f'{direction}ConnectionInput'])
                    
                    if(connecitonsData[direction[0]] > editorLevelInfo['AmountOfRooms'] or connecitonsData[direction[0]] < 0):
                        raise ValueError
                # otherwise save 0 to connectionsData
                except ValueError:
                    connecitonsData[direction[0]] = 0
 
            # store the values in the connections table        
            db.update(f'GameFiles/{editorSave}', 'connections', connecitonsData, ('id', roomId))
            time.sleep(0.5)

            # redisplay the connections for the selected room
            # if the player inputted  -21 then 0 would be stored
            # we need to update the values to reflect  what was actually  saved to the database
            temp = dbTools.getRoomData(editorSave, roomId)[1]  
            window.FindElement(f'NorthConnectionInput').Update(value = temp[0])
            window.FindElement(f'EastConnectionInput').Update(value = temp[1])
            window.FindElement(f'SouthConnectionInput').Update(value = temp[2])
            window.FindElement(f'WestConnectionInput').Update(value = temp[3])
    
    # takes you back to the previous menu 
    elif(str(event)[:4] == 'Back'):
        newWindow = goBackTo(currentWindow)
        changeWindow(newWindow)
        
    # break the loop and close the window
    elif(event == sg.WINDOW_CLOSED):
        break
        
window.close()