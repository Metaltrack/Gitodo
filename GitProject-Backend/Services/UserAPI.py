from ast import Await
from datetime import datetime, timedelta
from pathlib import Path
import secrets
from urllib import response
from fastapi import FastAPI, APIRouter, HTTPException
import os
from dotenv import load_dotenv
from Models.user import User
from .database import DataBase
from Services import database
from .auth import Auth
from fastapi import Depends
from fastapi.security import HTTPBearer
import httpx

security = HTTPBearer()
load_dotenv(Path(__file__).resolve().parent.parent / '.env')

router = APIRouter()
auth = Auth()
db = DataBase()

#--Utility--#
def get_cred(cred = Depends(security)):
    token = cred.credentials
    print("cred: ", token)
    user_id = auth.verify(token)
    return user_id


#---------Functions----------#
async def get_user_data(user_id :int = Depends(get_cred)):
    try:
        print("ID from frontend: ", user_id)
        return await db.get_user(user_id)

    except Exception as err:
        print(f"ERR> Error sending user data: {err}")
        return HTTPException(status_code=404, detail="User not found...")



async def user_login(code :str):
    #get access token from here
    try:
        print("LOG>> User trying to login...")
        url = "https://github.com/login/oauth/access_token"
        params = {"client_id": os.getenv("CLIENT_ID"), "client_secret": os.getenv("CLIENT_SECRET"), "code": code}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers={"Accept": "application/json"})
        #response = requests.post(url, data=params, headers={"Accept": "application/json"})

        token = response.json()["access_token"]

        #get_user_data(token)
        
        user = User(token)
        await db.add_user_data(user)

        #create JWT here
        encoded = auth.encode({
            "sub": str(user.user_id),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=1.0)
        })
        print("LOG>> User login success...")
        return {"message": "User logged in...", "jwt": encoded}
    except Exception as err:
        print(f"ERR> Error: {err}")
        return



#---------ROUTES-------------#
@router.get("/user")
async def get_user(user_id :str = Depends(get_cred)):
    return await get_user_data(user_id)

@router.get("/user-login")
async def login(code :str):
    return await user_login(code)
    