import { createVuetify } from 'vuetify';
import 'vuetify/styles';
import { pl } from 'vuetify/locale'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#2f27ce',
          secondary: '#dedcff',
          accent: '#ac6ed9',
          text: '#030309',
          background: '#F5F4FC',
        },
        variables: {
          borderRadius: '24px',
          gradientText: 'linear-gradient(to right, #2f27ce, #ac6ed9)',
          fontFamily: '"Roboto", serif',
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: '#BB86FC',
          secondary: '#03DAC6',
          accent: '#FF4081',
          background: '#121212',
          text: '#FFFFFF',
        },
        variables: {
          borderRadius: '24px',
          gradientText: 'linear-gradient(to right, #BB86FC, #FF4081)',
          fontFamily: '"Quicksand", serif',
        },
      },
    },
  },
  locale: {
    locale: 'pl',
    messages: { pl },
  }
});
