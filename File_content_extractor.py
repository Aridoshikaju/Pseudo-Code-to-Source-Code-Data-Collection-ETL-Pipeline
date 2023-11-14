import subprocess
import json

def fetch_file_content(repo_owner, repo_name, file_path, branch='master'):
    raw_url = f"https://github.com/{repo_owner}/{repo_name}/blob/{branch}/{file_path}"
    
    try:
        # Run the curl command to fetch the file content
        response = subprocess.check_output(['curl', '-L', raw_url], text=True)
        return response
    except subprocess.CalledProcessError as e:
        print(f"Error executing curl command: {e}")
        return None

def parse_content(content):
    try:
        # Parse the JSON response
        json_response = json.loads(content)
        
        # Extract raw lines from the response
        raw_lines = json_response.get("payload", {}).get("blob", {}).get("rawLines", [])
        
        return raw_lines
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

if __name__ == "__main__":
    # Replace these with your actual values
    repo_owner = "Aridoshikaju"
    repo_name = "Pseudo-Code-to-Source-Code-Data-Collection-ETL-Pipeline"
    file_path = "dam.py"
    
    # Fetch file content
    file_content = fetch_file_content(repo_owner, repo_name, file_path)

    # Parse content if needed
    raw_lines = parse_content(file_content)

    file_content = """"""

    for line in raw_lines:
        file_content = file_content + line + "\n"
    
    print(file_content)

    # # Print or use raw lines as needed
    # if raw_lines:
    #     print("Raw Lines:")
    #     for line in raw_lines:
    #         print(line)
    # else:
    #     print("Failed to fetch or parse file content.")
