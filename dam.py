import subprocess

# Replace these with your actual values
repo_owner = "guzzle"
repo_name = "guzzle"

# URL of the GitHub repository page
repo_url = "https://github.com/{repo_owner}/{repo_name}"

# Run the curl command to fetch the HTML content and follow redirects (-L option)
try:
    html_content = subprocess.check_output(['curl', '-L', repo_url], text=True)
except subprocess.CalledProcessError as e:
    print(f"Error executing curl command: {e}")
    html_content = None

print(html_content)

if html_content:
    # Continue with processing the HTML content
    from bs4 import BeautifulSoup

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the element containing the default branch name
    branch_element = soup.find("span", class_="css-truncate-target")

    if branch_element:
        default_branch = branch_element.text.strip()
        print("Default Branch:", default_branch)
    else:
        print("Failed to find the default branch element in the HTML content.")
else:
    print("HTML content not available.")