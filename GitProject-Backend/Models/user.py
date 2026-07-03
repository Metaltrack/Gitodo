from httpx import request
from Utility.logger import log, log_level
from Models.repo import Repo
import requests

class User():
    user_id :int
    access_token :str 
    user_name :str
    user_url :str 
    user_html_url :str
    user_repo_url :str

    def __init__(self, code :str):
        try:
            url = "https://api.github.com/user"
            params = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {code}"}

            response = requests.get(url, headers=params)
            data = response.json()

            self.user_id = data["id"]
            self.access_token = code
            self.user_name = data["name"] or data["login"]
            self.user_url = data["url"]
            self.user_html_url = data["html_url"]
            self.user_repo_url = data["repos_url"]
            self.repo_list :list[Repo] = []

            log(log_level.INFO, __file__, f"User Created >> ID: {self.user_id} | NAME: {self.user_name}")

        except Exception as err:
            log(log_level.ERROR, __file__, f"User Constructor '{err}'")
            return
