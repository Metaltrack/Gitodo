from ast import Await
from pathlib import Path
import secrets
from urllib import response
from fastapi import FastAPI, APIRouter
import requests
import os
from dotenv import load_dotenv
from Models.user import User
from .database import add_user_data, get_user
from Services import database
import jwt

load_dotenv(Path(__file__).resolve().parent.parent / '.env')

#65eddc2848ee5d537baaae50826639ad0151a6cd

router = APIRouter()

#test-route only
@router.get("/user-git-data")
def get_user_github_data(code :str):
    try:
        url = "https://api.github.com/user"
        params = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {code}"}

        response = requests.get(url, headers=params)
        
    except Exception as err:
        print(f"ERR> Error: {err}")
        return

@router.get("/user")
async def get_user_data(jwt_token :str):
    try:
        token = jwt.decode(jwt_token, os.getenv("JWT_SECRET"), algorithms="HS256")
        user_id = token["token"]

        return get_user(user_id)

    except Exception as err:
        print(f"ERR> Error sending user data: {err}")
        return

@router.get("/user-login")
async def user_login(code :str):
    #get access token from here
    try:
        print("LOG>> User trying to login...")
        url = "https://github.com/login/oauth/access_token"
        params = {"client_id": os.getenv("CLIENT_ID"), "client_secret": os.getenv("CLIENT_SECRET"), "code": code}

        response = requests.post(url, data=params, headers={"Accept": "application/json"})

        token = response.json()["access_token"]

        #get_user_data(token)
        
        user = User(token)
        await add_user_data(user)

        #create JWT here
        encoded = jwt.encode({"token": user.user_id}, os.getenv("JWT_SECRET"), algorithm="HS256")
        print("LOG>> User login success...")
        return {"message": "User logged in...", "jwt": encoded}
    except Exception as err:
        print(f"ERR> Error: {err}")
        return
    