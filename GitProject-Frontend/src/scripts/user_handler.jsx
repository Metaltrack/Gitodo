/* eslint-disable no-unused-vars */

const CLIENT_ID = import.meta.env.VITE_CLIENT_ID;
import { log, log_level } from './logger'

//Called When user presses login button
//Redirects to Github signin and gets us the code
//Client ID is required
export async function userLoginHandler() {
    try {
        window.location.assign("https://github.com/login/oauth/authorize?client_id=" + CLIENT_ID);
    } catch {
        throw new Error("Error Loging in with GITHUB...");
        log(log_level.ERROR, "user_handler.jsx", `userLoginHandler function 'Github Login Error'`);
    }
}

const userHandler = {
    userLoginHandler,
    CLIENT_ID
};

export default userHandler;
