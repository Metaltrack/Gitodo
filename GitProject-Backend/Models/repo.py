from Models.task import Task

class Repo():
    repo_id :int
    repo_name :str
    repo_url :str
    repo_html_url :str
    repo_commit_url :str

    def __init__(self, _id :int, name :str, url :str, html_url :str, commit_url :str):
        self.repo_id = _id
        self.repo_name = name
        self.repo_url = url
        self.repo_html_url = html_url
        self.repo_commit_url = commit_url
        self.repo_progress :int
        self.task_list :list[Task] = []

    def check_progress(self):
        total_complete :int = 0
        for t in self.task_list:
            if t.task_completion == True:
                total_complete += 1

        return (total_complete / len(self.task_list))
        
