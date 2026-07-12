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
from Utility.logger import log, log_level

security = HTTPBearer()
load_dotenv(Path(__file__).resolve().parent.parent / '.env')

router = APIRouter()
auth = Auth()
db = DataBase()

#--Utility--#
def get_cred(cred = Depends(security)):
    token = cred.credentials
    log(log_level.INFO, "UserAPI.py", f"Credential: '{cred}'")
    user_id = auth.verify(token)
    return user_id


#---------Functions----------#
async def update_repos(repo_id :int, data :dict, user_id :int):
    try:
        log(log_level.INFO, "UserAPI.py", f"UserID from frontend: '{user_id}'")
        await db.update_repo(user_id, repo_id, data)
        return {"message": "Repo Updated"}
    except Exception as err:
        log(log_level.ERROR, "UserAPI.py", f"update_repos function '{err}'")
        raise RuntimeError(err)

async def get_user_data(user_id :int):
    try:
        log(log_level.INFO, "UserAPI.py", f"UserID from frontend: '{user_id}'")
        return await db.get_user(user_id)

    except Exception as err:
        log(log_level.ERROR, "UserAPI.py", f"get_user_data function '{err}'")
        return HTTPException(status_code=404, detail="User not found...")


#called for login
#code -> Recieved from After Github login page auth
async def user_login(code :str):
    #call github api to get access_token
    try:
        url = "https://github.com/login/oauth/access_token"
        params = {"client_id": os.getenv("CLIENT_ID"), "client_secret": os.getenv("CLIENT_SECRET"), "code": code}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers={"Accept": "application/json"})
        #response = requests.post(url, data=params, headers={"Accept": "application/json"})

        if response.status_code in range(100, 199):
            log(log_level.INFO, "UserAPI.py", f"Response code INFO '{response.status_code}'")
        elif response.status_code in range(200, 299):
            log(log_level.INFO, "UserAPI.py", f"Response code SUCCESS '{response.status_code}'")
        elif response.status_code in range(300, 399):
            log(log_level.ERROR, "UserAPI.py", f"Response code REDIRECTION '{response.status_code}'")
        elif response.status_code in range(400, 499):
            log(log_level.ERROR, "UserAPI.py", f"Response code CLIENT ERROR '{response.status_code}'")
        elif response.status_code in range(500, 599):
            log(log_level.ERROR, "UserAPI.py", f"Response code SERVER ERROR '{response.status_code}'")


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
        
        log(log_level.INFO, "UserAPI.py", f"User login successful...")
        return {"message": "User login success returning token...", "jwt": encoded}
    except Exception as err:
        log(log_level.ERROR, "UserAPI.py", f"User login Failed, user_login function '{err}'")
        return


async def get_user_repos(user_id :str = Depends(get_cred)):
    try:
        log(log_level.INFO, "UserAPI.py", f"UserID from frontend: '{user_id}'")
        return await db.get_repository(user_id)
    except Exception as err:
        log(log_level.ERROR, "UserAPI.py", f"get_user_repos function '{err}'")
        raise RuntimeError(err)


#---------ROUTES-------------#

#Here the user_id must be string for authentication
#while passing they will ans should be passed as int for database

#called when switched to dashboard
@router.get("/user")
async def get_user(user_id :str = Depends(get_cred)):
    log(log_level.INFO, "UserAPI.py", f"Request to get data for user '{user_id}'")
    return await get_user_data(user_id)

#called when User presses login button at main page
#code is recieved from Github and sent to this function
@router.get("/user-login")
async def login(code :str):
    log(log_level.INFO, "UserAPI.py", f"Request for login with code '{code}'")
    return await user_login(code)
    

#also called when switched to dashboard
#I did not use the get_user function cause then it would be too confusing if goes wrong
@router.get("/user-repos")
async def get_repos(user_id :str = Depends(get_cred)):
    log(log_level.INFO, "UserAPI.py", f"Request to get user repos '{user_id}'")
    return await get_user_repos(user_id)

#Called to update any part of the repos
@router.post("/user-update-repo/{repo_id}")
async def user_update_repo(repo_id :int, data :dict, user_id :str = Depends(get_cred)):
    log(log_level.INFO, "UserAPI.py", f"Request to update repo '{repo_id}' of User '{user_id}'")
    return await update_repos(repo_id, data, user_id)

