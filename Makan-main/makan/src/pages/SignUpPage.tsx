import React from 'react';
import { Form, Input, Button, Checkbox } from 'antd';
import { Formik, Form as FormikForm, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
import { useUser } from '../contexts/UserContext';
import '../styles/SignUpPageStyles.css';

const validationSchema = Yup.object().shape({
  username: Yup.string().required('Please enter a username'),
  email: Yup.string().email('Invalid email').required('Please enter an email'),
  password: Yup.string().required('Please enter a password'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password')], 'Passwords must match')
    .required('Please confirm your password'),
  acceptTerms: Yup.boolean().oneOf([true], 'You must accept the terms and conditions'),
});

interface SignUpFormValues {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  acceptTerms: boolean;
}

const SignUpPage: React.FC = () => {
  const initialValues: SignUpFormValues = {
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    acceptTerms: false,
  };

  const { setUser } = useUser();

  const handleSubmit = async (values: SignUpFormValues) => {
    try {
      await axios.post(`${import.meta.env.VITE_API_URL}/users`, {
        username: values.username,
        email: values.email,
        password: values.password,
      });
  
      alert('Registration successful! Please log in.');
  
      window.location.href = '/login';
    } catch (error) {
      console.error('Registration failed:', error);
      alert('Registration failed. Please try again.');
    }
  };
  

  return (
    <div className="signup-form-container">
      <h2>Sign Up</h2>
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
                placeholder="Username"
                value={values.username}
                onChange={handleChange}
              />
              <ErrorMessage name="username" component="div" className="error-message" />
            </Form.Item>

            <Form.Item>
              <Field
                name="email"
                as={Input}
                placeholder="Email"
                value={values.email}
                onChange={handleChange}
              />
              <ErrorMessage name="email" component="div" className="error-message" />
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
              <Field
                name="confirmPassword"
                as={Input.Password}
                placeholder="Confirm Password"
                value={values.confirmPassword}
                onChange={handleChange}
              />
              <ErrorMessage name="confirmPassword" component="div" className="error-message" />
            </Form.Item>

            <Form.Item>
              <Checkbox
                checked={values.acceptTerms}
                onChange={(e) => setFieldValue('acceptTerms', e.target.checked)}
              >
                I accept the terms and conditions
              </Checkbox>
              <ErrorMessage name="acceptTerms" component="div" className="error-message" />
            </Form.Item>

            <Form.Item>
              <Button type="primary" htmlType="submit" className="signup-form-button">
                Sign Up
              </Button>
            </Form.Item>
          </FormikForm>
        )}
      </Formik>
    </div>
  );
};

export default SignUpPage;
