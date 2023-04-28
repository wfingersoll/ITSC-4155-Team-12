import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import '../bootstrap.darkly.css';


const Signup = () => {

    const navigate = useNavigate()
    const [token, setToken] = useState(null)
    const [email, setEmail] = useState(null)
    const [password, setPassword] = useState(null)
    const [name, setName] = useState(null)
    const [invalidEmail, setInvalidEmail] = useState(false)

    const handleSubmit = async(event) => {
        event.preventDefault();
        axios({
            method: "POST",
            url: "/signup",
            data: {'email': email, "password": password, 'name': name}
        }).then(response => {
            const res = response.data;
            const temp_token = res.token;
            sessionStorage.setItem('token', temp_token);
            navigate("/", {replace:true});
        }).catch(error => {
            setInvalidEmail(true)
        })
    }

    const handleEmail = (e) => {
        setEmail(e.target.value)
    }

    const handlePassword = (e) => {
        setPassword(e.target.value)
    }

    const handleName = (e) => {
        setName(e.target.value)
    }

    return(
        <div className="login-form-container">
            <form className="login-form" onSubmit={handleSubmit}>
                <div className="login-form-content">
                    <h1 className="login-form-title">Sign Up</h1>
                    <div className="login-input-container">
                        <div className="login-input-container">
                            <label className="login-input-title">First Name:</label>
                            <input
                                type="name"
                                placeholder="Enter Name"
                                onChange={handleName}
                                className="form-control mt-1"
                            />
                        <label className="login-input-title">Email Address:</label>
                        <input
                            type="email"
                            placeholder="Enter Email"
                            onChange={handleEmail}
                            className="form-control mt-1"
                        />
                        <label className="login-input-title">Password:</label>
                        <input 
                            type="password"
                            placeholder="Enter Password"
                            onChange={handlePassword}
                            className="form-control mt-1"
                        />
                        </div>
                    <div className="login-submit-container">
                        <button type="submit" className="submit-button">Submit</button>
                    </div>
                </div>
                </div>
            </form>
            {invalidEmail &&
                <div>
                    <h2>Email Already Taken</h2>
                </div>
            }
        </div>
    )
}

export default Signup