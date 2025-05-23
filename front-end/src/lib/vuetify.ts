import { createVuetify } from 'vuetify';
import 'vuetify/styles';
import { pl } from 'vuetify/locale'
export default createVuetify({
  defaults: {
    VBtn: {
      variant: 'outlined',
    },
    VDateInput: {
      class: 'transparent-bg',
    },
  },
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
          heroBg:'#ac6ed9',
          progressBarProgress:'#4caf50',
          progressBar:'#e0e0e0',
          delete:"#c6564c"
        },
        variables: {
          borderRadius: '24px',
          gradientText: 'linear-gradient(to right, #2f27ce, #ac6ed9)',
          fontFamily: '"Quicksand", serif',
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: '#8C7AE6',
          secondary: '#5A4E8C',
          accent: '#C778DD',
          surface:'#DEDCFF',
          text: '#E0E0E0',
          background: '#1E1E2E',
          heroBg:'#ac6ed9'
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
