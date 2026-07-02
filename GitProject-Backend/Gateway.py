from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from Services import UserAPI
from Services.database import DataBase
from Utility.logger import log, log_level

app = FastAPI()
allow_list = [
        "*"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserAPI.router, prefix="/user-api")

@app.get("/")
async def init():
    try:
        db = DataBase()
        #check database
        if await db.client.address:
            log(log_level.INFO, __file__, f"Database Response {await db.client.address}")
        else:
            log
            for tries in range(3):
                db = DataBase()
                if await db.client.address:
                    log(log_level.INFO, __file__, f"Database Response {await db.client.address}")
                    break
                log(log_level.ERROR, __file__, f"Database did not respond...")
            if tries >= 3:
                log()
    except Exception as err:
        raise Exception(err)


@app.get("/status")
def status():
    return {"message": "Good good.."} #change to real system check later

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4067)
