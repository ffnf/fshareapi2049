#README: https://github.com/ffnf/fshareapi2049
import requests
import json
import sys
import os

input_links = sys.argv[1]

USER_AGENT = ""
EMAIL = ""
PASSWORD = ""
APP_KEY = ""


def get_folder(user_agent, session_id, token, folderurl):
    try:
        response = requests.post(
            url="https://api.fshare.vn/api/fileops/getFolderList",
            headers={
                "Accept": "application/json",
                "User-Agent": user_agent,
                "Cookie": "session_id=" + session_id,
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "token": token,
                "pageIndex": 0,
                "url": folderurl,
                "dirOnly": 0,
                "limit": 60
            })
        )
        data = json.loads(response.content)

        for item in data:
            furl = item['furl']
            # ftitle = item['ftitle']
            # print(f"furl: {furl}")
            # print(f"ftitle: {ftitle}")
            print(furl)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

def download_url(user_agent, session_id, token, fshare_link):
    download_url = "https://api.fshare.vn/api/session/download"
    download_headers = {
        "User-Agent": user_agent,
        "Cookie": f"session_id={session_id}",
        "Content-Type": "application/json"
    }
    download_data = {
        "url": fshare_link,
        "password": "",
        "token": token,
        "zipflag": 0
    }

    download_response = requests.post(download_url, headers=download_headers, data=json.dumps(download_data))

    if download_response.status_code == 200:
        prefix = 'aria2c '
        download_link = prefix + download_response.json().get("location")
        print(download_link)
    else:
        print(f"Failed to get the download link for {fshare_link}")

def login(user_email, password, app_key, user_agent):
    login_url = "https://api.fshare.vn/api/user/login"
    credentials = {
        "user_email": user_email,
        "password": password,
        "app_key": app_key
    }
    login_headers = {
        "User-Agent": user_agent,
        "Content-Type": "application/json"
    }

    login_response = requests.post(login_url, headers=login_headers, data=json.dumps(credentials))

    if login_response.status_code == 200:
        response_data = login_response.json()
        token = response_data.get('token')
        session_id = response_data.get('session_id')
        return token, session_id
    else:
        print("Failed to authenticate")
        return None, None

def check_token_validity(user_agent, session_id):
    check_url = "https://api.fshare.vn/api/user/get"
    check_headers = {
        "accept": "application/json",
        "User-Agent": user_agent,
        "Cookie": f"session_id={session_id}"
    }

    check_response = requests.get(check_url, headers=check_headers)
    if check_response.status_code == 201:
        response_data = check_response.json()
        if response_data.get('msg') == "Not logged in yet!":
            return False
    return True


links_array = []

links_array = input_links.split("\n")

FSHARE_LINKS = [link.strip() for link in links_array if link.strip()]

# Fshare account credentials
user_email = EMAIL
password = PASSWORD
app_key = APP_KEY
user_agent = USER_AGENT

# Read token and session_id from "fstoken.txt" file
token = None
session_id = None

current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "fstoken.txt")

try:
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            token = lines[0].strip()
            session_id = lines[1].strip()
except FileNotFoundError:
    pass

# Check if token and session_id are valid
if token and session_id and check_token_validity(user_agent, session_id):
    print("token and session_id are valid")

else:
    print("token and session_id are invalid or not found, authenticate again")

    # If token and session_id are invalid or not found, authenticate again
    token, session_id = login(user_email, password, app_key, user_agent)

    # Check if authentication was successful
    if token and session_id:
        # Save the new token and session_id to "fstoken.txt" file
        try:
            with open(file_path, 'w') as file:
                file.write(token + '\n')
                file.write(session_id + '\n')
        except IOError as e:
            print("An IOError occurred:", str(e))
            print("Failed to update token and session_id in 'fstoken.txt'")
        print("Authentication successful")
    else:
        print("Failed to authenticate")


if len(sys.argv) > 1 and sys.argv[1] == "-f":
    get_folder(user_agent, session_id, token, sys.argv[2])
else:
    for fshare_link in FSHARE_LINKS:
        download_url(user_agent, session_id, token, fshare_link)
