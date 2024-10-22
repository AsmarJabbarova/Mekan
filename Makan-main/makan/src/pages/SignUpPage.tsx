import '../styles/SignUpPageStyles.css'

import React from 'react';
import { Form, Input, Button, Checkbox } from 'antd';
import { Formik, Form as FormikForm, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

// Validation schema for the form
const validationSchema = Yup.object().shape({
  username: Yup.string().required('Please enter a username'),
  email: Yup.string().email('Invalid email format').required('Please enter your email'),
  password: Yup.string().min(6, 'Password must be at least 6 characters').required('Please enter your password'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password'), null], 'Passwords must match')
    .required('Please confirm your password'),
  acceptTerms: Yup.boolean().oneOf([true], 'You must accept the terms and conditions')
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
    acceptTerms: false
  };

  const handleSubmit = (values: SignUpFormValues) => {
    console.log('Registration values: ', values);
  };

  return (
    <div className="signup-form-container">
      <h2>Register</h2>
      <Formik
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({ handleSubmit, handleChange, values }) => (
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
                placeholder="Email Address"
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
                name="acceptTerms"
                checked={values.acceptTerms}
                onChange={() => handleChange({ target: { name: 'acceptTerms', value: !values.acceptTerms } })}
              >
                I agree to the <a href="/terms">Terms and Conditions</a>
              </Checkbox>
              <ErrorMessage name="acceptTerms" component="div" className="error-message" />
            </Form.Item>

            <Form.Item>
              <Button type="primary" htmlType="submit" className="signup-form-button">
                Register
              </Button>
            </Form.Item>
          </FormikForm>
        )}
      </Formik>
    </div>
  );
};

export default SignUpPage;
