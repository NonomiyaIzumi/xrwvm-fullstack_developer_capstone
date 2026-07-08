import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  base: "/static/",
  build: {
    outDir: "static",
    emptyOutDir: false,
    rollupOptions: {
      input: "src/main.jsx",
      output: {
        entryFileNames: "static/js/main.js",
        chunkFileNames: "static/js/[name].js",
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.endsWith(".css")) {
            return "static/css/main.css";
          }
          return "static/assets/[name][extname]";
        },
      },
    },
  },
});
