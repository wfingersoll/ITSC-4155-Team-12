import React, { useEffect, useState } from "react";
import axios from "axios";
import '../bootstrap.darkly.css';
import { useParams } from "react-router-dom";


const Film = () => {

    const {title} = useParams()
    const [movieData, setMovieData] = useState(null)
    
    useEffect(() => {
        getData();
    }, []);

    const getData = async() => {
        axios({
            method: "GET",
            url: "/search-prod-info?query=" + title,
        }).then(response => {
            const res = response.data;
            setMovieData(({
                movie_title: res.title,
                director_name: res.director,
                genres: res.genres,
                title_year: res.year,
                platforms: res.streaming_services,
                similar: res.similar
            }))
        })
    }
    //end of new line

    return (
        <div className="row">
            <h1 className="mb-5">MovieDB</h1>

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
                            <tr>
                                <th scope="row">Streaming Platforms</th>
                                <td>{movieData.platforms}</td>
                            </tr>
                            <tr>
                                <th scope="row">Similar Films</th>
                                {movieData.similar.map((film) => <ul>{film}</ul>)}
                            </tr>
                        </tbody>
                    </table>
                </div>
            }
        </div>
    )
}

export default Film;