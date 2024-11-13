import './App.css';
import { Outlet } from 'react-router-dom';
import NavBar from './components/NavBar/NavBar';
import Header from './components/Header/Header';
import { IconContext } from 'react-icons';
import Footer from './components/Footer/Footer';
import { UserProvider } from './contexts/UserContext';

function App() {
  return (
    <UserProvider>
      <IconContext.Provider value={{ color: 'white', className: 'global-class-name' }}>
        <Header />
        <NavBar />
        <Outlet />
        <Footer />
      </IconContext.Provider>
    </UserProvider>
  );
}

export default App;
