const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  darkMode: 'media',
  content: [
    '../backend/**/jinja2/*.html',
    '../backend/**/jinja2/**/*.html',
    'src/*.js',
    'src/**/*.js',
    '../backend/**/templates/*.html',
    '../backend/**/templates/**/*.html'
  ],
  safelist: [
    'animate-spin',
    'alert-success',
    'alert-info',
    'alert-warning',
    'alert-error'
  ],
  theme: {
    screens: {
      xs: '375px',
      ...defaultTheme.screens,
      '3xl': '2200px'
    },
    extend: {
      fontFamily: {
        mono: ['"Space Mono"', ...defaultTheme.fontFamily.mono],
        jewippy: ['"Pixelated MS Sans Serif"', 'Arial', 'sans-serif']
      },
      colors: {
        'base-alt': '#ffdfad'
      },
      borderWidth: {
        3: '3px'
      },
      animation: {
        'spin-custom': 'spin var(--custom-spin-duration, 1s) linear infinite var(--custom-spin-direction, normal);'
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: 'none'
          }
        }
      }
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('daisyui'),
  ],
  daisyui: {
    themes: [{
      jewpizza: {
        fontFamily: 'Space Mono,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace',
        primary: '#fc49ab',
        'primary-content': '#ffffff',
        secondary: '#5fe8ff',
        accent: '#c07eec',
        neutral: '#3d3a00',
        'neutral-content': '#ffee00',
        'base-100': '#ffee00',
        info: '#3ABFF8',
        success: '#36D399',
        warning: '#FBBD23',
        error: '#F87272',
        '--border-btn': '0.1875rem',
        '--btn-text-case': 'none',
        '--rounded-btn': '0',
        '--navbar-padding': '0.375rem'
      }
    }]
  }
}
