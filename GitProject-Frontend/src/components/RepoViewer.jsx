/* eslint-disable no-unused-vars */
import { useSearchParams } from "react-router-dom";
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Router from "../Router";
import { log_level, log } from '../scripts/logger.jsx';
import '../App.css'
import './TaskStuff.css'
import { setTheme, cycleThemes } from '../Util/Theme'
import { Repo, Task } from '../scripts/DataClass.jsx'

function RepoViewer() {
    const API_URL = 'http://192.168.1.70:4067';
    const token = localStorage.getItem("token");

    const [RepoData, setRepoData] = useState(() => Repo);
    const [TaskData, setTaskData] = useState([]);
    const [CompletedTasksCount, setCompletedTasksCount] = useState(0);
    const [NextDeadline, setNextDeadline] = useState();

    const query = window.location.search;
    const searchParams = new URLSearchParams(query);

    const id = searchParams.get("id");

    console.log(id);

    var [taskChecker, setTaskChecker] = useState("No Tasks");


    const [ShowAddTask, setShowAddTask] = useState(false);
    const [newTask, setNewTask] = useState({
        task_name: "",
        task_condition: "",
        dead_line: ""
    });

    function addTask() {
        console.log(newTask);

        fetch(`${API_URL}/user-api/repo/tasks/add-task/${id}`, {
            headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
            method: "POST",
            body: JSON.stringify(newTask)
        }).then((response) => {
            if (!response.ok) {
                log(log_level.ERROR, "RepoViewer.jsx", `Response from API '${response.statusText}'`)
                return;
            }

            return response.json();
        }).then((data) => {
            console.log(data);
        }).catch((err) => {
            log(log_level.ERROR, "RepoViewer.jsx", `Error adding task data '${err}'`);
        });

        setShowAddTask(false);
    }

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
                    task.task_id,
                    task.task_name,
                    task.task_condition,
                    task.task_completion,
                    task.dead_line
                ))
            });
            console.log(task_list);
            setTaskData(task_list);
            var completed_count = 0;
            
            TaskData.forEach(task => {
                if (task.task_completion == true) {
                    completed_count = completed_count + 1;
                }
            })

            setCompletedTasksCount(completed_count);

            if (TaskData.length > 0) {
                setNextDeadline(TaskData[0].dead_line);
            } else {
                setNextDeadline("No Tasks");
            }

            if (TaskData.length == 0) {
                setTaskChecker("~ No Tasks ~");
            }
            console.log(TaskData);
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

                <div className="task-action-row">
                    <div className="action-section">
                        <h3>Tasks: {CompletedTasksCount}/{TaskData.length}</h3>
                    </div>
                    <div className="action-section">
                        <button className="active-button" onClick={() => setShowAddTask(true)}>Add Task</button>
                    </div>
                    <div className="action-section">
                        <h3>Next Deadline: {NextDeadline}</h3>
                    </div>
                </div>

                <br />

                <h3>
                    {
                        taskChecker
                    }
                </h3>
            </section>

            {
                ShowAddTask &&
                <div
                    className="modal-overlay"
                    onClick={() => setShowAddTask(false)}
                >
                    <div
                        className="task-modal"
                        onClick={(e) => e.stopPropagation()}
                    >

                        <h2>Add Task</h2>

                        <div className="task-input-group">

                            <label>Task Name</label>
                            <input
                                type="text"
                                value={newTask.task_name}
                                onChange={(e) =>
                                    setNewTask({
                                        ...newTask,
                                        task_name: e.target.value
                                    })
                                }
                            />

                            <label>Completion Condition</label>
                            <textarea
                                rows="4"
                                value={newTask.task_condition}
                                onChange={(e) =>
                                    setNewTask({
                                        ...newTask,
                                        task_condition: e.target.value
                                    })
                                }
                            />

                            <label>Deadline</label>
                            <input
                                type="date"
                                value={newTask.dead_line}
                                onChange={(e) =>
                                    setNewTask({
                                        ...newTask,
                                        dead_line: e.target.value
                                    })
                                }
                            />

                        </div>

                        <div className="modal-buttons">

                                <button
                                    onClick={addTask}
                            >
                                Add
                            </button>

                            <button
                                className="cancel-btn"
                                onClick={() => setShowAddTask(false)}
                            >
                                Cancel
                            </button>

                        </div>

                    </div>
                </div>
            }
        </>
    )
}

export default RepoViewer;
