export const hostName = "https://api.plannder.com";
export const params = [":tripId"];
export const apiEndpoints = {
    auth:{
        login: `${hostName}/user_auth/login/`,
        register: `${hostName}/user/`,
        refreshToken: `${hostName}/user_auth/token/refresh/`,
        verify:`${hostName}/user_auth/token/verify/`
    }
}