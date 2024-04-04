import requests
import base64

def get_file_content_from_github(owner, repo, path):

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)
    if response.status_code == 200:
        content = response.json()['content']
        return base64.b64decode(content).decode('utf-8')
    else:
        print("Failed to fetch file content from GitHub:", response.status_code)
        return None

def list_files_in_repo(owner, repo, path, keyword):

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)
    files = []
    if response.status_code == 200:
        for item in response.json():
            if item['type'] == 'file' and keyword.lower() in item['path'].lower():
                files.append(item['path'])
            elif item['type'] == 'dir':
                files.extend(list_files_in_repo(owner, repo, item['path'], keyword))  
    else:
        print("Failed to list files in GitHub:", response.status_code)
    return files


owner = "quanta-Irenelin"
repo = "openbmc"
path = ""  
keyword = "FRU"

fru_files = list_files_in_repo(owner, repo, path, keyword)

for fru_file in fru_files:
    print(f"Fetching content of: {fru_file}")
    content = get_file_content_from_github(owner, repo, fru_file)
    if content:
        print(content[:500], "...")  
    else:
        print("No content found or error fetching the file.")

