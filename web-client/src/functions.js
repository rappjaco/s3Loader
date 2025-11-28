const URL = "http://localhost:8000"


export async function backend_login_init() {
    try {
        window.location.href = `${URL}/api/v1/login`;
    } catch (error) {
        console.log(`error: ${error}`)
        throw error
    }
}


export function get_cookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export function logout_handler() {
    document.cookie = "session_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"

    window.location.reload()
}