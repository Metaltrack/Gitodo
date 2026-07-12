from pydantic import BaseModel

class task_model(BaseModel):
    task_id :int
    task_name :str
    task_condition :str
    task_completion :bool
    dead_line :str

class repo_model(BaseModel):
    repo_id :int
    repo_name :str
    repo_url :str
    repo_html_url :str
    repo_commit_url :str
    repo_progress :int
    task_list :list[task_model]
    source_list :list[str]
    total_tasks :int
    completed_tasks :int
    repo_archived :bool
    created_at :str

class user_model(BaseModel):
    user_id :int
    access_token :str
    user_name :str
    user_url :str
    user_html_url :str
    user_repo_url :str
    repo_list :list[repo_model]
