import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { server } from "./src/config/server";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server,
});
