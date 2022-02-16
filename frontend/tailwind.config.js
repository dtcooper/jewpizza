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
        'primary-focus': '#f10486',
        'primary-content': '#ffffff',

        secondary: '#75d1f0',
        'secondary-focus': '#5bbedc',
        'secondary-content': '#000000',

        accent: '#c07eec',
        'accent-focus': '#ad55e7',
        'accent-content': '#ffffff',

        neutral: '#3d3a00',
        'neutral-focus': '#090901',
        'neutral-content': '#ffee00',

        'base-100': '#ffee00',
        'base-200': '#d6c800',
        'base-300': '#b8ab00',
        'base-content': '#000000',

        info: '#1c92f2',
        success: '#009485',
        warning: '#ff9900',
        error: '#ff5724',

        '--rounded-box': '0',
        '--rounded-btn': '0',
        '--rounded-badge': '0',

        '--animation-btn': '0.25s',
        '--animation-input': '0.2s',

        '--btn-text-case': 'none',
        '--navbar-padding': '0.375rem',
        '--border-btn': '0.1875rem'
      }
    }]
  }
}
