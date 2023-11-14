import sqlite3
import threading
import subprocess
from bs4 import BeautifulSoup
# import requests

""" 
3 rows 
Pesudo Code
Sentence Code
Complete Code
"""


class RowData:
    #all the information of a row
    def __init__(self,language : str, url : str, filePath : str, repoName : str, repoOwner : str) -> None:
        #logic to traverse the row are aquire the required data only
        self.language = language
        self.url = url
        self.filePath = filePath
        self.repoName = repoName
        self.repoOwner = repoOwner
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
    # language = "python"
    # github_repo_url = "link"
    # filePath = "file name included"
    # repoName = "some"
    # repoOwner = "some"
    id, snippet, language, repo_file_name, github_repo_url, license, commit_hash, starting_line_number, chunk_size = row
    repoOwner, repoName, filePath = repo_file_name.split("/", 2)
    row = RowData(language, github_repo_url, filePath, repoName, repoOwner)
    return row

def attachBranch(row : RowData) -> None:
    #this will use the gitHub repo page to get the default branch which will be furthur used to create the URL
    try:
        html_content = subprocess.check_output(['curl', '-L', row.url], text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing curl command: {e}")
        html_content = None
    if html_content:
    # Continue with processing the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the <summary> element with the specified class and attributes
        summary_element = soup.find("summary", class_="btn css-truncate", attrs={"data-hotkey": "w", "title": "Switch branches or tags"})

        if summary_element:
            # Get the text inside the <span class="css-truncate-target" data-menu-button>
            version_text = summary_element.find("span", class_="css-truncate-target", attrs={"data-menu-button": True}).text.strip()
    row.branch = version_text
    

def getCompleteCodeFromGithub(row : RowData) -> None:
    #This will extract and attach the complete code from gitHub to the object
    reqUrl = "http://localhost:8080/getFile"  # Change the URL if your server is hosted elsewhere
    params = {
        "repoOwner": row.repoOwner,   # Replace with your GitHub username
        "repoName": row.repoName,    # Replace with the GitHub repository name
        "filePath": row.filePath,  # Replace with the file path you want to access
        "branch" : row.branch
        #"accessToken": "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"  # Replace with your GitHub access token (if needed)
    }
    response = requests.get(reqUrl, params=params)
    if response.status_code == 200:
        #take it to the next levels
        response_data = response.json()
        file_content = response_data.get("content")
        # row.completeCode = """{file_content}"""
        row.completeCode = f'{{"completeCode": """{file_content}"""}}'
    else:
        #save the repo name to file and end 
        pass
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

def processRow(row) -> None:
    #createt the row object with all the properties
    currentRow = newRowObj(row)
    tranform(currentRow)
    store(currentRow)


#extract
#extract each row and assign the work to a thread

#DataBase Connection

def fetchAndProcessRows():
    cursor = connectDataBase()
    row = cursor.fetchone()
    while row is not None:
        # currentRow = newRowObj(row)
        # Create a new thread for processing the current row
        thread = threading.Thread(target=processRow, args=(row,))
        # Start the thread
        thread.start()
        row = cursor.fetchone()

if __name__ == '__main__':
    fetchAndProcessRows()