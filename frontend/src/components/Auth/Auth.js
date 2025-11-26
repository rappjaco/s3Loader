import { useEffect, useState } from "react";
import { backend_login_init, get_cookie } from "./functions";


function Auth() {

    const [userToken, setUserToken] = useState("")

    const urlParams = new URLSearchParams(window.location.search)

    useEffect(() => {
        const auth = urlParams.get("auth")
        const cookie = get_cookie("session_id")
        setUserToken(cookie)
        if (cookie) {
            console.log(cookie)
        }
        else {
            backend_login_init();
        }
    }, [userToken])
    return (
        <>

        </>
    )

}

export default Auth