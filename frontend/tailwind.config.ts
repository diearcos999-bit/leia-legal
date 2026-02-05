import type { Config } from "tailwindcss"

const config = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
        serif: ['var(--font-lora)', 'Georgia', 'serif'],
      },
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        // Pacific Blue Scale - Principal
        pacific: {
          50: "hsl(var(--pacific-50))",
          100: "hsl(var(--pacific-100))",
          200: "hsl(var(--pacific-200))",
          300: "hsl(var(--pacific-300))",
          400: "hsl(var(--pacific-400))",
          500: "hsl(var(--pacific-500))",
          600: "hsl(var(--pacific-600))",
          700: "hsl(var(--pacific-700))",
          800: "hsl(var(--pacific-800))",
          900: "hsl(var(--pacific-900))",
          950: "hsl(var(--pacific-950))",
        },
        // Terracota Andino Scale - Acento
        terracota: {
          50: "hsl(var(--terracota-50))",
          100: "hsl(var(--terracota-100))",
          200: "hsl(var(--terracota-200))",
          300: "hsl(var(--terracota-300))",
          400: "hsl(var(--terracota-400))",
          500: "hsl(var(--terracota-500))",
          600: "hsl(var(--terracota-600))",
          700: "hsl(var(--terracota-700))",
          800: "hsl(var(--terracota-800))",
          900: "hsl(var(--terracota-900))",
          950: "hsl(var(--terracota-950))",
        },
        // Slate Neutrals
        slate: {
          50: "hsl(var(--slate-50))",
          100: "hsl(var(--slate-100))",
          200: "hsl(var(--slate-200))",
          300: "hsl(var(--slate-300))",
          400: "hsl(var(--slate-400))",
          500: "hsl(var(--slate-500))",
          600: "hsl(var(--slate-600))",
          700: "hsl(var(--slate-700))",
          800: "hsl(var(--slate-800))",
          900: "hsl(var(--slate-900))",
          950: "hsl(var(--slate-950))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
        xl: "calc(var(--radius) + 4px)",
        "2xl": "calc(var(--radius) + 8px)",
      },
      boxShadow: {
        'premium': '0 1px 3px 0 rgb(0 0 0 / 0.05), 0 10px 15px -3px rgb(0 0 0 / 0.08), 0 4px 6px -4px rgb(0 0 0 / 0.05)',
        'premium-lg': '0 1px 3px 0 rgb(0 0 0 / 0.05), 0 20px 25px -5px rgb(0 0 0 / 0.08), 0 8px 10px -6px rgb(0 0 0 / 0.04)',
        'pacific': '0 4px 14px 0 hsla(221, 83%, 53%, 0.25)',
        'terracota': '0 4px 14px 0 hsla(0, 72%, 51%, 0.2)',
        'hero-input': '0 4px 20px 0 hsla(221, 83%, 53%, 0.15), 0 0 0 1px hsla(221, 83%, 53%, 0.1)',
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "fade-in-up": {
          "0%": { opacity: "0", transform: "translateY(20px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "fade-in": {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        "scale-in": {
          "0%": { opacity: "0", transform: "scale(0.95)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        "slide-in-right": {
          "0%": { transform: "translateX(100%)", opacity: "0" },
          "100%": { transform: "translateX(0)", opacity: "1" },
        },
        "count-up": {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "pulse-subtle": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.8" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "fade-in-up": "fade-in-up 0.6s ease-out forwards",
        "fade-in": "fade-in 0.4s ease-out forwards",
        "scale-in": "scale-in 0.3s ease-out forwards",
        "slide-in-right": "slide-in-right 0.4s ease-out forwards",
        "count-up": "count-up 0.5s ease-out forwards",
        "pulse-subtle": "pulse-subtle 2s ease-in-out infinite",
      },
      transitionDuration: {
        '400': '400ms',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-pacific': 'linear-gradient(135deg, hsl(var(--pacific-50)) 0%, hsl(0 0% 100%) 100%)',
        'gradient-hero': 'linear-gradient(180deg, hsl(var(--pacific-50)) 0%, hsl(0 0% 100%) 100%)',
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config

export default config
