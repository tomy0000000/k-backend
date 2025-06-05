import { defineConfig } from "@hey-api/openapi-ts"

export default defineConfig({
  input: "http://localhost:8000/openapi.json",
  output: "lib/client",
  plugins: ["@hey-api/client-axios"],
})
