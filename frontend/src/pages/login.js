import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import '../bootstrap.darkly.css';


const Login = () => {

    const navigate = useNavigate()

    const handleSubmit = async(event) => {
        event.preventDefault();
        axios({
            method: "POST",
            url: "/post-user-info"
        }).then(response => {
            const res = response.data;
            const token = res.token
            sessionStorage.setItem('token', token)
            navigate("/", {replace:true})
        })
    }

    return(
        <div className="login-form-container">
            <form className="login-form" onSubmit={handleSubmit}>
                <div className="login-form-content">
                    <h3 className="login-form-title">Sign in</h3>
                    <div className="login-input-container">
                        <label className="login-input-title">Email Address:</label>
                        <input
                            type="email"
                            placeholder="Enter Email"
                            className="form-control mt-1"
                        />
                    </div>
                    <div className="login-input-container">
                        <label className="login-input-title">Password:</label>
                        <input 
                            type="password"
                            placeholder="Enter Password"
                            className="form-control mt-1"
                        />
                    </div>
                    <div className="login-submit-container">
                        <button type="submit" className="login-submit-button">Submit</button>
                    </div>
                </div>
            </form>
        </div>
    )
}

export default Login