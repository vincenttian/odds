import { dimensions, height, width } from 'src/utils/dimensions'

/**
 * Theme For Styled Components
 * -
 */
export const appTheme = {
  background: '#00234B',
  primary: '#FFF',
  secondary: '#F2F2F2',
  highlight: '#00FF00',
  size: dimensions,
  windowHeight: `${height}px`,
  windowWidth: `${width}px`
}

/**
 * Theme For Expo Navigation Header
 * -
 */
export const navTheme = {
  dark: false,
  colors: {
    background: appTheme.background,
    border: appTheme.secondary,
    card: appTheme.background,
    notification: appTheme.highlight,
    primary: appTheme.primary,
    text: appTheme.primary
  }
}
