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
import UserPage from "../pages/UserPage";
import AdminRoute from "./AdminRoute";
import AdminPage from "../pages/AdminPage";
import BookingsPage from "../pages/BookingsPage";
import BookingDetailPage from "../pages/BookingDetailPage";

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
            path: '/admin',
            element: (
              <AdminRoute>
                <AdminPage />
              </AdminRoute>
            ),
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
          {
            path: '/UserInfo',
            element: <UserPage/>
          },
          {
            path: '/bookings',
            element: <BookingsPage/>
          },
          {
            path: '/booking/:id',
            element: <BookingDetailPage/>
          }
        ]
      },
]);