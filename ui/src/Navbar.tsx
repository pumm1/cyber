import { NavLink } from 'react-router-dom'
import './Navbar.css'

const Navbar = ({}) => 
    <nav>
        <div>
            <ul>
                <li><NavLink to="/">Home</NavLink></li>
                <li><NavLink to="/weapon-tool">Weapon tool</NavLink></li>
            </ul>
        </div>
    </nav>

export default Navbar