import 'expo-dev-client'
import { ThemeProvider as NavProvider } from '@react-navigation/native'
import { Slot } from 'expo-router'
import { StatusBar } from 'expo-status-bar'
import PropTypes from "prop-types";
import styled, { ThemeProvider, type DefaultTheme } from 'styled-components/native'
import { ApolloClient, ApolloProvider, InMemoryCache, createHttpLink } from '@apollo/client';
import { appTheme, navTheme } from 'src/config/theme'

const httpLink = createHttpLink({
  uri: 'http://localhost:5500/graphql',
  fetch: async (uri, options) => {
    if (options?.method === 'GET') {
      return fetch(uri, {
        ...options,
        method: 'GET',
      });
    } else {
      return fetch(uri, {
        ...options,
        method: 'POST',
      });
    }
  },
});

const client = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
});

export default function AppLayout() {
  return (
    <ApolloProvider client={client}>
      <ThemeProvider theme={appTheme as DefaultTheme}>
        <StatusBar style="light" />
        <S.AppWrapper>
          <NavProvider value={navTheme}>
            <Slot screenOptions={{ headerShown: false }} />
          </NavProvider>
        </S.AppWrapper>
      </ThemeProvider>
    </ApolloProvider>
  )
}

const S = {
  AppWrapper: styled.SafeAreaView`
    flex: 1;
    flex-direction: column;
    background-color: ${appTheme.background};
  `
}
