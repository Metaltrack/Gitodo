/* eslint-disable no-unused-vars */
/*import { StrictMode } from 'react'*/
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import Router from './Router'

createRoot(document.getElementById('root')).render(
    <Router />
)
