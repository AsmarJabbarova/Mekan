import React from 'react';
import { Form, Input, Button } from 'antd';
import { Formik, Form as FormikForm, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import '../styles/LoginPageStyles.css'

// Validation schema for the form
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
        remember: true,
      };
    
      const handleSubmit = (values: LoginFormValues) => {
        console.log('Login values: ', values);
      };
    
      return (
        <div className="login-form-container">
          <h2>Login</h2>
          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleSubmit}
          >
            {({ handleSubmit, values, handleChange, setFieldValue }) => (
              <FormikForm onSubmit={handleSubmit}>
                <Form.Item>
                  <Field
                    name="username"
                    as={Input}
                    placeholder="Username or Email Address"
                    value={values.username}
                    onChange={handleChange}
                  />
                  <ErrorMessage name="username" component="div" className="error-message" />
                </Form.Item>
    
                <Form.Item>
                  <Field
                    name="password"
                    as={Input.Password}
                    placeholder="Password"
                    value={values.password}
                    onChange={handleChange}
                  />
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
          <div className='login-register-sec'>
            <p>Do not have an account? </p>
            <a href="/signup"> Register</a>
          </div>
        </div>
      );
  };
  
  export default LoginPage;