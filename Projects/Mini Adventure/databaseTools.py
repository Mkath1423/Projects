import sqlite_manager as db

def createNewDB(database, rooms):
    '''
  This function initializes a new database.
  
  A new gameSave database will be created with the required tables. rooms number of
  stock rooms then get inserted into the database. The database name also gets added to the
  gameFilePaths.txt file.

  Parameters
  ----------
  database : str
    This is the name of the database you want to create
    
  rooms : int
    this is the number of rooms you want in the new database
    
  Returns
  -------
  None
    '''
    # add the new gameSave path to the gameFilePaths.txt file
    gameFilePaths = open('GameFiles/gameFilePaths.txt', 'a')
    gameFilePaths.write(f',{database}')
    gameFilePaths.close()
    
    # set what columns should be in the rooms table and what datatype they contain
    rooms_columns = {
        'room_name' : 'TEXT',
        'room_description ': 'TEXT'
        }
    # create the rooms table
    db.createTable(f'GameFiles/{database}', 'rooms', rooms_columns)
    
    # set what columns should be in the connections table and what datatype they contain 
    connections_colums = {
        'N':'INTEGER',
        'E':'INTEGER',
        'S':'INTEGER',
        'W':'INTEGER'
        }
    # create the connections table
    db.createTable(f'GameFiles/{database}', 'connections', connections_colums)
    
    # insert rooms amount of stock rooms into the tables
    for i in range(rooms):
        createNewRoom(database)


def createNewRoom(database):
    '''
  This function inserts a new room in a database.
  
  A new stock room gets made in the specified database. The values for the rooms are:
  
  room_name = newRoomName
  room_discripton = newRoomDescription
  
  N = 0
  E = 0
  S = 0
  W = 0

  Parameters
  ----------
  database : str
    This is the name of the database you want to insert rooms into.
    
  Returns
  -------
  None
    '''
    # insert a new row into the rooms table with stock values
    db.insert(f'GameFiles/{database}', 'rooms', ['room_name', 'room_description '], [['"newRoomName"', '"newRoomDescription "']])
    
    # insert a new row into the connections table with stock values
    db.insert(f'GameFiles/{database}', 'connections', ['N', 'E', 'S', 'W'], [[0, 0, 0, 0]])
    
def getLevelInfo(database):
    '''
  This function gets and returns the names and ids of all the rooms in the database.
  
  A dictionary gets created and returned which contains the room ids as key and to room names as values.

  Parameters
  ----------
  database : str
    This is the name of the database you want to get information from.
    
  Returns
  -------
  dict<int, str>
    A dictionary of all the room ids and names in the database. The ids are keys and the names are values.
    '''  
    levelInfo = {}
    
    # query the database for the room name and id for every row
    roomsData = db.select(f'GameFiles/{database}', 'rooms', ['id', 'room_name'], None)
    
    # parse roomsData into a dictionary
    for room in roomsData:
        levelInfo[room[0]] = room[1]
    
    # add the amount of rooms to dictionary
    levelInfo['AmountOfRooms'] = len(levelInfo)
    
    # return the dictionary
    return levelInfo

def getRoomData(database, room):
    '''
  This function gets and returns the data stored for a given room.
  
  The room name, room description  and all 4 connections will be returned.

  Parameters
  ----------
  database : str
    This is the name of the database you want to get information from.
    
  room : int
    This is the id of the room you want to get the data of.
    
  Returns
  -------
  list<list<str>>
    All the information for the given room.
    Index 0 contains the room_name and the room_description .
    Index 1 contains the 4 connections in order [North, East, South, West]
    '''
    # query the database for the room id name and descripton
    room_data = db.select(f'GameFiles/{database}', 'rooms', ['id', 'room_name', 'room_description '], ('id', room))[0]
    
    # query the database for the rooms it connects to
    connections_data = db.select(f'GameFiles/{database}', 'connections', ['N', 'E', 'S', 'W'], ('id', room))[0]
    
    # return the collected data
    return (room_data, connections_data)

