import React, {useEffect, useState } from "react";
import { Nav, NavLink, NavMenu }
	from "./NavbarElements";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Navbar = ({refresh, onUpdate}) => {

	const navigate = useNavigate();

	const [open, setOpen] = useState(false)
	const [films, setFilms] = useState(null)
	const [emptyCells, setEmptyCells] = useState([])

	const handleOpen = () => {
		setOpen(!open);
	}

	useEffect (() => {
		if(sessionStorage.getItem('token')){
			getFilmList();
		}
	}, [sessionStorage.getItem('token'), refresh])

	const getFilmList = async () => {
		axios({
            method: "POST",
            url: "/get-film-queue",
			data: {'token': sessionStorage.getItem('token')}
        }).then(response => {
            const res = response.data;
			const empty_cells_temp = []
			for(let i = 0; i<10; i++) {
				if(i<res.titles.length){
				}
				else{
					res.titles.push('Empty')
				}
			}
			// Empty cells is so we always have at least ten films in queue
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
			if(films.titles[i]!='Empty'){
				index++;
			}
		}
		const random = Math.floor(Math.random() * films.titles.slice(0,index).length);
        const url = "../film/"+films.titles[random]
        navigate(url, {replace: true});
    }

	const handleRemove = async(title) => {
		axios({
			method: "POST",
			url: "/remove-film-queue",
			data: {'title': title, "token": sessionStorage.getItem('token')}
		}).then(response => {
			console.log(response)
		})
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
		{ !sessionStorage.getItem('token') &&
			<NavLink to="/login" acti>
				Login
			</NavLink>
		}
		{ sessionStorage.getItem('token') && 
			<NavLink to="/profile" activeStyle>
			Profile
			</NavLink>
		}
		{ films && sessionStorage.getItem('token') && 
			<button className="dropdown-button" onClick={handleOpen}>Film Queue</button>
		}
		</NavMenu>
	</Nav>{ films && sessionStorage.getItem('token') && 
	<div className={open ? "dropdown-queue":"dropdown-queue-closed"}>
			<table className="menu-queue">
				<tr>
				{films.titles.map((title, idx) => 
                <td className="film-queue-td">
					<a className={title=='Empty' ? "film-queue-link-container-disabled":"film-queue-link-container"} href={"/film/"+title}>
						<img className="film-queue-image" src={films.posters[idx]} ></img></a>
						<p className="film-queue-text">{title}</p>
						<button className="submit-button"onClick={() => {handleRemove(title);onUpdate()}}>Remove</button>
						</td>)}
				<td className="film-queue-td">
					<div className="film-queue-random-link-container">
						<button onClick={()=>{goToRandomFilm()}} className="film-queue-random-button">CHOOSE RANDOM FILM</button>
					</div>
					</td>
				</tr>
			</table>
		</div>}
	</>
);
};

export default Navbar;
