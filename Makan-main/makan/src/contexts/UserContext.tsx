import React, { createContext, useContext, useState, useEffect } from 'react';

interface UserContextType {
  id: number | null;
  username: string | null;
  email: string | null;
  token: string | null;
  role: string | null; 
  setUser: (userData: { id: number; username: string; email: string; token: string; role:string }) => void;
  logout: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

const  UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [id, setId] = useState<number | null>(null);
  const [username, setUsername] = useState<string | null>(null);
  const [email, setEmail] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    const savedId = localStorage.getItem('id');
    const savedUsername = localStorage.getItem('username');
    const savedEmail = localStorage.getItem('email');
    const savedRole = localStorage.getItem('role');

    if (savedToken && savedId && savedUsername && savedEmail) {
      setToken(savedToken);
      setId(Number(savedId));
      setUsername(savedUsername);
      setEmail(savedEmail);
      setRole(savedRole);
    }
  }, []);

  const setUser = ({ id, username, email, token, role }: { id: number; username: string; email: string; token: string; role: string }) => {
    setId(id);
    setUsername(username);
    setEmail(email);
    setToken(token);
    setRole(role); 
  
    localStorage.setItem('token', token);
    localStorage.setItem('id', id.toString());
    localStorage.setItem('username', username);
    localStorage.setItem('email', email);
    localStorage.setItem('role', role); 
  };
  const logout = () => {
    setId(null);
    setUsername(null);
    setEmail(null);
    setToken(null);
    setRole(null);
    localStorage.removeItem('token');
    localStorage.removeItem('id');
    localStorage.removeItem('username');
    localStorage.removeItem('email');
    localStorage.removeItem('role');
  };

  return (
    <UserContext.Provider value={{ id, username, email, token, role, setUser, logout }}>
      {children}
    </UserContext.Provider>
  );
};

const useUser = (): UserContextType => {
    const context = useContext(UserContext);
    if (!context) {
      throw new Error('useUser must be used within a UserProvider');
    }
    return context;
  };
  

export { UserProvider, useUser };