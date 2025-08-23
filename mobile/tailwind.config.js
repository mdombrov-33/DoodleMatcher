/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./App.tsx",
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
    "./screens/**/*.{js,jsx,ts,tsx}",
  ],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        primary: "#6366f1",
        secondary: "#f59e0b",
        background: "#fafbff",
        surface: "#fff",
        text: "#1f2937",
        textMuted: "#6b7280",
        success: "#10b981",
        error: "#8e3232",
        border: "#e5e7eb",
        disabled: "#9ca3af",
      },
    },
  },
  plugins: [],
};
