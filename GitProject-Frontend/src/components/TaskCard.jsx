/* eslint-disable no-unused-vars */
import './RepoCard.css'
import Router from '../Router';
import { log_level, log } from '../scripts/logger.jsx'
import { createSearchParams, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react';
import './TaskStuff.css'

function TaskCard({ repo, onUpdateRepo }) {
    const API_URL = 'http://192.168.1.70:4067';
    const token = localStorage.getItem("token");
    const navigate = useNavigate();

    const [expanded, setExpanded] = useState(false);

    return (

    );
}

export default TaskCard;
