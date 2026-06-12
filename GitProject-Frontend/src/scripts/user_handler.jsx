/* eslint-disable no-unused-vars */

const CLIENT_ID = import.meta.env.VITE_CLIENT_ID;

export async function userLoginHandler() {
    try {
        window.location.assign("https://github.com/login/oauth/authorize?client_id=" + CLIENT_ID);
    } catch {
        throw new Error("Error Loging in with GITHUB...")
    }
}

const userHandler = {
    userLoginHandler,
    CLIENT_ID
};

export default userHandler;
