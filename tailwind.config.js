/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "home": "url('./static/img/bg-home.jpg')",
      },
    },
  },
  plugins: [require("flowbite/plugin")],
};
