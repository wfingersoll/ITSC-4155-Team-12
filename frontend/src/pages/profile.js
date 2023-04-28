import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import '../bootstrap.darkly.css';

const Profile = () => {
    const [fName, setFName] = useState("N/A")
    const [lName, setLName] = useState("N/A")
    const [email, setEmail] = useState("N/A")
    const [movies, setMovies] = useState(["N/A", "N/A"])
    const [invalidEmail, setInvalidEmail] = useState(false)

    const navigate = useNavigate()

    useEffect(() => {
        getProfile()
    }, [invalidEmail])
    
    const getProfile = async () => {
        axios({
            method: "POST",
            url: "/get-profile",
            data: {'token': sessionStorage.getItem('token')}
        }).then(response => {
            const res = response.data
            setFName(res.first_name)
            setLName(res.last_name)
            setEmail(res.email)
            setMovies(res.movie)
        })
    }

    const handleLogOut = () => {
        sessionStorage.removeItem('token')
        navigate("/", {replace:true});
    }

    const handleUpdate = async() => {
        axios({
            method: "POST",
            url: "/update-profile",
            data: {
                "token": sessionStorage.getItem('token'),
                "f_name": fName,
                "l_name": lName,
                "email": email
            }
        }).then(response => {
            console.log(response.status)
        }).catch((error) => {
            setInvalidEmail(true)
        })
    }

    const updateFName = (e) => {
        e.preventDefault()
        setFName(e.target.value)
    }

    const updateLName = (e) => {
        e.preventDefault()
        setLName(e.target.value)
    }
    const updateEmail = (e) => {
        e.preventDefault()
        setEmail(e.target.value)
    }

    return(
        <div>
                <div>
                    <h2>{fName}</h2>
                    <form onSubmit={handleUpdate}>
                        <textarea onChange={(e) => updateFName(e)}/>
                    <h2>{lName}</h2>
                        <textarea onChange={(e) => updateLName(e)}/>
                    <h2>{email}</h2>
                        <textarea onChange={(e) => updateEmail(e)}/>
                    </form>
                    <ul>
                        {movies.map((title) => 
                            <li>{title}</li>
                        )}
                    </ul>
                    <button className="submit-button" onClick={handleUpdate}>Submit Profile Changes</button>
                    <button className="submit-button" onClick={handleLogOut}>Sign Out</button>
                    {invalidEmail &&
                        <div>
                            <h1>Email Already Taken</h1>    
                        </div>
                    }
                </div>
        </div>
    )
}

export default Profile