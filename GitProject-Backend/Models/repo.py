from Models.task import Task
from datetime import datetime

class Repo():
    repo_id :int
    repo_name :str
    repo_url :str
    repo_html_url :str
    repo_commit_url :str

    def __init__(self, _id :int, name :str, url :str, html_url :str, commit_url :str, created_at :str):
        try:
            self.repo_id = _id
            self.repo_name = name
            self.repo_url = url
            self.repo_html_url = html_url
            self.repo_commit_url = commit_url
            self.repo_progress :int = 0
            self.repo_archived :bool = False
            self.task_list :list[Task] = []
            self.source_list :list[str] = []
            self.created_at :str = str(datetime.fromisoformat(created_at.replace("Z", "+00:00")))

            self.total_tasks :int = len(self.task_list)
            self.completed_tasks :int = 0
            for task in self.task_list:
                if task.task_completion == True:
                    self.completed_tasks += 1
        except Exception as err:
            raise RuntimeError(err)


    def check_progress(self):
        total_complete :int = 0
        for t in self.task_list:
            if t.task_completion == True:
                total_complete += 1

        return (total_complete / len(self.task_list))
        
