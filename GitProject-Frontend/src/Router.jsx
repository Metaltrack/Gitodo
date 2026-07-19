import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import Dashboard from "./Dashboard";
import RepoViewer from "./components/RepoViewer";

function Router() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<App />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/repoviewer" element={<RepoViewer />} />
            </Routes>
        </BrowserRouter>
    );
}

export default Router;