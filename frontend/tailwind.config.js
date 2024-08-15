/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../static/src/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'custom': '#F8F4EC',
        'custom2': '#402B3A',
        'custom3' : '#FF9BD2',
        'custom4' : '#D63484',
        'custom5' : '#211C6A',
      }
    },
  },
  plugins: [
    require('daisyui'),
  ],
};


