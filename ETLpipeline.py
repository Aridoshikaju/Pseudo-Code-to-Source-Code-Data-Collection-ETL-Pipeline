import sqlite3
import threading
# import requests

""" 
3 rows 
Pesudo Code
Sentence Code
Complete Code
"""


class RowData:
    #all the information of a row
    def __init__(self,language : str, url : str, path : str) -> None:
        #logic to traverse the row are aquire the required data only
        self.language = language
        self.url = url
        self.path = path
        self.branch = None
        self.completeCode = None
        self.sentenceCode = None
        self.pesudoCode = None

def connectDataBase():
    db_file = "mydatabase.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    return cursor

def newRowObj(row) -> RowData:
    #logic to traverse the row and return a RowData object
    language = "python"
    url = "link"
    path = "file name included"
    row = RowData(language, url, path)
    return row

def attachBranch(row) -> None:
    #this will use the gitHub repo page to get the default branch which will be furthur used to create the URL
    pass

def getCompleteCodeFromGithub(row : RowData) -> None:
    #This will extract and attach the complete code from gitHub to the object
    pass

def attachPesudoCodes(row : RowData) -> None:
     #this will use the g4f model and attach the sentence and normal pesudo code to the row object
     pass

def tranform(row : RowData):
    #Thread Executed
        #the thread will first get data from gitHub and then use the g4f model to prepare the remaining columns
        #store the data in the object
        #only the transformation logic and nothing else
        attachBranch(row)
        getCompleteCodeFromGithub(row)
        attachPesudoCodes(row)

def store():
    #Thread Executed
        #convert the row into a binary and save it
        pass

def processRow(currentRow) -> None:
    tranform(currentRow)
    store(currentRow)


#extract
#extract each row and assign the work to a thread

#DataBase Connection

def fetchAndProcessRows():
    cursor = connectDataBase()
    row = cursor.fetchone()
    while row is not None:
        currentRow = newRowObj(row)
        # Create a new thread for processing the current row
        thread = threading.Thread(target=processRow, args=(currentRow,))
        # Start the thread
        thread.start()
        row = cursor.fetchone()

if __name__ == '__main__':
    fetchAndProcessRows()


