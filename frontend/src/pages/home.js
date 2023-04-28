import React, { useEffect, useState } from "react";
import axios from "axios";
import '../bootstrap.darkly.css';
import Index from '../components/index';

const Home = ({refresh, onUpdate}) => {

    const [pageNumber, setPageNumber] = useState(0)
    const[pageLength, setPageLength] = useState(18)
    const [movieData, setMovieData] = useState(null)
    const [prevButtonDisabled, setPrevButtonDisabled] = useState(true)
    const [nextButtonDisabled, setNextButtonDisabled] = useState(false)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        getData();
    }, [pageNumber, prevButtonDisabled, nextButtonDisabled]);

    const getData = async () => {

        setLoading(true);

        if (pageNumber != 0) {
            setPrevButtonDisabled(false)
        }
        else{
            setPrevButtonDisabled(true)
        }

        if (pageNumber==298){
            setNextButtonDisabled(true)
        }
        else{
            setNextButtonDisabled(false)
        }

        axios({
            method: "GET",
            url: "/get-page?page_num=" + pageNumber + "&page_length=" + pageLength,
        }).then(response => {
            const res = response.data;
            setMovieData(({
                titles : res.titles,
                posters : res.poster_paths,
                length: res.length,
            }));
            setLoading(false)
        })
    } 

    const goToNextPage = () => {
        setPageNumber((pageNumber) => pageNumber + 1);
    }

    const goToPrevPage = () => {
        setPageNumber((pageNumber) => pageNumber - 1);
    }

    const goToPageNumber = (event) => {
        const pageNum = parseInt(event.target.textContent);
        if (pageNum < movieData.length) {
            setPageNumber(pageNum)
        }
        else {
            setPageNumber(298);
        }
    }

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
    
    //Currently hacky solution that relies on us only taking 18 items per page
    <div>
        {loading && !movieData &&
            <div>
                <h1 className="loading"> Loading Films... </h1>
            </div>
        }
        {movieData && 
            <div className="film-grid">
                <h1 className="film-grid-header">Welcome to MovieDB</h1>
                <table className="film-grid-table">
                    <tbody>
                        <tr>
                            {movieData.titles.slice(0, 6).map((title, idx) => 
                            <td className="film-grid-td">
                                <a className="film-grid-link-container" href={"/film/"+title}>
                                <img className="film-grid-image" src={movieData.posters[idx]} ></img></a>
                                <p className="film-grid-text">{title}</p>
                                { sessionStorage.getItem('token') &&
                                <button className="submit-button" onClick={() => {addToQueue(title);onUpdate()}}>Add to Queue</button>
                                } 
                                </td>
                                )}
                        </tr>
                        <tr>
                            {movieData.titles.slice(6, 12).map((title, idx) => 
                                <td className="film-grid-td">
                                <a className="film-grid-link-container" href={"/film/"+title}>
                                <img className="film-grid-image" src={movieData.posters[idx+6]} ></img></a>
                                <p className="film-grid-text">{title}</p>
                                { sessionStorage.getItem('token') &&
                                <button className="submit-button" onClick={() => {addToQueue(title);onUpdate()}}>Add to Queue</button>
                                }   
                            </td>
                            )}
                        </tr>
                        <tr>
                            {movieData.titles.slice(12, 18).map((title, idx) => 
                                <td className="film-grid-td">
                                <a className="film-grid-link-container" href={"/film/"+title}>
                                <img className="film-grid-image" src={movieData.posters[idx+12]} ></img></a>
                                <p className="film-grid-text">{title}</p>
                                { sessionStorage.getItem('token') &&
                                <button className="submit-button" onClick={() => {addToQueue(title);onUpdate()}}>Add to Queue</button>
                                } 
                            </td>
                            )}
                        </tr>
                    </tbody>
                </table>
            </div>
        }
    {movieData &&
    <div className="page-controls">
    <h4 className="loading">{'Page : ' + pageNumber + ' / ' + movieData.length}</h4>
        <button className={prevButtonDisabled ? "prev-disabled": "prev"} onClick={goToPrevPage}>PREVIOUS</button>
        <form className="page-search" onSubmit={goToPageNumber}>
                <input type="text"
                        id="page-input-id"
                        className="page-search-box"
                        onChange={(e) => (parseInt(e.target.value) < 298 ? setPageNumber(parseInt(e.target.value)): setPageNumber(parseInt(movieData.length)))}
                        />
        </form>
        <button className={nextButtonDisabled ? "next-disabled": "next"} onClick={goToNextPage}>NEXT</button>
    </div>
    }
    {loading && movieData &&
        <h3 className="loading">Loading...</h3>
    }    

    </div>
  );
};
  
export default Home;