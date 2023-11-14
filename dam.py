import subprocess
from bs4 import BeautifulSoup

# Replace these with your actual values
repo_owner = "guzzle"
repo_name = "guzzle"

# URL of the GitHub repository page
repo_url = f"https://github.com/{repo_owner}/{repo_name}"
# repo_url = "https://github.com/Aridoshikaju/Pseudo-Code-to-Source-Code-Data-Collection-ETL-Pipeline"

# Run the curl command to fetch the HTML content and follow redirects (-L option)
try:
    html_content = subprocess.check_output(['curl', '-L', repo_url], text=True)
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
        print("Version:", version_text)
    else:
        print("Failed to find the summary element in the HTML content.")
else:
    print("HTML content not available.")
