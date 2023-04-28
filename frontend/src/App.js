import React, { useState } from 'react';
import Navbar from './components/index';
import { BrowserRouter as Router, Routes, Route}
    from 'react-router-dom';
import Home from './pages/home';
import Search from "./pages/search";
import Film from "./pages/film";
import Login from "./pages/login";
import Profile from "./pages/profile";  
import Temp from "./pages/temp_page";
import Signup from "./pages/signup";

function App() {

    const [refresh, setRefresh] = useState(false)

return (
    <Router>
    <Navbar refresh={refresh} onUpdate={() => setRefresh(!refresh)}/>
    <Routes>
        <Route path='/' element={<Home refresh={refresh} onUpdate={() => setRefresh(!refresh)}/>} />
        <Route path='/search' element={<Search/>} />
        <Route path='/film/:title' element={<Film/>} />
        <Route path='/login' element={<Login/>} />
        <Route path="/profile" element={<Profile/>} />
        <Route path="/temp_page" element={<Temp/>} />
        <Route path="/signup" element={<Signup/>} />
    </Routes>
    </Router>
);
}
  
export default App;