import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/", // ✅ IMPORTANT for Vercel deployment
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 3000
  }
});
