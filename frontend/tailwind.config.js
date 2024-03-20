import defaultTheme from "tailwindcss/defaultTheme"
import daisyui from "daisyui"
import typography from "@tailwindcss/typography"
import { addDynamicIconSelectors } from "@iconify/tailwind"

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./{src,static}/**/*.{html,js,svelte}"],
  theme: {
    screens: {
      xs: "375px",
      ...defaultTheme.screens,
      "3xl": "2200px"
    },
    extend: {
      animation: {
        "spin-custom": "spin var(--custom-spin-duration, 1s) linear infinite var(--custom-spin-direction, normal);"
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: "none"
          }
        }
      }
    }
  },
  daisyui: {
    themes: [
      {
        jewpizza: {
          fontFamily:
            "Space Mono,ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace",
          primary: "#fc49ab",
          "primary-content": "#ffffff",
          secondary: "#5fe8ff",
          accent: "#c07eec",
          neutral: "#3d3a00",
          "neutral-content": "#ffee00",
          "base-100": "#ffee00",
          info: "#3ABFF8",
          success: "#36D399",
          warning: "#FBBD23",
          error: "#F87272",
          "--border-btn": "0.1875rem"
        }
      }
    ]
  },
  plugins: [typography, daisyui, addDynamicIconSelectors()]
}
