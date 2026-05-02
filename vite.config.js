import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5174,
    proxy: {
      "/api": {
        target: process.env.VITE_DEV_API_TARGET || "http://localhost:5000",
        changeOrigin: true,
        secure: false,
        configure(proxy) {
          proxy.on("proxyReq", (proxyReq) => {
            // Some backends validate Origin even behind a dev proxy.
            // Removing it keeps local requests same-origin from the browser's perspective.
            proxyReq.removeHeader("origin");
          });
        },
      },
    },
  },
});
