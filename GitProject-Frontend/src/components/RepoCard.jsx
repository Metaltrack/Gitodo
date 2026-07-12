/* eslint-disable no-unused-vars */
import './RepoCard.css'
import Router from '../Router';
import { log_level, log } from '../scripts/logger.jsx'

function RepoCard({ repo, onUpdateRepo }) {
    const API_URL = 'http://192.168.1.70:4067';
    const token = localStorage.getItem("token");

    return (
        <div
            className="repo-card"
            onClick={() => {
                window.location.href = `/repoviewer?id=${repo.id}`;
            }}
        >

            <div className="repo-header">
                <h2>{repo.name}</h2>

                <span
                    className={
                        repo.archived
                            ? "status archived"
                            : "status active"
                    }
                >
                    {repo.archived ? "Archived" : "Active"}
                </span>
            </div>

            <a
                href={repo.html_url}
                target="_blank"
                rel="noreferrer"
                onClick={(e) => e.stopPropagation()}
            >
                <code>Open on GitHub</code>
            </a>

            <div className="progress-bar">
                <div
                    className="progress"
                    style={{ width: `${repo.progress}%` }}
                ></div>
            </div>
            <br />
            <div className="task-info">
                {repo.tasks_completed} / {repo.total_tasks} Tasks
            </div>
            <p className="task-info">Created At: {repo.created_at}</p>
            <div className="button-row">

            <button
                className="archive-tab"
                onClick={(e) => {

                    e.stopPropagation();

                    log(log_level.INFO, "RepoCard.jsx", `Archiving repo '${repo.id}'`)
                    fetch(`${API_URL}/user-api/user-update-repo/${repo.id}`, {
                        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` }, method: "POST", body: JSON.stringify({
                            repo_archived: true
                        })
                    }).then(
                        (response) => {
                            if (!response.ok) {
                                log(log_level.ERROR, "RepoCard.jsx", `Respomse from API '${response.statusText}'`)
                                return;
                            }

                            onUpdateRepo(repo.id, {
                                archived: true
                            });
                        }
                    ).catch(
                        (error) => {
                            log(log_level.ERROR, "RepoCard.jsx", `Archive tab function '${error}'`)
                        }
                    )
                }}
                title="Archive"
            >
                    {'>'}]
            </button>

            </div>

        </div>
    );
}

export default RepoCard;
