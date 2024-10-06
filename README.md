# What is this?
This is a *complete full stack **react native - python fastapi** application*

# Techstack
- Frontend:
  - **React Native** (Expo)
  - **Styled-components**: CSS-in-JS completely custom components built from the ground up.
  - **React Navigation v5**: Navigation and deep linking


- Backend:
  - **Fastapi** (Python)
  - **Postgres SQL**: Storing list of users
  
# Architecture/Organization
Code is split into two parts, the *backend* and the *frontend*.

## Backend
- **main.py**: Main fastapi endpoint which uses all of the functions above. _Websocket handling is also right here._

`export DATABASE_URL="postgresql://vincenttian@localhost:5432/odds_db"`
`python3 main.py`

`psql postgresql://vincenttian@localhost:5432/odds_db` to go into tables



## Frontend
`npm install`
`npx expo start`

