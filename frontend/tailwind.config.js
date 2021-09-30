const defaultTheme = require('tailwindcss/defaultTheme')
const colors = require('tailwindcss/colors')
const cyberpunkTheme = require('daisyui/colors/themes')['[data-theme=cyberpunk]']

delete colors.lightBlue // Avoid a tailwind deprecation warning

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
      '../backend/**/jinja2/*.html',
      '../backend/**/jinja2/**/*.html',
      '../backend/**/static/js/*.js',
      '../backend/**/templates/*.html',
      '../backend/**/templates/**/*.html'
    ],
    safelist: [
      'animate-spin'
    ]
  },
  theme: {
    screens: {
      xs: '375px',
      ...defaultTheme.screens,
      '3xl': '2200px'
    },
    extend: {
      fontFamily: {
        mono: ['"Space Mono"', ...defaultTheme.fontFamily.mono]
      },
      colors: {
        'base-alt': '#ffdfad',
        ...colors
      },
      borderWidth: {
        3: '3px'
      },
      animation: {
        'spin-custom': 'spin var(--custom-spin-duration, 1s) linear infinite var(--custom-spin-direction, normal);'
      }
    }
  },
  variants: {},
  plugins: [
    require('@tailwindcss/typography'),
    require('daisyui')
  ],
  daisyui: {
    themes: [{
      jewpizza: {
        ...cyberpunkTheme,
        fontFamily: 'Space Mono,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace',
        primary: '#fc49ab',
        'primary-focus': '#f10486',
        'primary-content': '#ffffff',
        // secondary: '#5fe8ff',
        // 'secondary-focus': '#0adaff',
        // 'secondary-content': '#171731',
        // 'accent-focus': '#b15fe7',
        // accent: '#c07eec',
        // 'accent-content': '#171731',
        // neutral: "#423f00",
        // neutral-focus: "#090901",
        // 'neutral-content': '#ffff00',
        // 'base-100': '#ffff00',
        // 'base-200': '#e0e000',
        // 'base-300': '#b8b800',
        // 'base-content': '#171731',
        '--border-btn': '0.1875rem',
        '--btn-text-case': 'none',
        '--rounded-btn': '1.25rem'
      }
    }]
  }
}
