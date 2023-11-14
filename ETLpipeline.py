import sqlite3
import threading
import subprocess
from bs4 import BeautifulSoup
import json
# import requests

""" 
4 rows 
actual code
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

def fetchBranchPage(url) -> None:
    try:
        response = subprocess.check_output(['curl', '-L', url], text=True)
        return response
    except subprocess.CalledProcessError as e:
        print(f"Error executing curl command: {e}")
        return None

def parseForBranch(html_content):
    try:
        if html_content:
        # Continue with processing the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the <summary> element with the specified class and attributes
            summary_element = soup.find("summary", class_="btn css-truncate", attrs={"data-hotkey": "w", "title": "Switch branches or tags"})

            if summary_element:
                # Get the text inside the <span class="css-truncate-target" data-menu-button>
                version_text = summary_element.find("span", class_="css-truncate-target", attrs={"data-menu-button": True}).text.strip()
                return version_text
        return "master"
    except:
        return "master"

def attachBranch(row : RowData) -> None:
    #this will use the gitHub repo page to get the default branch which will be furthur used to create the URL
    pageConent = fetchBranchPage(row.url)
    branchVersion = parseForBranch(pageConent)
    row.branch = branchVersion

    
def fetchForFileContent(row : RowData):
    raw_url = f"https://github.com/{row.repoOwner}/{row.repoName}/blob/{row.branch}/{row.filePath}"
    try:
        # Run the curl command to fetch the file content
        response = subprocess.check_output(['curl', '-L', raw_url], text=True)
        return response
    except subprocess.CalledProcessError as e:
        print(f"Error executing curl command: {e}")
        return None

def parseForContent(content):
    try:
        # Parse the JSON response
        json_response = json.loads(content)
        
        # Extract raw lines from the response
        raw_lines = json_response.get("payload", {}).get("blob", {}).get("rawLines", [])
        
        return raw_lines
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

def getCompleteCodeFromGithub(row : RowData) -> None:
    #This will extract and attach the complete code from gitHub to the object
    fileContent = fetchForFileContent(row)
    rawLines = parseForContent(fileContent)
    file_content = """"""

    for line in rawLines:
        file_content = file_content + line + "\n"

    row.completeCode = fileContent

def attachPesudoCodes(row : RowData) -> None:
     #this will use the g4f model and attach the sentence and normal pesudo code to the row object
     #attach pesudo form
     #attach sentence form
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

    #the set must be laoded at the start of the program
    #check if file already processed with help of hashSet
    #thread safe methods need to be implemented for check and adding into it
    #the set creaeted must go beond the life cycle of the program
        #needs to be stored is some form
        #achiveable using try-expect
    
    """
        try:
            try to perform the tasks
        expect:
            close the binary file
            store the set in a file
    """

    #Tasks
    tranform(currentRow)
    store(currentRow)

    #after Storing, the row must be added to processed set


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