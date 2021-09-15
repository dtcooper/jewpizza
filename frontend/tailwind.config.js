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
        ...cyberpunkTheme,
        '--btn-text-case': 'none',
        fontFamily: 'Space Mono,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace'
      }
    }]
  }
}
