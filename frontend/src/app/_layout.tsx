import 'expo-dev-client'
import { ThemeProvider as NavProvider } from '@react-navigation/native'
import { Slot } from 'expo-router'
import { StatusBar } from 'expo-status-bar'
import PropTypes from "prop-types";
import styled, { ThemeProvider, type DefaultTheme } from 'styled-components/native'
import { ApolloClient, ApolloProvider, InMemoryCache, createHttpLink } from '@apollo/client';
import { appTheme, navTheme } from 'src/config/theme'
import { configureStore } from '@reduxjs/toolkit';
import { Provider } from 'react-redux';

const initialState = { value: 0 }
function rootReducer(state = initialState, action: any) {
  // Check to see if the reducer cares about this action
  if (action.type === 'counter/increment') {
    return {
      ...state, // If so, make a copy of `state`
      value: state.value + 1 // and update the copy with the new value
    }
  }
  // otherwise return the existing state unchanged
  return state
}

const store = configureStore({
  reducer: rootReducer,
});

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
    <Provider store={store}>
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
    </Provider>
  )
}

const S = {
  AppWrapper: styled.SafeAreaView`
    flex: 1;
    flex-direction: column;
    background-color: ${appTheme.background};
  `
}
