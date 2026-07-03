from Utility.logger import log, log_level
from pymongo import AsyncMongoClient
from Models.models import user_model, repo_model, task_model
from Models.user import User
from Models.repo import Repo
from Models.task import Task

class DataBase:
    def __init__(self):
        self.uri = "mongodb://localhost:27017/"
        self.client = AsyncMongoClient(self.uri)
        self.database = self.client["test_database"]
        self.collection = self.database["GitCollection"]

    async def get_user(self, user_id :int):
        try:
            query_filter = await self.collection.find_one({"user_id": int(user_id)})
            print("query_filter", query_filter)
            if not query_filter:
                print("ERR> User not found!!")
                return

            data = {
                    "name": query_filter["user_name"],
                    "html_url": query_filter["user_html_url"]
                }

            return data

        except Exception as err:
            print(f"ERR> Error getting user from database {err}")
            return


    async def add_user_data(self, user :User):
        try:
            query_filter = {"user_id": user.user_id}
            result = await self.collection.find_one(query_filter)
        
            if(result):
                log(log_level.INFO, __file__, f"User '{user.user_id}' already exists.. Updating user access token..")
                update = await self.collection.update_one(query_filter, {"$set":{"access_token":user.access_token}})
                return

            input_user = user_model(
            user_id=user.user_id,
            access_token=user.access_token,
            user_name=user.user_name,
            user_url=user.user_url,
            user_html_url=user.user_html_url,
            user_repo_url=user.user_repo_url,
            repo_list=[repo_model(
                    repo_id=r.repo_id,
                    repo_name=r.repo_name,
                    repo_url=r.repo_url,
                    repo_html_url=r.repo_html_url,
                    repo_commit_url=r.repo_commit_url,
                    repo_progress=r.repo_progress,
                    task_list=[task_model(
                        task_id=t.task_id,
                        task_name=t.task_name,
                        task_condition=t.task_condition,
                        task_completion=t.task_completion
                    ) for t in r.task_list]
                ) for r in user.repo_list]
            )

            result = await self.collection.insert_one(input_user.model_dump())
            log(log_level.INFO, __file__, f"Database performed query with result '{result.acknowledged}', added user '{result.inserted_id}'")

            index = await self.collection.create_index("user_id")
            log(log_level.INFO, __file__, f"Database performed query.. index created for user '{user.user_id}' -> '{index}'")
        except Exception as err:
            log(log_level.ERROR, __file__, f"Database failed to add user, add_user_data function '{err}'")

    async def delete_user(self, user :User):
        try:
            query_filter = {"user_id": user.user_id}
            result = await self.collection.delete_one(query_filter)
            print(result)
        except Exception as err:
            print(f"ERR>> Error removing user: {err}")
