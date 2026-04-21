/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        kutahya: {
          red: '#C0392B',
          dark: '#1A1A2E',
          light: '#F5F5F0',
          accent: '#E67E22',
          muted: '#7F8C8D',
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
