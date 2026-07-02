
export class Repo {
    constructor(name, html_url, progress, tasks_list) {
        this.name = name;
        this.html_url = html_url;
        this.progress = progress;
        this.tasks_list = tasks_list;
    }
}
export class UserClass {
    constructor(name, html_url, repo_list) {
        this.name = name;
        this.html_url = html_url;
        this.repo_list = repo_list;
    }
}
