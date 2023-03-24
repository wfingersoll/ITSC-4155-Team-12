import React, { useState } from "react";
import axios from "axios";
import '../bootstrap.darkly.css';

const Search = () => {
    // new line start
    const [query, setQuery] = useState('')
    const [movieData, setMovieData] = useState(null)

    const getData = event => {
        event.preventDefault();
        axios({
            method: "GET",
            url: "/search-prod-info?query=" + query,
        }).then(response => {
            const res = response.data;
            setMovieData(({
                movie_title: res.title,
                director_name: res.director,
                genres: res.genres,
                title_year: res.year
            }))
        })
    }
    //end of new line

    return (
        <div className="row">
            <h1 className="mb-5">MovieDB</h1>

            {/*
                Input box.
                TODO: MAKE THIS A SEPARATE COMPONENT
            */}
            <div className="col-lg-6 mb-5">
                <form onSubmit={getData}>
                    <div className="mb-3">
                        <label htmlFor="query-input-id" className="form-label">Enter Query:</label>
                        <input type="text"
                               className="form-control"
                               id="query-input-id"
                               value={query}
                               onChange={e => setQuery(e.target.value)}
                        />
                    </div>
                    <button type="submit" className="btn btn-primary">Submit</button>
                </form>
            </div>

            {movieData &&
                <div className="col-lg-6">
                    <h5>{movieData.movie_title}</h5>
                    <table className="table">
                        <tbody>
                            <tr>
                                <th scope="row">Director</th>
                                <td>{movieData.director_name}</td>
                            </tr>
                            <tr>
                                <th scope="row">Genres</th>
                                <td>{movieData.genres}</td>
                            </tr>
                            <tr>
                                <th scope="row">Release Date</th>
                                <td>{movieData.title_year}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            }
        </div>
    )
}

export default Search;
