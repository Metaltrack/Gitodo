/* eslint-disable no-unused-vars */
import { useSearchParams } from "react-router-dom";
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Router from "../Router";
import { log_level, log } from '../scripts/logger.jsx';
import '../App.css'
import { setTheme, cycleThemes } from '../Util/Theme'
import { Repo, Task } from '../scripts/DataClass.jsx'

function RepoViewer() {
    const API_URL = 'http://192.168.1.70:4067';
    const token = localStorage.getItem("token");

    const [RepoData, setRepoData] = useState(() => Repo);
    const [TaskData, setTaskData] = useState([]);

    const query = window.location.search;
    const searchParams = new URLSearchParams(query);

    const id = searchParams.get("id");

    console.log(id);

    var [taskChecker, setTaskChecker] = useState("");

    useEffect(() => {
        setTheme(localStorage.getItem("theme") || "light");

        fetch(`${API_URL}/user-api/repo/${id}`, {
            headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
            method: "GET"
        }).then((response) => {
            if (!response.ok) {
                log(log_level.ERROR, "RepoViewer.jsx", `Reponse from API '${response.statusText}'`)
                return;
            }

            return response.json();
        }).then((data) => {
            console.log(data);
            setRepoData(new Repo(data["id"], data["name"], data["html_url"], data["progress"], data["total_tasks"], data["completed_tasks"], data["archived"], data["created_at"]));
        }).catch((err) => {
            log(log_level.ERROR, "RepoViewer.jsx", `Error getting repo data '${err}'`);
        });

        fetch(`${API_URL}/user-api/repo/tasks/${id}`, {
            headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
            method: "GET"
        }).then((response) => {
            if (!response.ok) {
                log(log_level.ERROR, "REpoViewer.jsx", `Response from API '${response.statusText}'`);
                return;
            }

            return response.json();
        }).then((data) => {
            const task_list = [];
            console.log(data);
            data.forEach(task => {
                task_list.push(new Task(
                    data["task_id"],
                    data["task_name"],
                    data["task_condition"],
                    data["task_completion"],
                    data["dead_line"]
                ))
            });

            setTaskData(task_list);

            if (TaskData.length == 0) {
                setTaskChecker("~ No Tasks ~");
            }
        });
    }, [])

    return (
        <>
            <section id="center">
                <h1>{'>>'}{RepoData.name}{'<<'}</h1>
                <span
                    className={
                        RepoData.archived
                            ? "status archived"
                            : "status active"
                    }
                >
                    {RepoData.archived ? "Archived" : "Active"}
                </span>
                <button onClick={cycleThemes}><i>Theme</i></button>
                <br />
                <code>--Progress--</code>
                <div className="progress-bar-repo">
                    <div
                        className="progress-repo"
                        style={{ width: `${RepoData.progress}%` }}
                    ></div>
                </div>
                <br />
                
                <br />
                <h3>
                    {
                        taskChecker
                    }
                </h3>

            </section>
        </>
    )
}

export default RepoViewer;
