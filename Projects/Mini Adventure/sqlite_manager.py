import sqlite3
from sqlite3 import Error
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

def connectToDB(path):
    '''
  This function established a connection to a SQULite database
  
  A connection to a database at the given path will be established allowing you to
  query it. If no database exists at the given path one will be created.

  Parameters
  ----------
  path : str
    The path to the database you want to interact with. If no database exists then one
    will be created with this path.

  
  Returns
  -------
  Connection
    This is the connection object for the database. All queries get sent to it and changes get
    save to it.
    '''  
    connection = None
    
    # try to establish a connection with the database
    # if the database does not exist one will be created first
    try:
        connection = sqlite3.connect(path)

    except Error as e:
        logging.error(f'Connection Failed: {e} ')
        
    return connection


def queryDB(path, query):
    '''
  This function sends a query to the database.
  
  This function will execute a query to change the data stored in a database or to make new tables.
  This function cannot return data from the database.

  Parameters
  ----------
  path : str
    The path to the database you want to interact with. If no database exists then one
    will be created with this path.

  query : str
    

  Returns
  -------
  None
    '''
    # establish connection to the database
    connection = connectToDB(path)
    cursor = connection.cursor()
    
    # try to send a query to the database
    # save any changes to the database
    try:
        cursor.execute(query)
        connection.commit()
        
    except Error as e:
        logging.error(f'Query Failed: {e}')
    
    # end connection to the database
    connection.close()

def readDB(path, query):
    '''
  This function sends a query to the database and returns the info it read.
  
  This function will execute a query to read data from the database. This function cannot
  make changes to the database.

  Parameters
  ----------
  path : str
    The path to the database you want to interact with. If no database exists then one
    will be created with this path.

  query : str
    The query that will be executed. This can be SELECT.

  Returns
  -------
  tuple<tuple>
    The data that has been collected from the database
    '''
    # establish connection to the database
    connection = connectToDB(path)
    cursor = connection.cursor()
    
    results = ()
    # try to query the database and read the results of the query
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
    except Error as e:
        logging.error(f'Read Query Failed: {e}')
        
    # end the connection to the database and return the results
    connection.close()
    return results 

def createTable(path, name, columns):
    '''
  This function generates and executes a CREATE TABLE query to a database.
  
  This function will generate a new table in an exsisting database or a new one with the required columns. 

  Parameters
  ----------
  path : str
    The path to the database you want to interact with. If no database exists then one
    will be created with this path.

  name : str
    The name of the table
    
  columns : dict<str, str>
    The names of the columns that will be in the new table paired with the type of data that they will store.

  Returns
  -------
  None
    '''
    # initializes the beggining of the CREATE TABLE query
    # this inclues the table name and a primary key column
    query = f'''CREATE TABLE IF NOT EXISTS {name} ('id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, '''
    
    # Add the rest of the desired columns to the query
    for key in columns:
        query += f'{key} {columns[key]},'
    
    query = f'{query[:-1]})'
    
    # Create the table
    queryDB(path, query)

def insert(path, table, columns, values):
    '''
  This function generates and executes an INSERT query to a database.
  
  This function will insert data into new rows of an existing table. This function cannot update existing rows.   

  Parameters
  ----------
  path : str
    The path to the database you want to interact with. If no database exists then one
    will be created with this path.

  table : str
    The name of the table that the data will be inserted into.
    
  columns : list<str>
    The names of the columns that will be given data.
    
  values : list<list<str>>
    The data that will be stored. Each of the innermost lists contains the information for a new row.

  Returns
  -------
  None
    '''
    # initializes the beggining of the INSERT query
    query = f'''INSERT INTO {table} ('''
    
    # add the columns that will recive data
    for columnName in columns:
        query += f'{columnName},'
    query = f'{query[:-1]})'
    
    # add the values for each row that will be inserted into the database
    query += '\nVALUES '
    for row in values:
        
        query += '('
        for value in row:
            query += f'{value},'
        query = f'{query[:-1]}),'
     
    query = f'{query[:-1]};'
    
    # insert the data into the database
    queryDB(path, query)
    
def select(path, table, columns, row):
    '''
  This function generates and executes a SELECT query to a database.
  
  This function select rows from a table and returns their the data stored in the specified columns. 

  Parameters
  ----------
  path : str
    The path to the database you want to interact with. If no database exists then one
    will be created with this path.

  table : str
    The name of the table that the data will be selected from.
    
  columns : list<str>
    The names of the columns that will be read.
    
  rows : tuple
    This is the conditional statment that will be used to select the rows.
    if rows[0] is equal to rows[1] then the row will be selected.

  Returns
  -------
  list<tuple>
    The data that has been collected from the database
    ''' 
    # initializes the beggining of the SELECT query
    query = '''SELECT '''
    
    # add the columns that you want information from
    for column in columns:
        query += f'{column},'
    # add the table you are getting information from    
    query = f'{query[:-1]} FROM {table}'
    
    # add the row condition if there is any
    # if row is == None all the rows in the table will be selected
    if (not row == None):
        query += f' WHERE {row[0]} = {row[1]}'
    
    # return the data retreved from the database
    return readDB(path, query)

def update(path, table, values, row):
    '''
  This function generates and executes an UPDATE query to a database.
  
  This function will update data into existing rows of an existing table. This function cannot make new rows.   

  

  Parameters
  ----------
  path : str
    The path to the database you want to interact with. If no database exists then one
    will be created with this path.

  table : str
    The name of the table where the data will be updated.
    
  values : dict
    The data that will be updated. The key will be the column name and the value will be the new value to store in it.

  rows : tuple
    This is the conditional statment that will be used to select the rows.
    if rows[0] is equal to rows[1] then the row will be selected.
    
  Returns
  -------
  None
    '''
    # initializes the beggining of the UPDATE query
    query = f'''UPDATE {table} SET '''
    
    # add the columns that will be changed as well as their new values
    for value in values:
        query += f'{value}="{values[value]}",'
    
    # add the conditional that determins what row will be updated.
    query = f'{query[:-1]} WHERE {row[0]} = {row[1]};'

    # update the database
    queryDB(path, query)