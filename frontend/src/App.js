import { useState } from 'react'
import axios from "axios";
import './App.css';

function App() {

   // new line start
  const [query, setQuery] = useState('')
  const [movieData, setMovieData] = useState(null)

  const getData = (event) => {
    event.preventDefault();
    axios({
      method: "GET",
      url:"/search-prod-info?query="+query,
    })
    .then((response) => {
      const res = response.data;
      setMovieData(({
        movie_title: res.title,
        director_name: res.director,
        title_year: res.year}))
    })
  }
    //end of new line 

  return (
    <div className="App">
      <header className="App-header">
        {/* new line start*/}
        <form onSubmit={getData}>
          <label>Enter Query: <span/>
            <input 
            type="text" 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            />
          </label>
          <input type="submit" />
        </form>
        {movieData && <div>
              <p>Movie Title: {movieData.movie_title}</p>
              <p>Director: {movieData.director_name}</p>
              <p>Release Date: {movieData.title_year}</p>
            </div>
        }
         {/* end of new line */}
      </header>
    </div>
  );
}

export default App;

