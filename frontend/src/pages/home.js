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
            }))
        })
    } 

    const goToNextPage = () => {
        setPageNumber((pageNumber) => pageNumber + 1);
        getData()
    }

    const goToPrevPage = () => {
        setPageNumber((pageNumber) => pageNumber - 1);
        getData()
    }

    const goToPageNumber = () => {}

  return (
    
    //Currently hacky solution that relies on us only taking 18 items per page
    <div>
        {movieData && 
            <div>
                <h1>Welcome to MovieDB</h1>
                <table>
                    <tbody>
                        <tr>
                            {movieData.titles.slice(0, 6).map((title) => <td>{title}</td>)}
                        </tr>
                        <tr>
                            {movieData.titles.slice(6, 12).map((title) => <td>{title}</td>)}
                        </tr>
                        <tr>
                            {movieData.titles.slice(12, 18).map((title) => <td>{title}</td>)}
                        </tr>
                    </tbody>
                </table>
            </div>
        }
    <button disabled={buttonDisabled} onClick={goToPrevPage}>previous</button>
    <button onClick={goToNextPage}>next</button>
    </div>
  );
};
  
export default Home;