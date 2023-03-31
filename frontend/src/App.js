import React from 'react';
import Navbar from './components/index';
import { BrowserRouter as Router, Routes, Route}
    from 'react-router-dom';
import Home from './pages/home';
import Search from "./pages/search";
import Film from "./pages/film";
  
function App() {
return (
    <Router>
    <Navbar />
    <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/search' element={<Search/>} />
        <Route path='/film/:title' element={<Film/>} />
    </Routes>
    </Router>
);
}
  
export default App;