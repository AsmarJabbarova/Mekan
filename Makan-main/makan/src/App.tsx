import './App.css';
import { Outlet } from 'react-router-dom';
import NavBar from './components/NavBar/NavBar';
import Header from './components/Header/Header';
import { IconContext } from 'react-icons';
import Footer from './components/Footer/Footer';
import { UserProvider } from './contexts/UserContext';
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY);

function App() {
  return (
    <UserProvider>
      <IconContext.Provider value={{ color: 'white', className: 'global-class-name' }}>
        <Header />
        <NavBar />
        <Elements stripe={stripePromise}>
          <Outlet />  
        </Elements>
        <Footer />
      </IconContext.Provider>
    </UserProvider>
  );
}

export default App;
