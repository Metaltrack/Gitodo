from fastapi import HTTPException
import jwt
from dotenv import load_dotenv
import os
from ast import Await
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / '.env')

class Auth():
    secret = os.getenv("JWT_SECRET")
    algorithm = "HS256"

    def encode(self, token :dict[str, any]):
        return jwt.encode(token, self.secret, algorithm=self.algorithm)

    def decode(self, token :str):
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])

    def verify(self, token :str):
        try:
            return self.decode(token)["sub"]
        except jwt.InvalidTokenError as err:
            print(f"ERR> Error verifying JWT: {err}")
            raise HTTPException(status_code=401, detail="Invalid JWT")
