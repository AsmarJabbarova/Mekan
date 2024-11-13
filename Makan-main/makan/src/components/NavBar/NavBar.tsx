import { useState, useEffect, useRef } from 'react';
import { FaRegUserCircle, FaSearch } from 'react-icons/fa';
import { Tooltip } from 'antd';
import { useUser } from '../../contexts/UserContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './NavBarStyles.css';

interface Place {
  id: number;
  name: string;
}

function NavBar() {
  const { id, username, token, logout } = useUser();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [allPlaces, setAllPlaces] = useState<Place[]>([]);
  const [filteredPlaces, setFilteredPlaces] = useState<Place[]>([]);
  const [showSearchBar, setShowSearchBar] = useState(false);
  const searchInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/places`);
        setAllPlaces(response.data);
      } catch (error) {
        console.error('Error fetching places:', error);
      }
    };
    fetchPlaces();
  }, []);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    setFilteredPlaces(
      query.trim() ? allPlaces.filter((place) => place.name.toLowerCase().includes(query.toLowerCase())) : []
    );
  };

  const handlePlaceSelect = (placeId: number) => {
    navigate(`/place/${placeId}`);
    setSearchQuery('');
    setShowSearchBar(false);
  };  

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleSearchBar = () => {
    setShowSearchBar(!showSearchBar);
    setSearchQuery('');
  };


  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light sticky-top">
      <div className="container">
        <a href="/home">
          <img src="/MəKan (2).png" alt="Logo" className="logo-img" />
        </a>
        <div className="d-flex justify-content-end">
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav mb-2 mb-lg-0">
              <li className="nav-item active">
                <a className="nav-link" href="/home">
                  Home
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="/places">
                  Destination
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="/contact">
                  Contact
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="/about">
                  About
                </a>
              </li>
            </ul>
          </div>
          <div className="search-user-sec">
            <div className="dropdown-line">
              {showSearchBar ? (
                <div className="search-bar-container">
                  <input
                    ref={searchInputRef}
                    className="form-control search-bar"
                    type="search"
                    placeholder="Search for places..."
                    aria-label="Search"
                    value={searchQuery}
                    onChange={handleSearchChange}
                  />
                  {filteredPlaces.length > 0 && (
                    <div className="search-results">
                      {filteredPlaces.map((place) => (
                        <div
                          key={place.id}
                          className="search-result-item"
                          onClick={() => handlePlaceSelect(place.id)}
                        >
                          {place.name}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                <FaSearch onClick={toggleSearchBar} color="black" style={{ cursor: 'pointer' }} />
              )}
            </div>
            <div>
              {token ? (
                <>
                  <Tooltip title={username || 'User'}>
                    <a href="/edit-profile">
                      <FaRegUserCircle color="#63ab45" />
                    </a>
                  </Tooltip>
                  <button onClick={handleLogout} className="logout-button">
                    Logout
                  </button>
                </>
              ) : (
                <a href="/login">
                  <FaRegUserCircle color="#63ab45" />
                </a>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
