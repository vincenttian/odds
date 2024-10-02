import React, { useState } from 'react'
import styled from 'styled-components/native'
import { Stack } from 'expo-router'
import LinkButton from 'src/components/LinkButton'
import ScreenLayout from 'src/components/ScreenLayout'
import { Button } from 'react-native'

export default function HomeScreen() {
  const [apiResponse, setApiResponse] = useState<string | null>(null)

  const makeApiCall = async () => {
    try {
      const response = await fetch('http://localhost:5500/')
      const data = await response.json()
      setApiResponse(JSON.stringify(data))
    } catch (error) {
      console.error('Error making API call:', error)
      setApiResponse('Error occurred while making API call')
    }
  }

  return (
    <ScreenLayout testID="home-screen-layout">
      <S.Content testID="home-screen-content">
        <Stack.Screen options={{ title: 'Home Screen' }} />

        <S.Title testID="home-screen-title">🏠</S.Title>
        <S.Text testID="home-screen-text">Go to app/index.tsx to edit</S.Text>

        <LinkButton href="/second" text="Go To Second Screen" />

        <Button title="Make API Call" onPress={makeApiCall} />

        {apiResponse && (
          <S.ApiResponse testID="api-response">
            API Response: {apiResponse}
          </S.ApiResponse>
        )}
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
