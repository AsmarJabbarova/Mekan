import { createBrowserRouter } from "react-router-dom";
import App from "../App";
import HomePage from "../pages/HomePage";
import ErrorPage from "../pages/ErrorPage";
import PlacesPage from "../pages/PlacesPage";
import ContactPage from "../pages/ContactPage";
import AboutPage from "../pages/AboutPage";

export const router = createBrowserRouter([
    {
        path: '/',
        element: <App/>,
        children: [
          {
            path: "*",
            element: <ErrorPage />,
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
            path: '/Contact',
            element: <ContactPage/>
          },
          {
            path: '/About',
            element: <AboutPage/>
          },
        ]
      },
]);