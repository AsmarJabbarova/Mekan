import React, { useEffect } from 'react';
import { Form, Input, Button, message } from 'antd';
import axios from 'axios';
import { useUser } from '../contexts/UserContext';

const UserPage: React.FC = () => {
  const { id, username, email, setUser, token } = useUser();
  const [form] = Form.useForm();
  const [passwordForm] = Form.useForm();

  useEffect(() => {
    // Set initial form values using the current username and email from context
    form.setFieldsValue({
      username: username || '',
      email: email || '',
    });
  }, [username, email, form]);

  const handleInfoSubmit = async (values: { username: string; email: string }) => {
    try {
      const response = await axios.put(
        `${import.meta.env.VITE_API_URL}/users/${id}`,
        { username: values.username, email: values.email },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      const updatedUser = response.data;
      setUser({ id: updatedUser.id, username: updatedUser.username, email: updatedUser.email, token });
      message.success('User info updated successfully');
    } catch (error) {
      console.error('Error updating user info:', error);
      message.error('Failed to update user info. Please try again.');
    }
  };

  const handlePasswordSubmit = async (values: { password: string }) => {
    try {
      await axios.put(
        `${import.meta.env.VITE_API_URL}/users/${id}`,
        { password: values.password },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      passwordForm.resetFields();
      message.success('Password updated successfully');
    } catch (error) {
      console.error('Error updating password:', error);
      message.error('Failed to update password. Please try again.');
    }
  };

  return (
    <div className="user-page">
        <div className="about-top-sec">
            <div className="about-top-inner">
                Edit User Information
            </div>
        </div>

      {/* Update User Info Form */}
      <Form
        form={form}
        initialValues={{ username, email }}
        onFinish={handleInfoSubmit}
        layout="vertical"
        style={{ maxWidth: 400, margin: '0 auto' }}
      >
        <Form.Item
          label="Username"
          name="username"
          rules={[{ required: true, message: 'Please enter your username' }]}
        >
          <Input placeholder="Enter new username" />
        </Form.Item>

        <Form.Item
          label="Email"
          name="email"
          rules={[{ required: true, type: 'email', message: 'Please enter a valid email' }]}
        >
          <Input placeholder="Enter new email" />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit">
            Save Changes
          </Button>
        </Form.Item>
      </Form>

      {/* Change Password Form */}
      <div className="about-top-sec">
            <div className="about-top-inner">
                Change Password
            </div>
        </div>
      <Form
        form={passwordForm}
        onFinish={handlePasswordSubmit}
        layout="vertical"
        style={{ maxWidth: 400, margin: '0 auto', marginTop: '20px' }}
      >
        <Form.Item
          label="New Password"
          name="password"
          rules={[{ required: true, message: 'Please enter a new password' }]}
        >
          <Input.Password placeholder="Enter new password" />
        </Form.Item>

        <Form.Item
          label="Confirm Password"
          name="confirmPassword"
          dependencies={['password']}
          rules={[
            { required: true, message: 'Please confirm your password' },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue('password') === value) {
                  return Promise.resolve();
                }
                return Promise.reject(new Error('Passwords do not match'));
              },
            }),
          ]}
        >
          <Input.Password placeholder="Confirm new password" />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit">
            Change Password
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default UserPage;
