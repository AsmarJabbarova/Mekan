import { FaSearch } from 'react-icons/fa'
import './NavBarStyles.css'

function NavBar() {
    return (
        <>
            <nav className="navbar navbar-expand-lg navbar-light bg-light sticky-top">
                <div className="container ">
                    <a className="navbar-brand" href="#">Məkan</a>
                    <div className='d-flex justify-content-end'>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav mb-2 mb-lg-0 ">
                          <li className="nav-item active">
                            <a className="nav-link" href="#">Home</a>
                          </li>
                          <li className="nav-item">
                            <a className="nav-link" href="#">Destination</a>
                          </li>
                          <li className="nav-item">
                            <a className="nav-link" href="#">Contact</a>
                          </li>
                          <li className="nav-item">
                            <a className="nav-link" href="#">About</a>
                          </li>
                        </ul>
                    </div>
                    <div className='dropdown dropdown-line'>
                            <a className="btn " href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <FaSearch color='black'/>
                            </a>
                          <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                          <form className="px-4 py-3 dropdown-item">
                            <input className="form-control me-2" type="search" placeholder="Search" aria-label="Search"/>
                            <button className="btn btn-outline-success" type="submit">Search</button>
                          </form>
                          </div>
                        </div>
                    </div>
                </div>
            </nav>
        </>
    )
}

export default NavBar