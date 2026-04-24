/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#1E3A8A',
        secondary: '#3B82F6',
        bgDark: '#0B1220',
        cardBg: '#111827',
        textPrimary: '#F9FAFB',
        textSecondary: '#9CA3AF',
        accentGlow: '#60A5FA',
      },
      backdropBlur: {
        md: '12px',
      },
    },
  },
  plugins: [],
}
