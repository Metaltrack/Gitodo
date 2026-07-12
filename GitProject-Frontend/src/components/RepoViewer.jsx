/* eslint-disable no-unused-vars */
import { useSearchParams } from "react-router-dom";
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Router from "../Router";
import '../App.css'

function RepoViewer() {
    const searchParams = useSearchParams();

    const id = searchParams.get("id");

    console.log(id);

    return (
        <>
            <h1>Repo Viewer</h1>
        </>
    )
}

export default RepoViewer;
