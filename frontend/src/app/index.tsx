import React, { useState } from 'react'
import styled from 'styled-components/native'
import { Stack } from 'expo-router'
import LinkButton from 'src/components/LinkButton'
import ScreenLayout from 'src/components/ScreenLayout'
import { Button } from 'react-native'
import { gql, useQuery } from "@apollo/client";
import { View, Text, FlatList } from 'react-native';

// Define the type for a user based on the schema
interface User {
  id: string;
  email: string;
  username: string;
  firstName?: string;
  lastName?: string;
  profilePhoto?: string;
}

export default function HomeScreen() {
  const { loading, error, data } = useQuery<{ users: User[] }>(GET_USERS);
  if (loading) return <Text>Loading...</Text>;
  if (error) return <Text>Error: {error.message}</Text>;
  console.log(data);

  return (
    <ScreenLayout testID="home-screen-layout">
      <S.Content testID="home-screen-content">
        <Stack.Screen options={{ title: 'Home Screen' }} />

        <S.Title testID="home-screen-title">🏠</S.Title>
        <S.Text testID="home-screen-text">Go to app/index.tsx to edit</S.Text>

        <LinkButton href="/second" text="Go To Second Screen" />
        <View>
          Data
          <FlatList
            data={data?.users}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <Text>{item.username} ({item.email})</Text>
            )}
          />
        </View>
      </S.Content>
    </ScreenLayout>
  )
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