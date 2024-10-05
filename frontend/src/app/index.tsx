import React, { useState } from 'react'
import styled from 'styled-components/native'
import { Stack } from 'expo-router'
import { Button } from 'react-native'
import { gql, useQuery } from "@apollo/client";
import { View, Text, FlatList } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

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
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Home Screen</Text>
    </View>
  );
};

const ProfileScreen: React.FC = () => {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Profile Screen</Text>
    </View>
  );
};

const MyTabs = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
};

export default function HomeScreen() {
  const { loading, error, data } = useQuery<{ users: User[] }>(GET_USERS);
  if (loading) return <Text>Loading...</Text>;
  if (error) return <Text>Error: {error.message}</Text>;
  console.log(data);
  return <MyTabs />
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