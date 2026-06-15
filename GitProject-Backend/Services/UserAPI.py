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
from .auth import Auth
from fastapi import Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()
load_dotenv(Path(__file__).resolve().parent.parent / '.env')

#65eddc2848ee5d537baaae50826639ad0151a6cd

router = APIRouter()
auth = Auth()

#--Utility--#
def get_cred(cred = Depends(security)):
    token = cred.credentials
    print("cred: ", token)
    user_id = auth.verify(token)
    return user_id

@router.get("/user")
async def get_user_data(user_id :str = Depends(get_cred)):
    try:
        return await get_user(user_id)

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
        encoded = auth.encode({"token": user.user_id})
        print("LOG>> User login success...")
        return {"message": "User logged in...", "jwt": encoded}
    except Exception as err:
        print(f"ERR> Error: {err}")
        return
    