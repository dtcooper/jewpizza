const defaultTheme = require('tailwindcss/defaultTheme')
const colors = require('tailwindcss/colors')
delete colors.lightBlue

module.exports = {
  mode: 'jit',
  darkMode: 'media',
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true
  },
  purge: {
    enabled: true,
    content: [
      '../backend/**/templates/*.html',
      '../backend/**/jinja2/*.html',
      '../backend/**/templates/**/*.html',
      '../backend/**/jinja2/**/*.html'
    ],
    safelist: [
      'animate-spin'
    ]
  },
  theme: {
    screens: {
      sm: defaultTheme.screens.sm,
      md: defaultTheme.screens.md,
      lg: defaultTheme.screens.lg,
      xl: defaultTheme.screens.xl
    },
    extend: {
      fontFamily: {
        mono: ['"Space Mono"', ...defaultTheme.fontFamily.mono]
      },
      colors: {
        'base-alt': '#ffdfad',
        ...colors
      },
      animation: {
        'spin-custom': 'spin var(--custom-spin-duration, 1s) linear infinite var(--custom-spin-direction, normal);'
      }
    }
  },
  variants: {},
  plugins: [
    require('daisyui')
  ],
  daisyui: {
    themes: [{
      jewpizza: {
        fontFamily: 'Space Mono,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace',
        primary: '#ff7598',
        'primary-focus': '#ff5784',
        'primary-content': '#000000',
        secondary: '#75d1f0',
        'secondary-focus': '#5abfdd',
        'secondary-content': '#000000',
        accent: '#c07eec',
        'accent-focus': '#af59e8',
        'accent-content': '#000000',
        neutral: '#423f00',
        'neutral-focus': '#090901',
        'neutral-content': '#ffee00',
        'base-100': '#ffee00',
        'base-200': '#dbcd00',
        'base-300': '#b8ab00',
        'base-content': '#000000',
        info: '#2094f3',
        success: '#009485',
        warning: '#ff9900',
        error: '#ff5724',
        '--btn-text-case': 'none',
        '--rounded-box': '0',
        '--rounded-btn': '0',
        '--rounded-badge': '0',
        '--tab-radius': '0'
      }
    }]
  }
}
