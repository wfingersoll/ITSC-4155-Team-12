import React, {useEffect, useState } from "react";
import { Nav, NavLink, NavMenu }
	from "./NavbarElements";
import { useActionData } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Navbar = () => {

	const navigate = useNavigate();

	const [open, setOpen] = useState(false)
	const [films, setFilms] = useState(null)
	const [emptyCells, setEmptyCells] = useState([])

	const handleOpen = () => {
		setOpen(!open);
	}

	useEffect (() => {
		getFilmList();
	}, [])

	const getFilmList = async () => {

		axios({
            method: "GET",
            url: "/get-film-queue",
        }).then(response => {
            const res = response.data;
			const empty_cells_temp = []
			for(let i = 0; i<10; i++) {
				if(i<res.titles.length){
				}
				else{
					res.titles.push('No Film Selected')
				}
			}
			console.log(empty_cells_temp)
			setEmptyCells(empty_cells_temp)
			
            setFilms(({
                titles: res.titles,
				posters: res.posters
            }));
        })

	}

	const goToRandomFilm = () => {
		var index = 0;
		for(let i = 0; i < films.titles.length; i++){
			if(films.titles[i]!='No Film Selected'){
				index++;
			}
		}
		const random = Math.floor(Math.random() * films.titles.slice(0,index).length);
		console.log(random)
        const url = "../film/"+films.titles[random]
        navigate(url, {replace: true});
    }

return (
	<>
	<Nav>
		<NavMenu>
		<NavLink to="/" activeStyle>
			Home
		</NavLink>
		<NavLink to="/search" activeStyle>
			Search
		</NavLink>
		<button className="dropdown-button" onClick={handleOpen}>Film Queue</button>
		</NavMenu>
	</Nav>{ films &&
	<div className="dropdown-queue">
			{open ? (
			<table className="menu-queue">
				<tr>
				{films.titles.map((title, idx) => 
                <td className="film-queue-td">
					<a className={title=='No Film Selected' ? "film-queue-link-container-disabled":"film-queue-link-container"} href={"/film/"+title}>
						<img className="film-queue-image" src={films.posters[idx]} ></img></a>
						<p className="film-queue-text">{title}</p></td>)}
				<td className="film-queue-td">
					<div className="film-queue-random-link-container">
						<button onClick={()=>{goToRandomFilm()}} className="film-queue-random-button">CHOOSE RANDOM FILM</button>
					</div>
					</td>
				</tr>
			</table>
			) : null}
		</div>}
	</>
);
};

export default Navbar;
