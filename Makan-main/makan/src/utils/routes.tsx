import { createBrowserRouter } from "react-router-dom";
import App from "../App";
import HomePage from "../pages/HomePage";
import ErrorPage from "../pages/ErrorPage";
import PlacesPage from "../pages/PlacesPage";
import ContactPage from "../pages/ContactPage";
import AboutPage from "../pages/AboutPage";
import PlaceSinglePage from "../pages/PlaceSinglePage";
import LoginPage from "../pages/LoginPage";
import SignUpPage from "../pages/SignUpPage";

export const router = createBrowserRouter([
    {
        path: '/',
        element: <App/>,
        errorElement: <ErrorPage />, 
        children: [
          {
            path: "*",
            element: <ErrorPage />,
          },
          {
            index: true, 
            element: <HomePage />,
          },
          {
            path: '/Home',
            element: <HomePage/>
          },
          {
            path: '/Places',
            element: <PlacesPage/>
          },
          {
            path: '/Place/:id',
            element: <PlaceSinglePage/>
          },
          {
            path: '/Contact',
            element: <ContactPage/>
          },
          {
            path: '/About',
            element: <AboutPage/>
          },
          {
            path: '/Login',
            element: <LoginPage/>
          },
          {
            path: '/SignUp',
            element: <SignUpPage/>
          },
        ]
      },
]);