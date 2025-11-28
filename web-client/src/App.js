import Scanner from "./components/Scanner/Scanner";
import { useEffect, useState } from "react";
import { backend_login_init, get_cookie, logout_handler } from "./functions";
import Button from "react-bootstrap/Button"


function App() {

    const [userToken, setUserToken] = useState("")
    const [loginStatus, setLoginStatus] = useState(false)

    

    useEffect(() => {
        const cookie = get_cookie("session_id")
        
        setUserToken(cookie)
        if (cookie) {
            setLoginStatus(true)
        }
        else {
          setLoginStatus(false)
          backend_login_init();
        }
      }, [])
    return (
        <>
        <Button variant="primary" onClick={logout_handler}>Logout</Button>
        {loginStatus && (<Scanner />)}
        </>
    )
}

export default App;
