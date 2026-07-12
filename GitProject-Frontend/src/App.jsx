/* eslint-disable no-unused-vars */
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import heroImg from './assets/hero.png'
import './App.css'
import userHandler from './scripts/user_handler'
import Router from './Router'
import { log, log_level } from './scripts/logger'

function App() {
    const [loginChecker, setLoginChecker] = useState("");
    const navigate = useNavigate();

    const API_URL = 'http://192.168.1.70:4067'

//Send backend Code from Github to get Auth Code for data
    function handleLogin(code) {
        fetch(`${API_URL}/user-api/user-login?code=${code}`).then(
            (response) => {
                if (!response.ok) {
                    log(log_level.ERROR, "App.jsx", `Response from API '${response.statusText}'`);
                    return null;
                }
                return response.json();
            }
        ).then(
            (data) => {
                log(log_level.INFO, "App.jsx", `Data from API '${data}'`);
                if (data["jwt"]) {
                    setLoginChecker("Login Successfull!");
                    localStorage.setItem("token", data["jwt"]);
                    if (localStorage.getItem("token")) {
                        navigate("/dashboard");
                    }
                } else {
                    setLoginChecker("Login Failed!");
                }
            }
        ).catch(
            (error) => {
                log(log_level.ERROR, "App.jsx", `handleLogin function '${error}'`);
            }
        )
    }

//Call when Github redirects us back
    useEffect(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);

        const codeParam = urlParams.get("code");
        if (codeParam) {
            log(log_level.INFO, "App.jsx", `Successfully recieved code from Github for further authorization`);
            //call to backend
            handleLogin(codeParam);
        } else {
            log(log_level.WARNING, "App.jsx", `User not yet logged in through github`);
        }
    }, [])

//Page Startup Function
    useEffect(() => {
        fetch(API_URL + '/').then(
            response => {
                if (!response.ok) {
                    log(log_level.ERROR, "App.jsx", `Response from API '${response.statusText}'`);
                    throw new Error(`ERR> API FETCH FAILED ${response.status}`);
                } else {
                    log(log_level.INFO, "App.jsx", `Response from API '${response.statusText}'`);
                }
                return response.json();
            }
        ).then(
            data => {
                log(log_level.INFO, "App.jsx", `Data from API '${data}'`)
                return data["message"];
            }
        ).catch(
            error => {
                log(log_level.ERROR, "App.jsx", `useEffect promise '${error}'`);
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
