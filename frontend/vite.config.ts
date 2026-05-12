import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: false,
    proxy: {
      "/health": "http://127.0.0.1:8000",
      "/session": "http://127.0.0.1:8000",
      "/workspaces": {
        target: "http://127.0.0.1:8000",
        bypass: (request) => {
          return request.headers.accept?.includes("text/html")
            ? "/index.html"
            : undefined;
        }
      },
      "/lifecycle": "http://127.0.0.1:8000",
      "/replay": "http://127.0.0.1:8000"
    }
  }
});
