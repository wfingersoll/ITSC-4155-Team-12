import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import '../bootstrap.darkly.css';

const Search = () => {
    // new line start
    const [query, setQuery] = useState('')
    const navigate = useNavigate();    

    const goToFilm = () => {
        const url = "../film/"+query;
        navigate(url, {replace: true});
    }

    
    //end of new line

    return (
        <div className="search-container">
            <h1 className="mb-5">Search the MovieDB Catalog</h1>

            {/*
                Input box.
                TODO: MAKE THIS A SEPARATE COMPONENT
            */}
            <div className="search-form-container">
                <form onSubmit={goToFilm}>
                        <label htmlFor="query-input-id" style={{"font-size":"24px"}}className="form-label">Enter Film Title:</label>
                        <input type="text"
                               className="search-form"
                               value={query}
                               onChange={e => setQuery(e.target.value)}
                        />
                    <button type="submit" className="search-submit">Submit</button>
                </form>
            </div>
        </div>
    )
}

export default Search;
