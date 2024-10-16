import { createBrowserRouter } from "react-router-dom";
import App from "../App";
import HomePage from "../pages/HomePage";
import ErrorPage from "../pages/ErrorPage";
import PlacesPage from "../pages/PlacesPage";
import ContactPage from "../pages/ContactPage";
import AboutPage from "../pages/AboutPage";
import PlaceSinglePage from "../pages/PlaceSinglePage";

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
        ]
      },
]);