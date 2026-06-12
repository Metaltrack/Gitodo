from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from Services import UserAPI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserAPI.router, prefix="/user-api")

@app.get("/")
def init():
    return {"message": "Connection success!!"} #initialize services here

@app.get("/status")
def status():
    return {"message": "Good good.."} #change to real system check later

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4067)
