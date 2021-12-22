const defaultTheme = require('tailwindcss/defaultTheme')
const cyberpunkTheme = require('daisyui/colors/themes')['[data-theme=cyberpunk]']


module.exports = {
  mode: 'jit',
  darkMode: 'media',
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true
  },
  content: [
    '../backend/**/jinja2/*.html',
    '../backend/**/jinja2/**/*.html',
    '../backend/**/static/js/*.js',
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
            maxWidth: 'none',
            a: {
              '@apply link link-primary link-hover': ''
            },
            blockquote: {
              '@apply border-l-primary': ''
            }
          }
        }
      }
    }
  },
  variants: {},
  plugins: [
    require('daisyui'),
    // Intentionally after daisyUI as its typography CSS is screwy
    require('@tailwindcss/typography')
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
        // accent: '#c07eec',
        // 'accent-focus': '#b15fe7',
        'accent-content': '#ffffff',
        // neutral: "#423f00",
        // neutral-focus: "#090901",
        // 'neutral-content': '#ffff00',
        // 'base-100': '#ffff00',
        // 'base-200': '#e0e000',
        // 'base-300': '#b8b800',
        // 'base-content': '#171731',
        // 'info': '#2094f3',
        // 'success': '#009485',
        warning: '#b88a00',
        // 'error': '#ff5724',
        '--border-btn': '0.1875rem',
        '--btn-text-case': 'none',
        '--rounded-btn': '0',
        '--navbar-padding': '0.375rem'
      }
    }]
  }
}
