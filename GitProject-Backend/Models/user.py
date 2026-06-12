from Models.repo import Repo
import requests

class User():
    user_id :int
    access_token :str
    user_name :str
    user_url :str
    user_html_url :str
    user_repo_url :str
    repo_list :Repo = []

    def __init__(self, code :str):
        try:
            url = "https://api.github.com/user"
            params = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {code}"}

            response = requests.get(url, headers=params)
            data = response.json()

            self.user_id = data["id"]
            self.access_token = code
            self.user_name = data["name"]
            self.user_url = data["url"]
            self.user_html_url = data["html_url"]
            self.user_repo_url = data["repos_url"]

            print(f"LOG> User Created >>\n ID: {self.user_id}\n NAME: {self.user_name}")

        except Exception as err:
            print(f"ERR> Error: {err}")
            return
