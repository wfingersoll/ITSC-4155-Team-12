import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import '../bootstrap.darkly.css';

const Profile = () => {
    const [user, setUser] = useState(null)

    const navigate = useNavigate()

    useEffect(() => {
        getProfile()
    }, [])
    
    const getProfile = async () => {
        const token = sessionStorage.getItem('token')
        axios({
            method: "POST",
            url: "/get-profile",
            data: {'token': sessionStorage.getItem('token')}
        }).then(response => {
            const res = response.data
            setUser({
                first_name: res.first_name,
                last_name: res.last_name,
                email: res.email,
                movies: res.movie,
            })
        })
    }

    const handleLogOut = () => {
        sessionStorage.removeItem('token')
        navigate("/", {replace:true});
    }

    return(
        <div>
            {user &&
                <div>
                    <h2>{user.first_name} {user.last_name}</h2>
                    <h2>{user.email}</h2>
                    <ul>
                        {user.movies.map((title) => 
                            <li>{title}</li>
                        )}
                    </ul>
                    <button onClick={handleLogOut}>Sign Out</button>
                </div>
            }
        </div>
    )
}

export default Profile