import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import storage from './storage'; // Your custom storage module

interface AuthContextType {
  isLoggedIn: boolean;
  login: (token: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const isLoggedIn = token !== null;
  useEffect(() => {
    const loadToken = async () => {
      const storedToken = await storage.getItem('auth_token');
      if (storedToken) {
        setToken(storedToken);
      }
    };
    loadToken();
  }, []);

  const login = async (newToken: string) => {
    await storage.setItem('auth_token', newToken);
    setToken(newToken);
  };

  const logout = async () => {
    await storage.deleteItem('auth_token');
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};