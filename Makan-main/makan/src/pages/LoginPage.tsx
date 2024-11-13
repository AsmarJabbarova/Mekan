import React from 'react';
import { Form, Input, Button } from 'antd';
import { Formik, Form as FormikForm, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
import { useUser } from '../contexts/UserContext';
import { useNavigate } from 'react-router-dom';
import '../styles/LoginPageStyles.css';

const validationSchema = Yup.object().shape({
  username: Yup.string().required('Please enter your username or email'),
  password: Yup.string().required('Please enter your password'),
});

interface LoginFormValues {
  username: string;
  password: string;
}

const LoginPage: React.FC = () => {
  const initialValues: LoginFormValues = {
    username: '',
    password: '',
  };

  const { setUser } = useUser();
  const navigate = useNavigate();

  const handleSubmit = async (values: LoginFormValues) => {
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/login`, {
        email: values.username,
        password: values.password,
      });
  
      const { id, username, email } = response.data.user; 
      const token = response.data.access_token;
  
      setUser({ id, username, email, token }); 
      navigate(-1);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('Login failed:', error.response?.data?.message || error.message);
      } else {
        console.error('An unexpected error occurred:', error);
      }
      alert('Login failed. Please check your username and password.');
    }
  };
  
  
  

  return (
    <div className="login-form-container">
      <h2>Login</h2>
      <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={handleSubmit}>
        {({ handleSubmit, values, handleChange }) => (
          <FormikForm onSubmit={handleSubmit}>
            <Form.Item>
              <Field name="username" as={Input} placeholder="Username or Email Address" value={values.username} onChange={handleChange} />
              <ErrorMessage name="username" component="div" className="error-message" />
            </Form.Item>

            <Form.Item>
              <Field name="password" as={Input.Password} placeholder="Password" value={values.password} onChange={handleChange} />
              <ErrorMessage name="password" component="div" className="error-message" />
            </Form.Item>

            <Form.Item>
              <Button type="primary" htmlType="submit" className="login-form-button">
                Sign In
              </Button>
            </Form.Item>
          </FormikForm>
        )}
      </Formik>
      <div className="login-register-sec">
        <p>Do not have an account?</p>
        <a href="/signup">Register</a>
      </div>
    </div>
  );
};

export default LoginPage;
