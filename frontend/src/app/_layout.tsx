import 'expo-dev-client';
import { StatusBar } from 'expo-status-bar';
import { Slot } from 'expo-router';
import PropTypes from 'prop-types';
import styled, { ThemeProvider, type DefaultTheme } from 'styled-components/native';
import { ThemeProvider as NavProvider } from '@react-navigation/native';
import { ApolloClient, ApolloProvider, InMemoryCache, createHttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { configureStore, createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Provider } from 'react-redux';

import { appTheme, navTheme } from 'src/config/theme';
import storage from 'src/app/storage';
import { AuthProvider } from 'src/app/AuthContext';

// Define the auth state type
interface AuthState {
  isAuthenticated: boolean;
  token: string | null;
  user: any | null; // Replace 'any' with a proper user type
}

const initialState: AuthState = {
  isAuthenticated: false,
  token: null,
  user: null,
};

export const loginAsync = createAsyncThunk(
  'auth/loginAsync',
  async (credentials: { auth_token: string; }, { rejectWithValue }) => {
    try {
      await storage.setItem('auth_token', credentials.auth_token);
      return credentials.auth_token;
    } catch (error) {
      return rejectWithValue("Fail");
    }
  }
);

export const logoutAsync = createAsyncThunk(
  'auth/logoutAsync',
  async (_, { rejectWithValue }) => {
    try {
      await storage.deleteItem('auth_token');
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// Create the auth slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(loginAsync.fulfilled, (state, action: PayloadAction<{ token: string; user: any }>) => {
        console.log('Login reducer called');
        state.isAuthenticated = true;
        state.token = action.payload.token;
        state.user = action.payload.user;
      })
      .addCase(logoutAsync.fulfilled, (state) => {
        console.log('Logout reducer called');
        state.isAuthenticated = false;
        state.token = null;
        state.user = null;
      });
  },
});
// Create the root reducer
const rootReducer = {
  auth: authSlice.reducer,
  // Add other reducers here if needed
};

// Create the store
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

const authLink = setContext(async (_, { headers }) => {
  try {
    const token = await storage.getItem('auth_token');
    return {
      headers: {
        ...headers,
        authorization: token ? `Bearer ${token}` : "",
      }
    }
  } catch (error) {
    return { headers };
  }
});

const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache()
});

export default function AppLayout() {
  return (
    <AuthProvider>
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
    </AuthProvider>
  )
}

const S = {
  AppWrapper: styled.SafeAreaView`
    flex: 1;
    flex-direction: column;
    background-color: ${appTheme.background};
  `
}
