import React, { useEffect, useState } from "react";
import axios from "axios";
import '../bootstrap.darkly.css';

const Home = () => {

    const [pageNumber, setPageNumber] = useState(0)
    const[pageLength, setPageLength] = useState(18)
    const [movieData, setMovieData] = useState(null)
    const [buttonDisabled, setButtonDisabled] = useState(true)

    useEffect(() => {
        getData();
    }, [pageNumber, buttonDisabled]);

    const getData = async () => {

        if (pageNumber != 0) {
            setButtonDisabled(false)
        }
        else{
            setButtonDisabled(true)
        }

        axios({
            method: "GET",
            url: "/get-page?page_num=" + pageNumber + "&page_length=" + pageLength,
        }).then(response => {
            const res = response.data;
            setMovieData(({
                titles : res.titles,
                posters : res.poster_paths,
            }))
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
        setPageNumber(pageNum);
    }
  return (
    
    //Currently hacky solution that relies on us only taking 18 items per page
    <div>
        {movieData && 
            <div>
                <h1>Welcome to MovieDB</h1>
                <table>
                    <tbody>
                        <tr>
                            {movieData.titles.slice(0, 6).map((title, idx) => 
                            <td><a href={"/film/"+title}><img src={movieData.posters[idx]} width="64" height="100"></img></a><br/>{title}</td>)}
                        </tr>
                        <tr>
                            {movieData.titles.slice(6, 12).map((title, idx) => 
                            <td><img src={movieData.posters[idx+6]} width="64" height="100"></img><br/>{title}</td>)}
                        </tr>
                        <tr>
                            {movieData.titles.slice(12, 18).map((title, idx) => 
                            <td><img src={movieData.posters[idx+12]} width="64" height="100"></img><br/>{title}</td>)}
                        </tr>
                    </tbody>
                </table>
            </div>
        }
    <div className="page-controls">
        <button className="prev" disabled={buttonDisabled} onClick={goToPrevPage}>previous</button>
                <form onSubmit={goToPageNumber}>
                        <input type="text"
                               id="page-input-id"
                               className="page-search"/>
                    <button type="submit" className="btn btn-primary">Submit</button>
                </form>
            </div>
        <button className="next" onClick={goToNextPage}>next</button>
    </div>
  );
};
  
export default Home;