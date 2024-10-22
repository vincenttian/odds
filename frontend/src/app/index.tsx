import React, { useEffect, useState } from 'react';
import { Button, View, Text, FlatList } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Stack } from 'expo-router';
import * as SecureStore from 'expo-secure-store';
import { gql, useQuery } from '@apollo/client';
import styled from 'styled-components/native';

import storage from 'src/app/storage';
import { useAuth } from 'src/app/AuthContext';

import { loginAsync, logoutAsync } from 'src/app/_layout';
import NewUserOnboarding from "src/app/onboarding";

import { useDispatch, useSelector } from 'react-redux';


// Define the type for a user based on the schema
interface User {
  id: string;
  email: string;
  username: string;
  firstName?: string;
  lastName?: string;
  profilePhoto?: string;
}

const Tab = createBottomTabNavigator();
const HScreen: React.FC = () => {
  const dispatch = useDispatch();
  const isAuthenticated = useSelector((state) => state?.auth?.isAuthenticated);
  const { isLoggedIn } = useAuth();

  const handleApiCall = async (url: string, body: any): Promise<any> => {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });
      console.log(response);
      if (!response.ok) {
        throw new Error('API call failed');
      }
      const data = await response.json();
      console.log(data);
      return data;
    } catch (error) {
      console.error('API call error:', error);
      throw error;
    }
  };

  const phoneNumber = "+15109968300"; // going downwards
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text style={{ color: 'white' }}>Home Screen</Text>
      <Text style={{ color: 'white' }}>Logged In: {isLoggedIn ? 'True' : 'False'}</Text>
      {/* Only see if unauth */}
      {!isLoggedIn && (
        <>
          <Button title="Create Account" onPress={() => handleApiCall('http://localhost:5500/api/register', { phone: phoneNumber })} />
          <Button title="Verify" onPress={async () => {
            try {
              const response = await handleApiCall('http://localhost:5500/api/verify', { phone: phoneNumber, code: '623995' });
              if (response?.access_token) {
                // set access token in secure store
                // await storage.setItem('auth_token', response.access_token);
                await dispatch(loginAsync({ auth_token: response.access_token }));
                window.location.reload(false);
                // need to refresh state of app
              }
            } catch (error) {
              console.error("verification failed", error);
            }
          }} />
          <Button title="Login" onPress={() => handleApiCall('http://localhost:5500/api/login', { phone: phoneNumber })} />
          <Button title="Re-send code" onPress={() => handleApiCall('http://localhost:5500/api/resend-verification/3531b3c2-9fdc-48dc-b586-f115ef5dc84d', { phone: phoneNumber })} />
        </>
      )}
      {/* Only see if auth */}
      {isLoggedIn && (
        <Button title="Log out" onPress={async () => {
          await dispatch(logoutAsync());
          window.location.reload(false);
        }} />
      )}
    </View>
  );
};

const GridScreen: React.FC = () => {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text style={{ color: 'white' }}>Grid Screen</Text>
    </View>
  );
};

const ProfileScreen: React.FC = () => {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text style={{ color: 'white' }}>Profile Screen</Text>
    </View>
  );
};

const AuthTabs = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HScreen} />
      <Tab.Screen name="Grid" component={GridScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
};

export default function HomeScreen() {
  // const { loading, error, data } = useQuery<{ users: User[] }>(GET_USERS);
  // if (loading) return <Text>Loading...</Text>;
  // if (error) return <Text>Error: {error.message}</Text>;
  // console.log(data);
  const { isLoggedIn } = useAuth();
  if (isLoggedIn) {
    return <AuthTabs />;
  } else {
    return <NewUserOnboarding />
  }
}

const S = {
  Content: styled.View`
    flex: 1;
    align-items: center;
    justify-content: center;
  `,
  Title: styled.Text`
    color: ${(p) => p.theme.primary};
    font-family: helvetica;
    font-weight: 900;
    font-size: ${(p) => p.theme.size(200, 'px')};
    margin-bottom: ${(p) => p.theme.size(10, 'px')};
  `,
  Text: styled.Text`
    color: ${(p) => p.theme.primary};
    font-family: helvetica;
    font-weight: 700;
    font-size: ${(p) => p.theme.size(15, 'px')};
    margin-bottom: ${(p) => p.theme.size(15, 'px')};
  `,
  ApiResponse: styled.Text`
    color: ${(p) => p.theme.primary};
    font-family: helvetica;
    font-size: ${(p) => p.theme.size(12, 'px')};
    margin-top: ${(p) => p.theme.size(15, 'px')};
    text-align: center;
  `
}

const GET_USERS = gql`
  query GetUsers {
    users {
      id
      email
      username
      firstName
      lastName
      profilePhoto
    }
  }
`;