import requests
import base64

def get_github_file_content(repo_url, file_path, access_token=None):
    # Construct the API URL
    api_url = f"https://api.github.com/repos/{repo_url}/contents/{file_path}"

    # Add authentication if required
    headers = {}
    if access_token:
        headers['Authorization'] = f"token {access_token}"

    # Send a GET request to the GitHub API
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        content = base64.b64decode(data['content']).decode('utf-8')
        return content
    else:
        return None  # Handle errors appropriately

# Example usage
repo_url = "https://github.com/guzzle/guzzle"
# file_path = "path/to/file.txt"
file_path = "docs/conf.py"
access_token = "your_github_access_token"  # If accessing a private repo
content = get_github_file_content(repo_url, file_path, access_token)
if content:
    print(content)
else:
    print("File not found or an error occurred.")
