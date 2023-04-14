import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import '../bootstrap.darkly.css';

const Profile = () => {
    const [user, setUser] = useState(null)

    useEffect(() => {
        getProfile()
    }, [])
    
    const getProfile = async () => {
        const token = sessionStorage.getItem('token')
        axios({
            method: "GET",
            url: "/get-profile?token="+token,
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
                </div>
            }
        </div>
    )
}

export default Profile