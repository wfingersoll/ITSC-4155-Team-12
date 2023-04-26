import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import '../bootstrap.darkly.css';

const Temp = () => {

    const navigate = useNavigate()
    const [tempToken, setTempToken] = useState()

    useEffect(() => {
        navigate("/")
        setTempToken(sessionStorage.getItem('token'))
    })

    return(
        <div>
            <h1>Loading...</h1>
            <h1>{tempToken}</h1>
        </div>
    )
}

export default Temp