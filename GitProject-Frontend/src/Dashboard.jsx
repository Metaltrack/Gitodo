/* eslint-disable no-unused-vars */
import { useEffect, useState } from 'react'
import './App.css'
import { UserClass, Repo } from './scripts/DataClass.jsx'
import { log_level, log } from './scripts/logger.jsx'
import RepoCard from './components/RepoCard.jsx'
import { setTheme, cycleThemes } from '../src/Util/Theme.jsx'

function Dashboard() {
    const API_URL = 'http://192.168.1.70:4067';
    const [User, setUser] = useState(() => UserClass);
    const [RepoList, setRepoList] = useState([]);

    useEffect(() => {
        setTheme(localStorage.getItem("theme") || "light");

        const token = localStorage.getItem("token");

        fetch(`${API_URL}/user-api/user`, { headers: {Authorization: `Bearer ${token}`} }).then(
            (response) => {
                if (!response.ok) {
                    console.log("No response from get-user");
                    return null;
                }
                return response.json();
            }
        ).then(
            (data) => {
                //setRepoList(new Repo(data["repo_list"]))
                setUser(new UserClass(data["name"], data["html_url"]));
                console.log(data);
                console.log(User);
        }).catch(
            (error) => {
                console.log("ERROR: " + error);
            }
        )

        fetch(`${API_URL}/user-api/user-repos`, { headers: { Authorization: `Bearer ${token}` } }).then(
            (response) => {
                if (!response.ok) {
                    log(log_level.ERROR, "Dashboard.jsx", `Response from API for repos'${response.statusText}'`);
                    return null;
                }
                return response.json();
            }
        ).then(
            (data) => {
                const repo_list = [];
                console.log(data);
                data.forEach(repo => {
                    repo_list.push(new Repo(
                        repo.id,
                        repo.name,
                        repo.html_url,
                        repo.progress,
                        repo.total_tasks,
                        repo.completed_tasks,
                        repo.archived,
                        repo.created_at
                    ))
                });

                setRepoList(repo_list);

                console.log(RepoList);
            }
        )
    }, [])

    function updateRepo(repoId, updates) {

        setRepoList(oldRepos =>
            oldRepos.map(repo =>
                repo.id === repoId
                    ? { ...repo, ...updates }
                    : repo
            )
        );

    }

    var stuff_count = 0;
    var [view_archived, setViewArchived] = useState(false);
    const [buttonText, setButtonText] = useState("View Archived");

    function flipArchive() {
        if (view_archived == true) {
            setViewArchived(false);
            setButtonText("View Archived");
        } else {
            setViewArchived(true);
            setButtonText("View Active");
        }
        console.log(view_archived);
    }

    return (
        <>
            <section id="center">
                <h1 onClick={function stuff() {
                    stuff_count = stuff_count + 1;
                    console.log(stuff_count);
                    if (stuff_count >= 10) {
                        setTheme("dev");
                        stuff_count = 0;
                    }
                }}>{'>>'}{User.name}{'<<'}</h1>
                <p>
                    <a href={User.html_url}><code>View Github Page</code></a>
                </p>
                <br />
                <button onClick={cycleThemes}><i>Theme</i></button>
                <br />
                <button onClick={flipArchive} > {buttonText}</button>
                <br />
                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns: "repeat(auto-fit, minmax(360px, 720px))",
                        justifyContent: "center",
                        gap: "25px"
                    }}>

                    {
                        RepoList
                            .filter(repo => view_archived ? repo.archived : !repo.archived)
                            .map(repo => (
                                <RepoCard
                                    key={repo.id}
                                    repo={repo}
                                    onUpdateRepo={updateRepo}
                                />
                            ))
                    }

                </div>

            </section>
        </>
    )
}

export default Dashboard;
