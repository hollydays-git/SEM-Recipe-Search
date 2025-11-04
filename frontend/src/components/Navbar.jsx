import { Link, useLocation } from 'react-router-dom';
import '../styles/Navbar.css';

function Navbar() {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          🍳 Recipe Search
        </Link>

        <ul className="navbar-menu">
          <li className="navbar-item">
            <Link to="/" className={`navbar-link ${isActive('/')}`}>
              📊 Dashboard
            </Link>
          </li>
          <li className="navbar-item">
            <Link to="/search" className={`navbar-link ${isActive('/search')}`}>
              🔍 Search
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
