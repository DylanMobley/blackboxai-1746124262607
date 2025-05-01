// vite.config.js

import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default ({ mode }) => {
  // Load environment variables
  const env = loadEnv(mode, process.cwd(), "");

  return defineConfig({
    plugins: [react()],
    server: {
      port: 5173,
      open: true,
      proxy: {
        "/api": {
          target: env.VITE_API_URL,
          changeOrigin: true,
          rewrite: path => path.replace(/^\/api/, "/api"),
        },
        "/clone-video": {
          target: env.VITE_CLONE_API,
          changeOrigin: true,
          rewrite: path => path.replace(/^\/clone-video/, "/clone-video"),
        },
        "/express": {
          target: env.VITE_CLONE_API,
          changeOrigin: true,
          rewrite: path => path.replace(/^\/express/, "/express"),
        },
        "/static": {
          target: env.VITE_CLONE_API,
          changeOrigin: true,
        },
      },
    },
    define: {
      "process.env": {
        VITE_API_URL: JSON.stringify(env.VITE_API_URL),
        VITE_CLONE_API: JSON.stringify(env.VITE_CLONE_API),
        VITE_TTS_API_URL: JSON.stringify(env.VITE_TTS_API_URL),
        VITE_REQUIRE_AUTH: JSON.stringify(env.VITE_REQUIRE_AUTH),
        VITE_AUTH_TOKEN_KEY: JSON.stringify(env.VITE_AUTH_TOKEN_KEY),
        VITE_MAX_TEXT_LENGTH: JSON.stringify(env.VITE_MAX_TEXT_LENGTH),
        VITE_MAX_AUDIO_MB: JSON.stringify(env.VITE_MAX_AUDIO_MB),
        VITE_MAX_IMAGE_MB: JSON.stringify(env.VITE_MAX_IMAGE_MB),
        VITE_ENABLE_AUTO_TTS: JSON.stringify(env.VITE_ENABLE_AUTO_TTS),
        VITE_ENABLE_MIC: JSON.stringify(env.VITE_ENABLE_MIC),
        VITE_PROMETHEUS_URL: JSON.stringify(env.VITE_PROMETHEUS_URL),
        VITE_GRAFANA_URL: JSON.stringify(env.VITE_GRAFANA_URL),
      },
    },
  });
};
