import React, { useEffect, useState } from "react";
import axios from "axios";
import '../bootstrap.darkly.css';
import { useParams } from "react-router-dom";


const Film = ({refresh, onUpdate}) => {

    const {title} = useParams()
    const [movieData, setMovieData] = useState(null)
    
    useEffect(() => {
        getData();
    }, [title]);

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
                similar: res.similar,
                poster: res.poster_path,
                content_warnings: res.content_warnings,
            }))
        })
    }
    //end of new line

    const addToQueue = async(title) => {
        axios({
            method: 'POST',
            url: '/post-film-queue',
            data: {'title': title, 'token': sessionStorage.getItem('token')}
        }).then(response => {
            console.log(response)
        });
    }

    return (
        <div className="row">
            {movieData &&
                <div className="individual-film-container">
                    <h1>{movieData.movie_title}</h1>
                    <div className="individual-film-image-container">
                        <img className="individual-film-image" src={movieData.poster} width="256" height="428"/>
                        <button className="submit-button-narrow" onClick={() => {addToQueue(title);onUpdate()}}>Add to Queue</button>
                    </div>
                    <table className="individual-film-table">
                        <tbody>
                            <tr>
                                <th className="individual-film-th" scope="row">Director</th>
                                <td className="individual-film-td">{movieData.director_name}</td>
                            </tr>
                            <tr>
                                <th className="individual-film-th" scope="row">Genres</th>
                                <td className="individual-film-td">{movieData.genres}</td>
                            </tr>
                            <tr>
                                <th className="individual-film-th" scope="row">Release Date</th>
                                <td className="individual-film-td">{movieData.title_year}</td>
                            </tr>
                            <tr>
                                <th className="individual-film-th" scope="row">Streaming Platforms</th>
                                <td className="individual-film-td">{movieData.platforms}</td>
                            </tr>
                            <tr>
                                <th className="individual-film-th" scope="row">Similar Films</th>
                                <td className="individual-film-td">{movieData.similar.map((film) => <ul>{film}</ul>)}</td>
                            </tr>
                            <tr>
                                <th className="individual-film-th" scope="row">Content Warnings</th>
                                <td className="individual-film-td">{movieData.content_warnings.map((warning) =><ul>{warning}</ul>)}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            }
        </div>
    )
}

export default Film;