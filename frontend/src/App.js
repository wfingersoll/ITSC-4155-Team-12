import React from 'react';
import Navbar from './components/index';
import { BrowserRouter as Router, Routes, Route}
    from 'react-router-dom';
import Home from './pages/home';
import Search from "./pages/search";
import Film from "./pages/film";
import Login from "./pages/login";
import Profile from "./pages/profile";  

function App() {
return (
    <Router>
    <Navbar />
    <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/search' element={<Search/>} />
        <Route path='/film/:title' element={<Film/>} />
        <Route path='/login' element={<Login/>} />
        <Route path="/profile" element={<Profile/>} />
    </Routes>
    </Router>
);
}
  
export default App;