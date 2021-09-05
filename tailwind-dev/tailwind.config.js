const defaultTheme = require('tailwindcss/defaultTheme')
const colors = require('tailwindcss/colors')


module.exports = {
    mode: 'jit',
    future: {
        removeDeprecatedGapUtilities: true,
        purgeLayersByDefault: true,
    },
    purge: {
        enabled: true,
        content: [
            '../jew_pizza/**/templates/*.html',
            '../jew_pizza/**/jinja2/*.html',
            '../jew_pizza/**/templates/**/*.html',
            '../jew_pizza/**/jinja2/**/*.html',
        ],
        safelist: [
            'animate-spin'
        ],
    },
    theme: {
        screens: {
            'xs': '475px',
            ...defaultTheme.screens,
        },
        extend: {
            fontFamily: {
                mono: ['"Space Mono"', ...defaultTheme.fontFamily.mono],
            },
            colors: {
                'brand-background': '#f5dcff',
                'brand': '#fe3f3f',
                'brand-alt': '#008000',
                ...colors,
            },
            animation: {
                'spin-custom': 'spin var(--custom-spin-duration, 1s) linear infinite var(--custom-spin-direction, normal);',
            },
        }
    },
    variants: {},
    plugins: [],
}
