/* eslint-disable no-unused-vars */
import { useEffect, useState } from 'react'
import './App.css'

function Dashboard() {
    const API_URL = 'http://localhost:4067'

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
                console.log(data);
        }).catch(
            (error) => {
                console.log("ERROR: " + error);
            }
        )
    }, [])

    return (
        <>
            <h1>Dashboard</h1>
        </>
    )
}

export default Dashboard;
