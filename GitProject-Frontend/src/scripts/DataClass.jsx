export class Task {
    constructor(name, condition, completion, deadline) {
        this.name = name;
        this.condition = condition;
        this.completion = completion;
        this.deadline = deadline;
    }
}

export class Repo {
    constructor(id, name, html_url, progress, tasks, completed, archived, created_at) {
        this.id = id,
        this.name = name;
        this.html_url = html_url;
        this.progress = progress;
        this.total_tasks = tasks;
        this.tasks_completed = completed;
        this.archived = archived;
        this.created_at = created_at;
    }
}
export class UserClass {
    constructor(name, html_url) {
        this.name = name;
        this.html_url = html_url;
    }
}
