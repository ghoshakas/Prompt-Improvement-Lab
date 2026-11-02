import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    // Forward API calls to the FastAPI backend during local development so the
    // frontend can use same-origin relative paths ("/api/...") like in prod.
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
