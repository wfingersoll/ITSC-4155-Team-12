import { useState } from 'react'
import axios from "axios";
import './App.css';

function App() {
    // new line start
    const [query, setQuery] = useState('')
    const [movieData, setMovieData] = useState(null)

    const getData = event => {
        event.preventDefault();
        axios({
            method: "GET",
            url:"/search-prod-info?query="+query,
        })
        .then(response => {
            const res = response.data;
            setMovieData(({
            movie_title: res.title,
            director_name: res.director,
            title_year: res.year}))
        })
    }
    //end of new line

    return (
        <div class="row">
            <h1>MovieDB</h1>

            <div class="col-md-6">
                <form onSubmit={getData}>
                    <div class="mb-3">
                        <label for="query-input-id" class="form-label">Enter Query:</label>
                        <input type="text"
                               class="form-control"
                               id="query-input-id"
                               value={query}
                               onChange={e => setQuery(e.target.value)}
                        />
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>

            {//movieData &&
                <div class="col-md-6">
                    Result would go here
                </div>
            }
        </div>
    )

  // return (
  //   <div className="App">
  //     <header className="App-header">
  //       {/* new line start*/}
  //       <form onSubmit={getData}>
  //         <label>Enter Query: <span/>
  //           <input
  //           type="text"
  //           value={query}
  //           onChange={(e) => setQuery(e.target.value)}
  //           />
  //         </label>
  //         <input type="submit" />
  //       </form>
  //       {movieData && <div>
  //             <p>Movie Title: {movieData.movie_title}</p>
  //             <p>Director: {movieData.director_name}</p>
  //             <p>Release Date: {movieData.title_year}</p>
  //           </div>
  //       }
  //        {/* end of new line */}
  //     </header>
  //   </div>
  // );
}

export default App;
