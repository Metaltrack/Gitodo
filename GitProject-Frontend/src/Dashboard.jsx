/* eslint-disable no-unused-vars */
import { useEffect, useState } from 'react'
import './App.css'
import {UserClass, Repo} from './scripts/DataClass.jsx'

function Dashboard() {
    const API_URL = 'http://localhost:4067'
    const [User, setUser] = useState(() => UserClass)
    const [RepoList, setRepoList] = useState(() => Repo)

    useEffect(() => {
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
                setUser(new UserClass(data["name"], data["html_url"], data["repo_list"]));
                console.log(data);
                console.log(User);
        }).catch(
            (error) => {
                console.log("ERROR: " + error);
            }
        )
    }, [])

    return (
        <>
            <section id="center">
                <h1>{'>>'}{User.name}{'<<'}</h1>
                <p>
                    <a href={User.html_url}><code>View Github Page</code></a>
                </p>
            </section>
        </>
    )
}

export default Dashboard;
