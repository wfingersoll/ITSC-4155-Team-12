import React from 'react';
import './App.css';
import Navbar from './components/index';
import { BrowserRouter as Router, Routes, Route}
    from 'react-router-dom';
import Home from './pages/home';
import Search from "./pages/search";
  
function App() {
return (
    <Router>
    <Navbar />
    <Routes>
        <Route exact path='/home' element={<Home />} />
        <Route path='/search' element={<Search/>} />
    </Routes>
    </Router>
);
}
  
export default App;