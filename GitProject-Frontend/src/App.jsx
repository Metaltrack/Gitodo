/* eslint-disable no-unused-vars */
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import heroImg from './assets/hero.png'
import './App.css'
import userHandler from './scripts/user_handler'
import Router from './Router'

function App() {
    const [loginChecker, setLoginChecker] = useState("");
    const navigate = useNavigate();

  const API_URL = 'http://localhost:4067'

    function handleLogin(code) {
        fetch(`${API_URL}/user-api/user-login?code=${code}`).then(
            (response) => {
                if (!response.ok) {
                    console.log("No response from user-login");
                    return null;
                }
                return response.json();
            }
        ).then(
            (data) => {
                console.log(data);
                if (data["jwt"]) {
                    setLoginChecker("Login Successfull!");
                    localStorage.setItem("token", data["jwt"]);
                    navigate("/dashboard");
                } else {
                    setLoginChecker("Login Failed!");
                }
            }
        ).catch(
            (error) => {
                console.log("ERROR: " + error);
            }
        )
    }

    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);

        const codeParam = urlParams.get("code");
        if (codeParam) {
            console.log("Successfully got code from git hub...");
            handleLogin(codeParam);
        } else {
            console.log("Login Failed...");
        }
    }, [])

    useEffect(() => {
        fetch(API_URL + '/').then(
            response => {
                if (!response.ok) {
                    console.log(`ERR> API FETCH FAILED ${response.status}`);
                    throw new Error(`ERR> API FETCH FAILED ${response.status}`);
                } else {
                    console.log(`LOG> API FETCH SUCCESS ${response.status}`)
                }
                return response.json();
            }
        ).then(
            data => {
                console.log(data);
                return data["message"];
            }
        ).catch(
            error => {
                console.log(`ERR> POST API FETCH ERROR ${error}`);
            }
        )
    }, [])

  return (
    <>
      <section id="center">
        <div className="hero">
          <img src={heroImg} className="base" width="170" height="179" alt="" />
        </div>
        <div>
          <h1>GITODO</h1>
          <p>
            <code>Automated Github Repo task management platform</code>
          </p>
        </div>
        <button
        type="button"
        className="counter"
        onClick={userHandler.userLoginHandler}
        >
          LOGIN
        </button>
        <br />
        <br />
        <p>{loginChecker}</p>
      </section>
    </>
  )
}

export default App
