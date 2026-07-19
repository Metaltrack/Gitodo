from multiprocessing import Value

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

#--User Queries--#
    async def get_repository(self, user_id :int):
        try:
            query_filter = await self.collection.find_one({"user_id": int(user_id)})

            if not query_filter:
                log(log_level.ERROR, "database.py", f"UserID '{user_id}' does not exist in Database...")
                return

            repo_arr = query_filter["repo_list"]

            data = [{"id": r["repo_id"],
                     "name": r["repo_name"],
                     "html_url": r["repo_html_url"],
                     "progress": r["repo_progress"],
                     "total_tasks": r["total_tasks"],
                     "completed_tasks": r["completed_tasks"],
                     "archived": r["repo_archived"],
                     "created_at": r["created_at"]
                } for r in repo_arr]

            return data

        except Exception as err:
            log(log_level.ERROR, "database.py", f"get_repos function '{err}'")
            raise RuntimeError(err)
            return

    async def get_user(self, user_id :int):
        try:
            query_filter = await self.collection.find_one({"user_id": int(user_id)})

            if not query_filter:
                log(log_level.ERROR, "database.py", f"UserID '{user_id}' does not exist in Database...")
                return

            data = {
                    "name": query_filter["user_name"],
                    "html_url": query_filter["user_html_url"]
                }

            return data

        except Exception as err:
            log(log_level.ERROR, "database.py", f"get_user function '{err}'")
            return


    async def add_user_data(self, user :User):
        try:
            query_filter = {"user_id": user.user_id}
            result = await self.collection.find_one(query_filter)

            if(result):
                log(log_level.INFO, "database.py", f"User '{user.user_id}' already exists.. Updating user access token..")
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
                        task_completion=t.task_completion,
                        dead_line=t.dead_line
                    ) for t in r.task_list],
                    source_list=[],
                    total_tasks=r.total_tasks,
                    completed_tasks=r.completed_tasks,
                    repo_archived=r.repo_archived,
                    created_at=r.created_at
                ) for r in user.repo_list]
            )

            result = await self.collection.insert_one(input_user.model_dump())
            log(log_level.INFO, "database.py", f"Database performed query with result '{result.acknowledged}', added user '{result.inserted_id}'")

            index = await self.collection.create_index("user_id")
            log(log_level.INFO, "database.py", f"Database performed query.. index created for user '{user.user_id}' -> '{index}'")
        except Exception as err:
            log(log_level.ERROR, "database.py", f"Database failed to add user, add_user_data function '{err}'")

    async def delete_user(self, user :User):
        try:
            query_filter = {"user_id": user.user_id}
            result = await self.collection.delete_one(query_filter)
            print(result)
        except Exception as err:
            print(f"ERR>> Error removing user: {err}")


#--Repo Queries--#
    async def update_repo(self, user_id :int, repo_id, data :dict):
        try:
            log(log_level.INFO, "database.py", f"Updating database userid '{user_id}'")

            query_filter = {"user_id": int(user_id)}
            result = await self.collection.find_one(query_filter)

            if not result:
                log(log_level.ERROR, "database.py", f"User '{user_id}' does not exist...")
                return None
            
            query_filter = {"user_id": int(user_id), "repo_list.repo_id": int(repo_id)}

            update_operation = {
                "$set": {
                    f"repo_list.$.{key}": value
                    for key, value in data.items()                 
                }   
            }

            result = await self.collection.update_one(query_filter, update_operation)
            log(log_level.INFO, "database.py", f"Database response '{result}'")
            log(log_level.INFO, "database.py", f"Repo '{repo_id}' of User '{user_id}' was updated with '{data}'")
        except Exception as err:
            log(log_level.CRITICAL, "database.py", f"update_repo function '{err}'")
            raise RuntimeError(err)

    async def repo_data(self, user_id :int, repo_id :int):
        try:
            log(log_level.INFO, "database.py", f"Getting repo data from RepoID '{repo_id}' of User '{user_id}'")

            query_filter = {"user_id": int(user_id)}
            result = await self.collection.find_one(query_filter)

            if not result:
                log(log_level.ERROR, "database.py", f"User '{user_id}' does not exist...")
                return None

            query_filter = {"user_id": int(user_id), "repo_list.repo_id": int(repo_id)}

            repo_data = await self.collection.find_one(query_filter)

            repo = next(r for r in repo_data["repo_list"] if r["repo_id"] == int(repo_id))

            data = {
                "id": repo["repo_id"],
                "name": repo["repo_name"],
                "html_url": repo["repo_html_url"],
                "progress": repo["repo_progress"],
                "total_tasks": repo["total_tasks"],
                "completed_task": repo["completed_tasks"],
                "archived": repo["repo_archived"],
                "created_at": repo["created_at"],
            }

            return data
        except Exception as err:
            log(log_level.ERROR, "database.py", f"repo_data function '{err}'")
            raise RuntimeError(err)


#--Task Queries--#

    async def task_data(self, user_id :int, repo_id :int):
        try:
            log(log_level.INFO, "database.py", f"Getting repo data from RepoID '{repo_id}' of User '{user_id}'")

            query_filter = {"user_id": int(user_id)}
            result = await self.collection.find_one(query_filter)

            if not result:
                log(log_level.ERROR, "database.py", f"User '{user_id}' does not exist...")
                return None
            
            query_filter = {"user_id": int(user_id), "repo_list.repo_id": int(repo_id)}
            user = await self.collection.find_one(query_filter)

            repo = next(r for r in user["repo_list"] if r["repo_id"] == repo_id)

            tasks = repo["task_list"]

            return tasks
        except Exception as err:
            log(log_level.ERROR, "database.py", f"task_data function '{err}'")
            raise RuntimeError(err)
